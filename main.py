from src.processing import filter_by_state, sort_by_date

# Данные для проверки (из условия задачи)
data = [
    {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
    {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
    {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
    {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
]

print("Исходные данные:")
print(data)
print("\n" + "="*50 + "\n")

# Проверка фильтрации (статус по умолчанию 'EXECUTED')
executed_list = filter_by_state(data)
print("Фильтр по 'EXECUTED':")
print(executed_list)

print("\n" + "="*50 + "\n")

# Проверка фильтрации со статусом 'CANCELED'
canceled_list = filter_by_state(data, 'CANCELED')
print("Фильтр по 'CANCELED':")
print(canceled_list)

print("\n" + "="*50 + "\n")

# Проверка сортировки по убыванию (сначала новые)
sorted_desc = sort_by_date(data)
print("Сортировка по убыванию (новые сверху):")
print(sorted_desc)

print("\n" + "="*50 + "\n")

# Проверка сортировки по возрастанию
sorted_asc = sort_by_date(data, False)
print("Сортировка по возрастанию (старые сверху):")
print(sorted_asc)