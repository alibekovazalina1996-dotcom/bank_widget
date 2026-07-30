import re
from typing import List, Dict, Any
from src.utils import load_transactions, read_transactions_from_csv, read_transactions_from_xlsx
from src.processing import search_by_description
from src.widget import mask_account_card, get_date


def main() -> None:
    """Основная логика программы для работы с банковскими транзакциями."""
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = input("Ваш выбор (1-3): ").strip()

    transactions = []
    file_path = ""

    if choice == "1":
        file_path = "data/operations.json"
        transactions = load_transactions(file_path)
        print("Для обработки выбран JSON-файл.")
    elif choice == "2":
        file_path = "data/transactions.csv"
        transactions = read_transactions_from_csv(file_path)
        print("Для обработки выбран CSV-файл.")
    elif choice == "3":
        file_path = "data/transactions_excel.xlsx"
        transactions = read_transactions_from_xlsx(file_path)
        print("Для обработки выбран XLSX-файл.")
    else:
        print("Неверный выбор. Завершение программы.")
        return

    if not transactions:
        print("Не удалось загрузить транзакции. Завершение программы.")
        return

    # Фильтрация по статусу
    status_filtered = filter_by_status(transactions)

    if not status_filtered:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")
        return

    # Сортировка по дате
    sort_choice = input("Отсортировать операции по дате? Да/Нет\n").strip().lower()
    if sort_choice == "да":
        order = input("Отсортировать по возрастанию или по убыванию?\n").strip().lower()
        reverse = order == "по убыванию"
        status_filtered.sort(key=lambda x: x.get("date", ""), reverse=reverse)

    # Фильтр по рублевым транзакциям
    rub_filter = input("Выводить только рублевые транзакции? Да/Нет\n").strip().lower()
    if rub_filter == "да":
        status_filtered = [tx for tx in status_filtered if tx.get("currency_code") == "RUB"]

    # Поиск по описанию
    search_filter = input("Отфильтровать список транзакций по определенному слову в описании? Да/Нет\n").strip().lower()
    if search_filter == "да":
        search_string = input("Введите слово для поиска:\n").strip()
        status_filtered = search_by_description(status_filtered, search_string)

    # Вывод результата
    print("Распечатываю итоговый список транзакций...")
    print(f"Всего банковских операций в выборке: {len(status_filtered)}")

    for tx in status_filtered:
        # Форматируем дату
        date_str = get_date(tx.get("date", ""))
        # Маскируем номер счета/карты (упрощенно)
        account = tx.get("account", "Нет данных")  # Замените на реальную маскировку
        amount = tx.get("amount", 0)
        currency = tx.get("currency_code", "RUB")
        description = tx.get("description", "Без описания")
        print(f"{date_str} {description}")
        print(f"{account} Сумма: {amount} {currency}\n")


def filter_by_status(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Фильтрует транзакции по статусу, запрашивая его у пользователя."""
    valid_statuses = {"EXECUTED", "CANCELED", "PENDING"}
    while True:
        status = input("Введите статус, по которому необходимо выполнить фильтрацию. Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING\n").strip().upper()
        if status in valid_statuses:
            print(f"Операции отфильтрованы по статусу '{status}'")
            return [tx for tx in transactions if tx.get("state", "").upper() == status]
        else:
            print(f"Статус операции '{status}' недоступен.")


if __name__ == "__main__":
    main()