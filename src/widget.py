"""
Модуль для маскировки данных банковских карт и счетов.
"""

from src.masks import get_mask_card_number, get_mask_account


def mask_account_card(account_info: str) -> str:
    parts = account_info.split()
    if len(parts) < 2:
        return account_info
    name = " ".join(parts[:-1])
    number = parts[-1]
    if name.lower() == "счет":
        masked = get_mask_account(number)
    else:
        masked = get_mask_card_number(number)
    return f"{name} {masked}"


def get_date(date_str: str) -> str:
    try:
        if "T" in date_str:
            date_str = date_str.split("T")[0]
        parts = date_str.split("-")
        if len(parts) == 3:
            return f"{parts[2]}.{parts[1]}.{parts[0]}"
        else:
            return date_str
    except Exception:
        return date_str
