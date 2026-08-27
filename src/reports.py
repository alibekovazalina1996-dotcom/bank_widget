import json
from datetime import datetime, timedelta
import pandas as pd
from src.utils import logger


def spending_by_category(transactions: pd.DataFrame, category: str, date_str: str = None) -> str:
    """
    Возвращает траты по заданной категории за последние 3 месяца.

    Аргументы:
        transactions (pd.DataFrame): Данные с транзакциями.
        category (str): Название категории.
        date_str (str, optional): Дата в формате 'YYYY-MM-DD'. По умолчанию текущая.

    Возвращает:
        str: JSON с тратами по категории.
    """
    if date_str is None:
        end_date = datetime.now()
    else:
        end_date = pd.to_datetime(date_str)

    start_date = end_date - timedelta(days=90)

    logger.info(f"Отчёт по категории '{category}' с {start_date.date()} по {end_date.date()}")

    df = transactions.copy()
    df['Дата операции'] = pd.to_datetime(df['Дата операции'], dayfirst=True, errors='coerce')

    mask = (df['Дата операции'] >= start_date) & (df['Дата операции'] <= end_date)
    filtered_df = df.loc[mask]

    # Берём расходы по категории
    category_df = filtered_df[
        (filtered_df['Категория'] == category) &
        (filtered_df['Сумма платежа'] < 0)
    ]

    # Группируем по датам
    result = category_df.groupby(category_df['Дата операции'].dt.date)['Сумма платежа'].sum().abs()

    # Преобразуем в JSON
    output = {
        "category": category,
        "period": f"{start_date.date()} - {end_date.date()}",
        "total_spent": round(result.sum(), 2),
        "transactions": [
            {"date": str(date), "amount": round(amount, 2)}
            for date, amount in result.items()
        ]
    }

    return json.dumps(output, ensure_ascii=False, indent=2, default=str)


def spending_by_weekday(transactions: pd.DataFrame, date_str: str = None) -> str:
    """
    Возвращает средние траты по дням недели за последние 3 месяца.

    Аргументы:
        transactions (pd.DataFrame): Данные с транзакциями.
        date_str (str, optional): Дата в формате 'YYYY-MM-DD'. По умолчанию текущая.

    Возвращает:
        str: JSON со средними тратами по дням недели.
    """
    if date_str is None:
        end_date = datetime.now()
    else:
        end_date = pd.to_datetime(date_str)

    start_date = end_date - timedelta(days=90)

    logger.info(f"Отчёт по дням недели с {start_date.date()} по {end_date.date()}")

    df = transactions.copy()
    df['Дата операции'] = pd.to_datetime(df['Дата операции'], dayfirst=True, errors='coerce')

    mask = (df['Дата операции'] >= start_date) & (df['Дата операции'] <= end_date)
    filtered_df = df.loc[mask]

    # Берём расходы
    expenses_df = filtered_df[filtered_df['Сумма платежа'] < 0]

    # Добавляем день недели
    expenses_df['День недели'] = expenses_df['Дата операции'].dt.day_name(locale='ru_RU.UTF-8')

    # Группируем по дням недели
    weekday_spending = expenses_df.groupby('День недели')['Сумма платежа'].mean().abs()

    # Задаём порядок дней
    weekday_order = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    sorted_spending = {day: round(weekday_spending.get(day, 0), 2) for day in weekday_order}

    return json.dumps(sorted_spending, ensure_ascii=False, indent=2)


def spending_by_workday(transactions: pd.DataFrame, date_str: str = None) -> str:
    """
    Возвращает средние траты в рабочие и выходные дни за последние 3 месяца.

    Аргументы:
        transactions (pd.DataFrame): Данные с транзакциями.
        date_str (str, optional): Дата в формате 'YYYY-MM-DD'. По умолчанию текущая.

    Возвращает:
        str: JSON со средними тратами в рабочие и выходные дни.
    """
    if date_str is None:
        end_date = datetime.now()
    else:
        end_date = pd.to_datetime(date_str)

    start_date = end_date - timedelta(days=90)

    logger.info(f"Отчёт по рабочим/выходным дням с {start_date.date()} по {end_date.date()}")

    df = transactions.copy()
    df['Дата операции'] = pd.to_datetime(df['Дата операции'], dayfirst=True, errors='coerce')

    mask = (df['Дата операции'] >= start_date) & (df['Дата операции'] <= end_date)
    filtered_df = df.loc[mask]

    # Берём расходы
    expenses_df = filtered_df[filtered_df['Сумма платежа'] < 0]

    # Определяем рабочие дни (0-4) и выходные (5-6)
    expenses_df['is_weekend'] = expenses_df['Дата операции'].dt.dayofweek >= 5

    # Группируем
    workday_spending = expenses_df[~expenses_df['is_weekend']]['Сумма платежа'].mean()
    weekend_spending = expenses_df[expenses_df['is_weekend']]['Сумма платежа'].mean()

    result = {
        "workday": round(abs(workday_spending), 2) if not pd.isna(workday_spending) else 0,
        "weekend": round(abs(weekend_spending), 2) if not pd.isna(weekend_spending) else 0
    }

    return json.dumps(result, ensure_ascii=False, indent=2)