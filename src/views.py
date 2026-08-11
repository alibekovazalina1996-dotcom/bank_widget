from datetime import datetime
import json
import pandas as pd
from src.utils import read_excel_file, get_date_range, format_date, logger


def get_greeting() -> str:
    """Возвращает приветствие в зависимости от времени."""
    hour = datetime.now().hour
    if 6 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def get_card_data(transactions: pd.DataFrame) -> list:
    """Возвращает данные по картам: последние 4 цифры, расходы, кешбэк."""
    if 'Номер карты' not in transactions.columns:
        return []
    
    card_groups = transactions.groupby('Номер карты')
    result = []
    for card, group in card_groups:
        last_digits = str(card)[-4:] if card else '0000'
        total_spent = group['Сумма платежа'].sum()
        cashback = total_spent / 100
        result.append({
            "last_digits": last_digits,
            "total_spent": round(total_spent, 2),
            "cashback": round(cashback, 2)
        })
    return result


def get_top_transactions(transactions: pd.DataFrame, n: int = 5) -> list:
    """Возвращает топ-N транзакций по сумме платежа."""
    sorted_tx = transactions.sort_values(by='Сумма платежа', ascending=False).head(n)
    result = []
    for _, row in sorted_tx.iterrows():
        # Преобразуем дату в строку
        date_val = row.get('Дата платежа')
        if pd.isna(date_val):
            date_str = ''
        elif isinstance(date_val, pd.Timestamp):
            date_str = date_val.strftime('%d.%m.%Y')
        else:
            date_str = str(date_val)
        result.append({
            "date": date_str,
            "amount": round(row.get('Сумма платежа', 0), 2),
            "category": row.get('Категория', ''),
            "description": row.get('Описание', '')
        })
    return result


def get_currency_rates(currencies: list) -> list:
    """Получает курсы валют через API."""
    # Здесь нужно будет подключить реальный API
    # Пока возвращаем заглушку
    rates = []
    for cur in currencies:
        rates.append({
            "currency": cur,
            "rate": 73.21  # Заглушка
        })
    return rates


def get_stock_prices(stocks: list) -> list:
    """Получает цены акций через API."""
    # Здесь нужно будет подключить реальный API
    # Пока возвращаем заглушку
    prices = []
    for stock in stocks:
        prices.append({
            "stock": stock,
            "price": 150.12  # Заглушка
        })
    return prices


def main_page(date_str: str) -> str:
    """Главная функция для страницы 'Главная'."""
    logger.info(f"Запрос для страницы 'Главная' с датой: {date_str}")

    # Читаем файл
    df = read_excel_file('data/operations.xlsx')
    if df.empty:
        return json.dumps({"error": "Нет данных"}, ensure_ascii=False)

    # Преобразуем даты в datetime
    df['Дата операции'] = pd.to_datetime(df['Дата операции'], dayfirst=True, errors='coerce')
    df['Дата платежа'] = pd.to_datetime(df['Дата платежа'], dayfirst=True, errors='coerce')

    # Определяем диапазон дат
    start_date, end_date = get_date_range(date_str)
    mask = (df['Дата операции'] >= start_date) & (df['Дата операции'] <= end_date)
    filtered_df = df.loc[mask]

    # Загружаем настройки пользователя
    try:
        with open('user_settings.json', 'r', encoding='utf-8') as f:
            settings = json.load(f)
    except FileNotFoundError:
        settings = {"user_currencies": [], "user_stocks": []}
        logger.warning("Файл user_settings.json не найден, используются пустые настройки")

    response = {
        "greeting": get_greeting(),
        "cards": get_card_data(filtered_df),
        "top_transactions": get_top_transactions(filtered_df, 5),
        "currency_rates": get_currency_rates(settings.get('user_currencies', [])),
        "stock_prices": get_stock_prices(settings.get('user_stocks', []))
    }

    return json.dumps(response, ensure_ascii=False, indent=2)

def events_page(date_str: str, period: str = 'M') -> str:
    """Страница 'События' — аналитика расходов и поступлений."""
    logger.info(f"Запрос для страницы 'События' с датой: {date_str}, период: {period}")

    # Читаем файл
    df = read_excel_file('data/operations.xlsx')
    if df.empty:
        return json.dumps({"error": "Нет данных"}, ensure_ascii=False)

    # Преобразуем даты
    df['Дата операции'] = pd.to_datetime(df['Дата операции'], dayfirst=True, errors='coerce')
    df['Дата платежа'] = pd.to_datetime(df['Дата платежа'], dayfirst=True, errors='coerce')

    # Определяем диапазон дат
    end_date = pd.to_datetime(date_str)
    if period == 'W':
        start_date = end_date - pd.Timedelta(days=7)
    elif period == 'M':
        start_date = end_date.replace(day=1)
    elif period == 'Y':
        start_date = end_date.replace(month=1, day=1)
    else:  # ALL
        start_date = df['Дата операции'].min()

    mask = (df['Дата операции'] >= start_date) & (df['Дата операции'] <= end_date)
    filtered_df = df.loc[mask]

    # Расходы (отрицательные суммы)
    expenses_df = filtered_df[filtered_df['Сумма платежа'] < 0]
    expenses_total = round(abs(expenses_df['Сумма платежа'].sum()))

    # Группируем расходы по категориям
    expenses_by_category = expenses_df.groupby('Категория')['Сумма платежа'].sum().abs().sort_values(ascending=False)
    top_categories = expenses_by_category.head(7)
    rest_sum = expenses_by_category.iloc[7:].sum() if len(expenses_by_category) > 7 else 0

    # Формируем main расходов
    main_expenses = []
    for cat, amount in top_categories.items():
        main_expenses.append({"category": cat, "amount": round(amount)})
    if rest_sum > 0:
        main_expenses.append({"category": "Остальное", "amount": round(rest_sum)})

    # Переводы и наличные
    transfers_df = expenses_df[expenses_df['Категория'].isin(['Переводы', 'Наличные'])]
    transfers_cash = transfers_df.groupby('Категория')['Сумма платежа'].sum().abs().sort_values(ascending=False)
    transfers_and_cash = [{"category": cat, "amount": round(amount)} for cat, amount in transfers_cash.items()]

    # Поступления (положительные суммы)
    income_df = filtered_df[filtered_df['Сумма платежа'] > 0]
    income_total = round(income_df['Сумма платежа'].sum())

    income_by_category = income_df.groupby('Категория')['Сумма платежа'].sum().sort_values(ascending=False)
    main_income = [{"category": cat, "amount": round(amount)} for cat, amount in income_by_category.head(7).items()]

    # Загружаем настройки пользователя
    try:
        with open('user_settings.json', 'r', encoding='utf-8') as f:
            settings = json.load(f)
    except FileNotFoundError:
        settings = {"user_currencies": [], "user_stocks": []}

    response = {
        "expenses": {
            "total_amount": expenses_total,
            "main": main_expenses,
            "transfers_and_cash": transfers_and_cash
        },
        "income": {
            "total_amount": income_total,
            "main": main_income
        },
        "currency_rates": get_currency_rates(settings.get('user_currencies', [])),
        "stock_prices": get_stock_prices(settings.get('user_stocks', []))
    }

    return json.dumps(response, ensure_ascii=False, indent=2)