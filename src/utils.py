import pandas as pd
import logging
from datetime import datetime

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def read_excel_file(file_path: str) -> pd.DataFrame:
    """Читает Excel-файл и возвращает DataFrame."""
    try:
        df = pd.read_excel(file_path)
        logger.info(f"Файл {file_path} успешно загружен")
        return df
    except Exception as e:
        logger.error(f"Ошибка при чтении файла {file_path}: {e}")
        return pd.DataFrame()


def get_date_range(date_str: str) -> tuple:
    """Возвращает начало месяца и дату из строки."""
    dt = pd.to_datetime(date_str)
    start_of_month = dt.replace(day=1)
    return start_of_month, dt


def format_date(date_obj) -> str:
    """Форматирует дату в dd.mm.yyyy."""
    return date_obj.strftime('%d.%m.%Y')