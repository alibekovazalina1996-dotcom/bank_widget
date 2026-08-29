# Bank Widget Project  
  
## Курсовая работа: Анализ банковских транзакций  
  
Проект представляет собой приложение для анализа финансовых транзакций из Excel-файла.  
  
## Установка  
  
1. Клонируйте репозиторий:  
   ```bash  
   git clone https://github.com/alibekovazalina1996-dotcom/bank_widget.git  
   cd bank_widget  
   ```  
  
2. Установите зависимости:  
   ```bash  
   poetry install  
   ```  
  
## Модули  
  
- `utils.py` — чтение Excel, работа с датами  
- `views.py` — главная страница и события  
- `services.py` — кешбэк, инвесткопилка, поиск  
- `reports.py` — отчёты по категориям и дням недели  
  
## Тестирование  
  
```bash  
pytest tests/ -v  
```  
