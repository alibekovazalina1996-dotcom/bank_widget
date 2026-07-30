import json
import pandas as pd
from typing import Any, List, Dict
from src.logger_config import setup_logger

# Создаем логгер для модуля utils
logger = setup_logger(__name__, "utils.log")


def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    """Загружает транзакции из JSON-файла."""
    logger.info(f"Попытка загрузки JSON-файла: {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if isinstance(data, list):
                logger.info(f"Успешно загружено {len(data)} транзакций из JSON")
                return data
            else:
                logger.warning(f"Файл {file_path} содержит не список, а {type(data)}")
                return []
    except FileNotFoundError:
        logger.error(f"JSON-файл не найден: {file_path}")
        return []
    except json.JSONDecodeError as e:
        logger.error(f"Ошибка декодирования JSON в файле {file_path}: {e}")
        return []


def read_transactions_from_csv(file_path: str) -> List[Dict[str, Any]]:
    """Читает транзакции из CSV-файла и возвращает список словарей."""
    logger.info(f"Попытка загрузки CSV-файла: {file_path}")
    try:
        df = pd.read_csv(file_path)
        transactions = df.to_dict(orient='records')
        logger.info(f"Успешно загружено {len(transactions)} транзакций из CSV")
        return transactions
    except FileNotFoundError:
        logger.error(f"CSV-файл не найден: {file_path}")
        return []
    except Exception as e:
        logger.error(f"Ошибка при чтении CSV-файла {file_path}: {e}")
        return []


def read_transactions_from_xlsx(file_path: str) -> List[Dict[str, Any]]:
    """Читает транзакции из XLSX-файла и возвращает список словарей."""
    logger.info(f"Попытка загрузки XLSX-файла: {file_path}")
    try:
        df = pd.read_excel(file_path, engine='openpyxl')
        transactions = df.to_dict(orient='records')
        logger.info(f"Успешно загружено {len(transactions)} транзакций из XLSX")
        return transactions
    except FileNotFoundError:
        logger.error(f"XLSX-файл не найден: {file_path}")
        return []
    except Exception as e:
        logger.error(f"Ошибка при чтении XLSX-файла {file_path}: {e}")
        return []