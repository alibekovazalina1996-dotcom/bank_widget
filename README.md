## Чтение данных из CSV и Excel  
  
В модуле `utils` реализованы функции для чтения финансовых транзакций из файлов разных форматов:  
  
### `read_transactions_from_csv(file_path)`  
Читает данные из CSV-файла и возвращает список словарей.  
  
**Пример:**  
```python  
from src.utils import read_transactions_from_csv  
transactions = read_transactions_from_csv("data/transactions.csv")  
for transaction in transactions[:3]:  
    print(transaction)  
```  
  
### `read_transactions_from_xlsx(file_path)`  
Читает данные из Excel-файла (XLSX) и возвращает список словарей.  
  
**Пример:**  
```python  
from src.utils import read_transactions_from_xlsx  
transactions = read_transactions_from_xlsx("data/transactions_excel.xlsx")  
for transaction in transactions[:3]:  
    print(transaction)  
```  
