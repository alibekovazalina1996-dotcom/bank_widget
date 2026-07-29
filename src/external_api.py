  import os
from typing import Dict, Any
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("EXCHANGE_RATES_API_KEY")

def convert_to_rub(transaction: Dict[str, Any]) -> float:
    amount = float(transaction.get("amount", 0))
    currency = transaction.get("currency", {}).get("code", "RUB")

    if currency not in ("USD", "EUR"):
        return amount

    if not API_KEY:
        print("Ошибка: API ключ не найден. Укажите его в файле .env")
        return amount

    try:
        url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={currency}&amount={amount}"
        headers = {"apikey": API_KEY}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return float(data.get("result", amount))
    except (requests.RequestException, KeyError, ValueError) as e:
        print(f"Ошибка при конвертации: {e}")
        return amount
