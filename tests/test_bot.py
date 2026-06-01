import asyncio
import unittest
from unittest.mock import AsyncMock, MagicMock
from database.db import Database


class TestCakeBotCore(unittest.IsolatedAsyncioTestCase):
    """
    Класс модульного тестирования бизнес-логики асинхронного ядра
    и объектно-реляционного взаимодействия с СУБД PostgreSQL.
    """

    # Использовался async def setUp -> переименован в asyncSetUp
    async def asyncSetUp(self):
        """Инициализация изолированного тестового окружения и моков"""
        self.mock_dsn = "postgresql://mock_user:mock_password@localhost:5432/mock_db"
        self.db = Database(self.mock_dsn)

        # Подменяем реальный пул asyncpg на мок-объект
        self.db.pool = MagicMock()

        # Создаем макеты для асинхронного соединения и контекстного менеджера пула
        self.mock_conn = AsyncMock()
        self.mock_acq_context = AsyncMock()
        self.mock_acq_context.__aenter__.return_value = self.mock_conn
        self.db.pool.acquire.return_value = self.mock_acq_context

    async def test_add_user_execution(self):
        """Тест 1: Проверка корректности SQL-запроса регистрации нового пользователя"""
        telegram_id = 8983696498
        fullname = "Иванов Иван Иванович"
        username = "ivan_cake"
        phone = "+79991112233"

        # Вызов тестируемого метода
        await self.db.add_user(telegram_id, fullname, phone, username)

        # Проверяем, что метод СУБД execute был вызван внутри контекстного менеджера
        self.db.pool.acquire.assert_called_once()
        self.mock_conn.execute.assert_called_once()

        # Извлекаем переданный SQL-запрос для верификации его структуры
        called_args = self.mock_conn.execute.call_args[0]
        self.assertIn("INSERT INTO users", called_args[0])
        self.assertIn("ON CONFLICT (telegram_id) DO NOTHING", called_args[0])

    async def test_count_orders_by_date_limit(self):
        """Тест 2: Проверка функции расчета лимита заказов на определенную дату"""
        target_date = "15.06.2026"
        expected_count = 3

        # Настраиваем мок-соединение на возврат тестового числового значения
        self.mock_conn.fetchval = AsyncMock(return_value=expected_count)

        # Вызов тестируемого метода бизнес-логики
        actual_count = await self.db.count_orders_by_date(target_date)

        # Проверка утверждений
        self.assertEqual(actual_count, expected_count)
        self.mock_conn.fetchval.assert_called_once()

        # Проверяем, что в SQL-запрос правильно подставился строковый аргумент даты
        called_args = self.mock_conn.fetchval.call_args[0]
        self.assertIn("SELECT COUNT(*)", called_args[0])
        self.assertEqual(called_args[1], target_date)

    async def test_get_catalog_returns_records(self):
        """Тест 3: Проверка корректности извлечения и сортировки записей каталога"""
        # Имитируем ответ СУБД в виде списка словарей (Record-like структуры asyncpg)
        mock_records = [
            {"id": 1, "title": "Торт Наполеон",
                "description": "Классический", "file_id": "file_id_1"},
            {"id": 2, "title": "Торт Медовик",
                "description": "Ароматный", "file_id": "file_id_2"}
        ]
        self.mock_conn.fetch = AsyncMock(return_value=mock_records)

        catalog_items = await self.db.get_catalog()

        # Проверяем структуру и наполнение возвращаемого списка
        self.assertEqual(len(catalog_items), 2)
        self.assertEqual(catalog_items[0]["title"], "Торт Наполеон")
        self.assertIn("ORDER BY created_at DESC",
                      self.mock_conn.fetch.call_args[0][0])

    async def test_add_order_mapping(self):
        """Тест 4: Проверка парсинга и сохранения FSM-контекста в реляционные поля"""
        telegram_id = 123456789
        mock_fsm_data = {
            "fullname": "Петр Петров",
            "phone_number": "+79998887766",
            "account": "@petr_tg",
            "cake": "Бенто-торт",
            "size": "S (500г)",
            "date_delivery": "20.06.2026",
            "logistics": "Самовывоз",
            "media": "photo_file_id_abc",
            "additional_info": "Сделать надпись 'С ДР!'"
        }

        await self.db.add_order(telegram_id, mock_fsm_data)

        # Убеждаемся, что запрос ушел в СУБД с правильным количеством позиционных аргументов
        self.mock_conn.execute.assert_called_once()
        executed_args = self.mock_conn.execute.call_args[0]

        # Первый аргумент - SQL строка, последующие ($1, $2...) - это параметры из FSM словаря
        self.assertEqual(executed_args[1], telegram_id)
        self.assertEqual(executed_args[2], mock_fsm_data["fullname"])
        self.assertEqual(executed_args[6], mock_fsm_data["size"])
        self.assertEqual(executed_args[10], mock_fsm_data["additional_info"])


if __name__ == "__main__":
    unittest.main()
