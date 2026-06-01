from aiogram.fsm.state import State, StatesGroup


class Form(StatesGroup):
    fullname = State()  # ФИО заказчика
    phone_number = State()  # Номер телефона заказчика
    account = State()  # Аккаунт в соц. сетях заказчика
    cake = State()  # Выбор торта
    size = State()  # Выбор размера торта
    date = State()  # Выбор даты
    logistics = State()  # Способ доставки
    media = State()  # Медиавложения (фото/видео)
    additional_info = State()  # Дополнительная информация
    # Состояние для просмотра работ (может быть полезно для пагинации)
    viewing_works = State()
