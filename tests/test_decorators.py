"""
Тесты для модуля decorators.
"""

import os
import pytest
from src.decorators import log


def test_log_to_file_success():
    """Тест логирования успешного выполнения в файл."""
    @log(filename="logs/test.log")
    def add(a, b):
        return a + b

    result = add(2, 3)
    assert result == 5

    with open("logs/test.log", "r", encoding="utf-8") as f:
        content = f.read()
        assert "add ok. Result: 5" in content

    os.remove("logs/test.log")
    os.rmdir("logs")


def test_log_to_file_error():
    """Тест логирования ошибки в файл."""
    @log(filename="logs/error.log")
    def divide(a, b):
        return a / b

    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

    with open("logs/error.log", "r", encoding="utf-8") as f:
        content = f.read()
        assert "divide error: ZeroDivisionError" in content
        assert "Inputs: (10, 0), {}" in content

    os.remove("logs/error.log")
    os.rmdir("logs")


def test_log_to_console_success(capsys):
    """Тест логирования успешного выполнения в консоль."""
    @log()
    def multiply(a, b):
        return a * b

    result = multiply(3, 4)
    assert result == 12

    captured = capsys.readouterr()
    assert "multiply ok. Result: 12" in captured.out


def test_log_to_console_error(capsys):
    """Тест логирования ошибки в консоль."""
    @log()
    def divide(a, b):
        return a / b

    with pytest.raises(ZeroDivisionError):
        divide(5, 0)

    captured = capsys.readouterr()
    assert "divide error: ZeroDivisionError" in captured.out
    assert "Inputs: (5, 0), {}" in captured.out


def test_log_with_kwargs(capsys):
    """Тест логирования с именованными аргументами."""
    @log()
    def greet(name, greeting="Hello"):
        return f"{greeting}, {name}!"

    result = greet("Alice", greeting="Hi")
    assert result == "Hi, Alice!"

    captured = capsys.readouterr()
    assert "greet ok. Result: Hi, Alice!" in captured.out


def test_log_nested_functions(capsys):
    """Тест логирования с несколькими функциями."""
    @log()
    def square(x):
        return x ** 2

    @log()
    def cube(x):
        return x ** 3

    assert square(2) == 4
    assert cube(2) == 8

    captured = capsys.readouterr()
    assert "square ok. Result: 4" in captured.out
    assert "cube ok. Result: 8" in captured.out


def test_log_with_multiple_decorators(capsys):
    """Тест логирования с несколькими декораторами."""
    @log()
    def add(a, b):
        return a + b

    @log()
    def subtract(a, b):
        return a - b

    assert add(10, 5) == 15
    assert subtract(10, 5) == 5

    captured = capsys.readouterr()
    assert "add ok. Result: 15" in captured.out
    assert "subtract ok. Result: 5" in captured.out