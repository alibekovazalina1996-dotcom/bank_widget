import json
import re
from collections import Counter
from datetime import datetime
import pandas as pd
from src.utils import logger


def cashback_analysis(transactions: pd.DataFrame, year: int, month: int) -> str:
    """
    Анализ выгодности категорий повышенного кешбэка.

    Аргументы:
        transactions (pd.DataFrame): Данные с транзакциями.
        year (int): Год для анализа.
        month (int): Месяц для анализа.

    Возвращает:
        str: JSON с потенциальным кешбэком по категориям.
    """
    logger.info(f"Анализ кешбэка за {month:02d}.{year}")

    # Фильтруем транзакции за указанный месяц
    df = transactions.copy()
    df['Дата операции'] = pd.to_datetime(df['Дата операции'], dayfirst=True, errors='coerce')
    mask = (df['Дата операции'].dt.year == year) & (df['Дата операции'].dt.month == month)
    filtered_df = df.loc[mask]

    # Берём только расходы (отрицательные суммы)
    expenses_df = filtered_df[filtered_df['Сумма платежа'] < 0]

    # Группируем по категориям и считаем сумму расходов
    category_spending = expenses_df.groupby('Категория')['Сумма платежа'].sum().abs()

    # Кешбэк = 1% от суммы (в рублях)
    cashback = {}
    for category, amount in category_spending.items():
        cashback[category] = round(amount * 0.01, 2)

    # Сортируем по убыванию и берём топ-10
    sorted_cashback = dict(sorted(cashback.items(), key=lambda x: x[1], reverse=True)[:10])

    return json.dumps(sorted_cashback, ensure_ascii=False, indent=2)


def investment_bank(transactions: pd.DataFrame, month: str, limit: int) -> float:
    """
    Рассчитывает сумму для Инвесткопилки.

    Аргументы:
        transactions (pd.DataFrame): Данные с транзакциями.
        month (str): Месяц в формате 'YYYY-MM'.
        limit (int): Шаг округления (10, 50 или 100).

    Возвращает:
        float: Сумма, отложенная в Инвесткопилку.
    """
    logger.info(f"Расчёт Инвесткопилки за {month} с шагом {limit}")

    # Фильтруем транзакции за указанный месяц
    df = transactions.copy()
    df['Дата операции'] = pd.to_datetime(df['Дата операции'], dayfirst=True, errors='coerce')
    target_month = pd.to_datetime(month + '-01')

    mask = (df['Дата операции'].dt.year == target_month.year) & (df['Дата операции'].dt.month == target_month.month)
    filtered_df = df.loc[mask]

    # Берём только расходы (отрицательные суммы)
    expenses_df = filtered_df[filtered_df['Сумма платежа'] < 0]

    total_saved = 0.0
    for amount in abs(expenses_df['Сумма платежа']):
        # Округление вверх до ближайшего кратного limit
        rounded = ((amount // limit) + 1) * limit if amount % limit != 0 else amount
        total_saved += rounded - amount

    return round(total_saved, 2)


def simple_search(transactions: pd.DataFrame, query: str) -> str:
    """
    Поиск транзакций по подстроке в описании или категории (регистронезависимый).

    Аргументы:
        transactions (pd.DataFrame): Данные с транзакциями.
        query (str): Строка для поиска.

    Возвращает:
        str: JSON с найденными транзакциями.
    """
    logger.info(f"Поиск транзакций по запросу: '{query}'")

    if not query:
        return json.dumps({"error": "Запрос не может быть пустым"}, ensure_ascii=False)

    df = transactions.copy()
    # Приводим к нижнему регистру для регистронезависимого поиска
    mask = (
        df['Описание'].str.lower().str.contains(query.lower(), na=False) |
        df['Категория'].str.lower().str.contains(query.lower(), na=False)
    )
    result_df = df.loc[mask]

    # Преобразуем в список словарей
    result = result_df[['Дата операции', 'Сумма платежа', 'Категория', 'Описание']].to_dict(orient='records')

    return json.dumps(result, ensure_ascii=False, indent=2, default=str)


def phone_search(transactions: pd.DataFrame) -> str:
    """
    Поиск транзакций, содержащих номера телефонов в описании.

    Аргументы:
        transactions (pd.DataFrame): Данные с транзакциями.

    Возвращает:
        str: JSON с транзакциями, содержащими номера телефонов.
    """
    logger.info("Поиск транзакций с номерами телефонов")

    # Регулярное выражение для поиска номеров телефонов
    phone_pattern = re.compile(
        r'(\+7|8)?[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}'
    )

    df = transactions.copy()
    mask = df['Описание'].apply(lambda x: bool(phone_pattern.search(str(x))) if pd.notna(x) else False)
    result_df = df.loc[mask]

    result = result_df[['Дата операции', 'Сумма платежа', 'Категория', 'Описание']].to_dict(orient='records')

    return json.dumps(result, ensure_ascii=False, indent=2, default=str)


def transfer_search(transactions: pd.DataFrame) -> str:
    """
    Поиск транзакций, относящихся к переводам физическим лицам.

    Аргументы:
        transactions (pd.DataFrame): Данные с транзакциями.

    Возвращает:
        str: JSON с транзакциями-переводами физлицам.
    """
    logger.info("Поиск переводов физическим лицам")

    # Регулярное выражение для поиска имени и инициала
    name_pattern = re.compile(r'[А-ЯЁ][а-яё]+\s[А-ЯЁ]\.')

    df = transactions.copy()
    mask = (
        (df['Категория'] == 'Переводы') &
        df['Описание'].apply(lambda x: bool(name_pattern.search(str(x))) if pd.notna(x) else False)
    )
    result_df = df.loc[mask]

    result = result_df[['Дата операции', 'Сумма платежа', 'Категория', 'Описание']].to_dict(orient='records')

    return json.dumps(result, ensure_ascii=False, indent=2, default=str)