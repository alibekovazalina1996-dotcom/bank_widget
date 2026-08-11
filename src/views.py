import os
import json
import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from src.utils import read_excel_file, get_date_range, logger

load_dotenv()

# Получаем ключи из переменных окружения
EXCHANGE_RATES_API_KEY = os.getenv("EXCHANGE_RATES_API_KEY")
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")


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


def get_currency_rates(currencies: list) -> list:
    """Получает курсы валют через API apilayer.com."""
    if not EXCHANGE_RATES_API_KEY:
        logger.warning("API ключ для валют не найден, используются заглушки")
        return [{"currency": cur, "rate": 73.21} for cur in currencies]

    rates = []
    for cur in currencies:
        try:
            url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={cur}&amount=1"
            headers = {"apikey": EXCHANGE_RATES_API_KEY}
            # Добавляем кодировку UTF-8 для корректной обработки
            response = requests.get(url, headers=headers, timeout=5)
            response.encoding = 'utf-8'
            response.raise_for_status()
            data = response.json()
            rate = data.get("result", 73.21)
        except Exception as e:
            logger.error(f"Ошибка получения курса {cur}: {e}")
            rate = 73.21
        rates.append({"currency": cur, "rate": round(rate, 2)})
    return rates

def get_stock_prices(stocks: list) -> list:
    """Получает цены акций через API Alpha Vantage."""
    if not ALPHA_VANTAGE_API_KEY:
        logger.warning("API ключ для акций не найден, используются заглушки")
        return [{"stock": stock, "price": 150.12} for stock in stocks]

    prices = []
    for stock in stocks:
        try:
            url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock}&apikey={ALPHA_VANTAGE_API_KEY}"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            price = float(data.get("Global Quote", {}).get("05. price", 150.12))
        except Exception as e:
            logger.error(f"Ошибка получения цены {stock}: {e}")
            price = 150.12
        prices.append({"stock": stock, "price": round(price, 2)})
    return prices


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


def main_page(date_str: str) -> str:
    """Главная функция для страницы 'Главная'."""
    logger.info(f"Запрос для страницы 'Главная' с датой: {date_str}")

    df = read_excel_file('data/operations.xlsx')
    if df.empty:
        return json.dumps({"error": "Нет данных"}, ensure_ascii=False)

    df['Дата операции'] = pd.to_datetime(df['Дата операции'], dayfirst=True, errors='coerce')
    df['Дата платежа'] = pd.to_datetime(df['Дата платежа'], dayfirst=True, errors='coerce')

    start_date, end_date = get_date_range(date_str)
    mask = (df['Дата операции'] >= start_date) & (df['Дата операции'] <= end_date)
    filtered_df = df.loc[mask]

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

    df = read_excel_file('data/operations.xlsx')
    if df.empty:
        return json.dumps({"error": "Нет данных"}, ensure_ascii=False)

    df['Дата операции'] = pd.to_datetime(df['Дата операции'], dayfirst=True, errors='coerce')
    df['Дата платежа'] = pd.to_datetime(df['Дата платежа'], dayfirst=True, errors='coerce')

    end_date = pd.to_datetime(date_str)
    if period == 'W':
        start_date = end_date - pd.Timedelta(days=7)
    elif period == 'M':
        start_date = end_date.replace(day=1)
    elif period == 'Y':
        start_date = end_date.replace(month=1, day=1)
    else:
        start_date = df['Дата операции'].min()

    mask = (df['Дата операции'] >= start_date) & (df['Дата операции'] <= end_date)
    filtered_df = df.loc[mask]

    expenses_df = filtered_df[filtered_df['Сумма платежа'] < 0]
    expenses_total = round(abs(expenses_df['Сумма платежа'].sum()))

    expenses_by_category = expenses_df.groupby('Категория')['Сумма платежа'].sum().abs().sort_values(ascending=False)
    top_categories = expenses_by_category.head(7)
    rest_sum = expenses_by_category.iloc[7:].sum() if len(expenses_by_category) > 7 else 0

    main_expenses = []
    for cat, amount in top_categories.items():
        main_expenses.append({"category": cat, "amount": round(amount)})
    if rest_sum > 0:
        main_expenses.append({"category": "Остальное", "amount": round(rest_sum)})

    transfers_df = expenses_df[expenses_df['Категория'].isin(['Переводы', 'Наличные'])]
    transfers_cash = transfers_df.groupby('Категория')['Сумма платежа'].sum().abs().sort_values(ascending=False)
    transfers_and_cash = [{"category": cat, "amount": round(amount)} for cat, amount in transfers_cash.items()]

    income_df = filtered_df[filtered_df['Сумма платежа'] > 0]
    income_total = round(income_df['Сумма платежа'].sum())

    income_by_category = income_df.groupby('Категория')['Сумма платежа'].sum().sort_values(ascending=False)
    main_income = [{"category": cat, "amount": round(amount)} for cat, amount in income_by_category.head(7).items()]

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