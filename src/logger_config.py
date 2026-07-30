import logging
import os
from logging.handlers import RotatingFileHandler

# Создаем папку для логов, если её нет
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Настройка форматирования логов
log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
date_format = "%Y-%m-%d %H:%M:%S"

# Настройка корневого логгера
def setup_logger(name: str, log_file: str = "app.log") -> logging.Logger:
    """Настраивает и возвращает логгер с записью в файл."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Очищаем старые обработчики, чтобы не дублировать записи
    if logger.handlers:
        logger.handlers.clear()

    # Создаем обработчик для записи в файл (с ротацией)
    file_handler = RotatingFileHandler(
        os.path.join(log_dir, log_file),
        maxBytes=5*1024*1024,  # 5 MB
        backupCount=3,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)

    # Создаем обработчик для вывода в консоль (опционально, для удобства)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Устанавливаем формат для обоих обработчиков
    formatter = logging.Formatter(log_format, datefmt=date_format)
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Добавляем обработчики к логгеру
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger