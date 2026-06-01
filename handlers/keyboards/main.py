"""
Inline keyboard builders for the bot.
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram_calendar import SimpleCalendar


class Keyboards:
    """Class for building inline keyboards for bot messages."""

    @staticmethod
    def get_main_menu() -> InlineKeyboardMarkup:
        """
        Build main menu keyboard.

        Returns:
            Main menu inline keyboard
        """
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Каталог товаров", callback_data="catalog"),
                    InlineKeyboardButton(
                        text="Посмотреть работы", callback_data="view_works")
                ],
                [
                    InlineKeyboardButton(
                        text="Отзывы", callback_data="reviews"),
                    InlineKeyboardButton(
                        text="Написать мне", callback_data="contact_me")
                ],
                [
                    InlineKeyboardButton(
                        text="Обо мне", callback_data="about")
                ],
                [
                    InlineKeyboardButton(
                        text="Сделать заказ", callback_data="make_order")
                ]
            ]
        )
        return keyboard

    @staticmethod
    def get_miss_keyboard() -> InlineKeyboardMarkup:
        """
        Build skip button keyboard.

        Returns:
            Skip keyboard with single button
        """
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(
                text="Пропустить", callback_data="skip")]]
        )
        return keyboard

    @staticmethod
    def get_back_keyboard() -> InlineKeyboardMarkup:
        """
        Build back to main menu button keyboard.

        Returns:
            Back keyboard with single button
        """
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(
                text="Назад", callback_data="back")]]
        )
        return keyboard

    @staticmethod
    def get_cake_choice() -> InlineKeyboardMarkup:
        """
        Build cake selection keyboard.

        Returns:
            Cake choice inline keyboard
        """
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Банан-карамель", callback_data="cake_1"),
                    InlineKeyboardButton(text="Баунти", callback_data="cake_2")
                ],
                [
                    InlineKeyboardButton(
                        text="Молочная девочка", callback_data="cake_3"),
                    InlineKeyboardButton(
                        text="Красный бархат", callback_data="cake_4")
                ],
                [
                    InlineKeyboardButton(
                        text="Фисташка-малина", callback_data="cake_5"),
                    InlineKeyboardButton(
                        text="Медовик", callback_data="cake_6")
                ],
                [
                    InlineKeyboardButton(
                        text="Сникерс", callback_data="cake_7"),
                    InlineKeyboardButton(
                        text="Черный лес", callback_data="cake_8")
                ]
            ]
        )
        return keyboard

    @staticmethod
    def get_size_choice() -> InlineKeyboardMarkup:
        """
        Build cake size selection keyboard.

        Returns:
            Size choice inline keyboard
        """
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Стандарт (18см)",
                        callback_data="size_standard"),
                    InlineKeyboardButton(
                        text="Бенто (14см)",
                        callback_data="size_bento")
                ]
            ]
        )
        return keyboard

    @staticmethod
    async def get_calendar() -> InlineKeyboardMarkup:
        """
        Build date selection calendar keyboard.

        Returns:
            Calendar inline keyboard
        """
        return await SimpleCalendar().start_calendar()

    @staticmethod
    def get_logistics_choice() -> InlineKeyboardMarkup:
        """
        Build delivery method selection keyboard.

        Returns:
            Logistics choice inline keyboard
        """
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(
                    text="Самовывоз", callback_data="logistics_pickup")],
                [InlineKeyboardButton(
                    text="Доставка", callback_data="logistics_delivery")],
            ]
        )
        return keyboard

    @staticmethod
    def get_check_keyboard() -> InlineKeyboardMarkup:
        """
        Build order confirmation keyboard.

        Returns:
            Confirmation inline keyboard
        """
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Все верно", callback_data="confirm_order"),
                    InlineKeyboardButton(
                        text="Заполнить заявку заново", callback_data="edit_order")
                ]
            ]
        )
        return keyboard
