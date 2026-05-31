import re
from datetime import date, timedelta


class Validators:
    """Класс для проверки корректности данных заказа"""

    @staticmethod
    def validate_phone(phone: str) -> tuple[bool, str]:
        """
        Проверяет корректность номера телефона.
        Возвращает (is_valid, processed_phone_or_message)
        """
        phone = re.sub(r'\D', '', phone)

        if len(phone) != 11:
            return False, "Введите корректный номер телефона"

        return True, phone

    @staticmethod
    def validate_social_account(url: str) -> tuple[bool, str]:
        """
        Проверяет ссылку на аккаунт Telegram или ВКонтакте.
        Возвращает (is_valid, message)
        """
        url = url.strip()

        # Паттерны для Telegram
        telegram_patterns = [
            r'^@[\w]{3,32}$',  # @username
            r'^https?://t\.me/[\w]{3,32}$',  # https://t.me/username
            # https://telegram.me/username
            r'^https?://telegram\.me/[\w]{3,32}$',
            # tg://resolve?domain=username
            r'^tg://resolve\?domain=[\w]{3,32}$',
        ]

        # Паттерны для ВКонтакте
        vk_patterns = [
            r'^https?://vk\.com/[\w.]+$',  # https://vk.com/username
            r'^https?://www\.vk\.com/[\w.]+$',  # https://www.vk.com/username
            r'^vk\.com/[\w.]+$',  # vk.com/username
        ]

        # Проверка Telegram
        for pattern in telegram_patterns:
            if re.match(pattern, url, re.IGNORECASE):
                return True, url

        # Проверка ВКонтакте
        for pattern in vk_patterns:
            if re.match(pattern, url, re.IGNORECASE):
                return True, url

        return False, "Некорректная ссылка. Используйте: @username для ТГ или https://vk.com/username для ВК"

    @staticmethod
    def validate_date(selected_date) -> tuple[bool, str]:
        """
        Проверяет, что выбранная дата не в прошлом. дата не раньше чем через 3 дня
        Возвращает (is_valid, message)
        """
        # Приводим datetime к date если нужно
        if hasattr(selected_date, 'date'):
            selected_date = selected_date.date()

        today = date.today()
        min_date = today + timedelta(days=3)

        if selected_date < today:
            return False, "Выберите дату в будущем!"

        if selected_date < min_date:
            return False, "Можно выбрать дату минимум через 3 дня от текущей даты!"

        return True, "Ок"

    @staticmethod
    def validate_fullname(fullname: str) -> tuple[bool, str]:
        """
        Проверяет, что ФИО содержит минимум 3 символа.
        Возвращает (is_valid, message)
        """
        fullname = fullname.strip()

        if len(fullname) < 3:
            return False, "Введите ФИО (минимум 3 символа)"

        return True, fullname
