from src.utils import read_transactions_from_csv, read_transactions_from_xlsx

# Тест CSV
csv_data = read_transactions_from_csv("data/transactions.csv")
print(f"CSV: загружено {len(csv_data)} записей")
if csv_data:
    print("Первая запись из CSV:", csv_data[0])

# Тест XLSX
xlsx_data = read_transactions_from_xlsx("data/transactions_excel.xlsx")
print(f"XLSX: загружено {len(xlsx_data)} записей")
if xlsx_data:
    print("Первая запись из XLSX:", xlsx_data[0])