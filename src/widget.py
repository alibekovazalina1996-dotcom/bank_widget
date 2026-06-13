from src.masks import get_mask_account, get_mask_card_number
import datetime


def mask_account_card(account_info: str) -> str:
    parts = account_info.split()
    if len(parts) < 2:
        raise ValueError("Недостаточно данных: укажите тип и номер")
    number = parts[-1]
    name_parts = parts[:-1]
    if not number.isdigit():
        raise ValueError("Номер должен содержать только цифры")
    if "Счет" in name_parts or "счет" in name_parts:
        masked_number = get_mask_account(number)
    else:
        if len(number) != 16:
            raise ValueError("Номер карты должен содержать 16 цифр")
        masked_number = get_mask_card_number(number)
    return " ".join(name_parts) + " " + masked_number


def get_date(date_string: str) -> str:
    date_part = date_string[:10]
    date_obj = datetime.datetime.strptime(date_part, "%Y-%m-%d")
    return date_obj.strftime("%d.%m.%Y")