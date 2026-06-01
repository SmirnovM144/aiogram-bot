"""
Data validation utilities for order processing.
"""
import re
from datetime import date, timedelta

from core.constants import MIN_DAYS_FOR_ORDER


class Validators:
    """Validator class for checking order data correctness."""

    @staticmethod
    def validate_phone(phone: str) -> tuple[bool, str]:
        """
        Validate phone number format.

        Args:
            phone: Phone number string

        Returns:
            Tuple of (is_valid, processed_phone_or_message)
        """
        phone = re.sub(r'\D', '', phone)

        if len(phone) != 11:
            return False, "Введите корректный номер телефона"

        return True, phone

    @staticmethod
    def validate_social_account(url: str) -> tuple[bool, str]:
        """
        Validate Telegram or VK account link.

        Args:
            url: Social network URL or username

        Returns:
            Tuple of (is_valid, message)
        """
        url = url.strip()

        # Telegram patterns
        telegram_patterns = [
            r'^@[\w]{3,32}$',  # @username
            r'^https?://t\.me/[\w]{3,32}$',  # https://t.me/username
            r'^https?://telegram\.me/[\w]{3,32}$',  # https://telegram.me/username
            r'^tg://resolve\?domain=[\w]{3,32}$',  # tg://resolve?domain=username
        ]

        # VK patterns
        vk_patterns = [
            r'^https?://vk\.com/[\w.]+$',  # https://vk.com/username
            r'^https?://www\.vk\.com/[\w.]+$',  # https://www.vk.com/username
            r'^vk\.com/[\w.]+$',  # vk.com/username
        ]

        # Check Telegram
        for pattern in telegram_patterns:
            if re.match(pattern, url, re.IGNORECASE):
                return True, url

        # Check VK
        for pattern in vk_patterns:
            if re.match(pattern, url, re.IGNORECASE):
                return True, url

        return False, (
            "Некорректная ссылка. Используйте: @username для ТГ "
            "или https://vk.com/username для ВК"
        )

    @staticmethod
    def validate_date(selected_date) -> tuple[bool, str]:
        """
        Validate that selected date is not in the past and meets minimum days requirement.

        Args:
            selected_date: Date object to validate

        Returns:
            Tuple of (is_valid, message)
        """
        # Convert datetime to date if needed
        if hasattr(selected_date, 'date'):
            selected_date = selected_date.date()

        today = date.today()
        min_date = today + timedelta(days=MIN_DAYS_FOR_ORDER)

        if selected_date < today:
            return False, "Выберите дату в будущем!"

        if selected_date < min_date:
            return False, (
                f"Можно выбрать дату минимум через {MIN_DAYS_FOR_ORDER} дня "
                "от текущей даты!"
            )

        return True, "Ок"

    @staticmethod
    def validate_fullname(fullname: str) -> tuple[bool, str]:
        """
        Validate that fullname has minimum required length.

        Args:
            fullname: User's full name

        Returns:
            Tuple of (is_valid, message)
        """
        fullname = fullname.strip()

        if len(fullname) < 3:
            return False, "Введите ФИО (минимум 3 символа)"

        return True, fullname
