"""
Модуль с декоратором log для логирования функций.
"""

import os
from datetime import datetime
from typing import Callable, Any, Optional


def log(filename: Optional[str] = None) -> Callable:
    """
    Декоратор для логирования работы функции.

    Args:
        filename (Optional[str]): Имя файла для записи логов.
                                   Если None, логи выводятся в консоль.

    Returns:
        Callable: Обёрнутая функция с логированием.
    """
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs) -> Any:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            func_name = func.__name__

            try:
                result = func(*args, **kwargs)
                log_message = f"{timestamp} - {func_name} ok. Result: {result}"
                _write_log(log_message, filename)
                return result
            except Exception as e:
                log_message = (
                    f"{timestamp} - {func_name} error: {type(e).__name__}. "
                    f"Inputs: {args}, {kwargs}"
                )
                _write_log(log_message, filename)
                raise

        return wrapper
    return decorator


def _write_log(message: str, filename: Optional[str] = None) -> None:
    """
    Записывает сообщение в файл или выводит в консоль.

    Args:
        message (str): Сообщение для логирования.
        filename (Optional[str]): Имя файла. Если None, вывод в консоль.
    """
    if filename:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "a", encoding="utf-8") as f:
            f.write(message + "\n")
    else:
        print(message)