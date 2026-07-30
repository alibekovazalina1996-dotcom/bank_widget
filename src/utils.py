import json
from typing import Any, List, Dict
from src.logger_config import setup_logger

# Создаем логгер для модуля utils
logger = setup_logger(__name__, "utils.log")


def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    """Загружает транзакции из JSON-файла."""
    logger.info(f"Попытка загрузки файла: {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if isinstance(data, list):
                logger.info(f"Успешно загружено {len(data)} транзакций")
                return data
            else:
                logger.warning(f"Файл {file_path} содержит не список, а {type(data)}")
                return []
    except FileNotFoundError:
        logger.error(f"Файл не найден: {file_path}")
        return []
    except json.JSONDecodeError as e:
        logger.error(f"Ошибка декодирования JSON в файле {file_path}: {e}")
        return []