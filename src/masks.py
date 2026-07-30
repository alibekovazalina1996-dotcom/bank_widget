import logging
from src.logger_config import setup_logger

# Создаем логгер для модуля masks
logger = setup_logger(__name__, "masks.log")


def get_mask_card_number(card_number: str) -> str:
    """Маскирует номер карты."""
    logger.info(f"Получен номер карты: {card_number}")
    if len(card_number) != 16 or not card_number.isdigit():
        logger.error(f"Некорректный номер карты: {card_number}")
        raise ValueError("Номер карты должен содержать ровно 16 цифр")
    masked = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[12:]}"
    logger.info(f"Замаскированный номер карты: {masked}")
    return masked


def get_mask_account(account_number: str) -> str:
    """Маскирует номер счета."""
    logger.info(f"Получен номер счета: {account_number}")
    if len(account_number) < 4 or not account_number.isdigit():
        logger.error(f"Некорректный номер счета: {account_number}")
        raise ValueError("Номер счета должен содержать минимум 4 цифры")
    masked = f"**{account_number[-4:]}"
    logger.info(f"Замаскированный номер счета: {masked}")
    return masked