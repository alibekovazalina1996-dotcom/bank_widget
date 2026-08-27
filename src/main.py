from src.aeroplanes_api import AeroplanesAPI
from src.aeroplane import Aeroplane
from src.json_saver import JSONSaver
from src.utils import logger


def user_interaction():
    """Функция для взаимодействия с пользователем."""
    print("✈️ Добро пожаловать в программу отслеживания самолётов!")

    # Создаём экземпляры классов
    api = AeroplanesAPI()
    saver = JSONSaver()

    # Шаг 1: Ввод страны
    country = input("Введите название страны (например, France): ").strip()
    if not country:
        print("❌ Страна не может быть пустой!")
        return

    # Получаем данные о самолётах
    print(f"⏳ Получение информации о самолётах в {country}...")
    raw_data = api.get_aeroplanes(country)
    if not raw_data:
        print("❌ Не удалось получить данные. Проверьте название страны или подключение к интернету.")
        return

    # Преобразуем в объекты
    aeroplanes = Aeroplane.cast_to_object_list(raw_data)
    print(f"✅ Найдено {len(aeroplanes)} самолётов.")

    # Ограничиваем количество сохраняемых самолётов (первые 50)
    max_planes = min(len(aeroplanes), 50)
    print(f"✅ Сохраняю первые {max_planes} самолётов из {len(aeroplanes)}...")
    for plane in aeroplanes[:max_planes]:
        saver.add_aeroplane(plane)
    print("✅ Данные сохранены в файл aeroplanes.json")

    # Шаг 2: Топ N по высоте
    try:
        top_n = int(input("Введите количество самолётов для топа по высоте (N): "))
        if top_n <= 0:
            print("❌ Число должно быть положительным!")
        else:
            sorted_by_altitude = sorted(aeroplanes, key=lambda x: x.altitude, reverse=True)
            print(f"\n🏆 Топ {top_n} самолётов по высоте:")
            for i, plane in enumerate(sorted_by_altitude[:top_n], 1):
                print(f"{i}. {plane.callsign} - {plane.altitude} м")
    except ValueError:
        print("❌ Введите число!")

    # Шаг 3: Фильтрация по стране
    filter_country = input("Введите страну регистрации для фильтрации (или оставьте пустым): ").strip()
    if filter_country:
        filtered = [p for p in aeroplanes if filter_country.lower() in p.country.lower()]
        print(f"\n🔍 Самолёты из страны '{filter_country}':")
        if filtered:
            for plane in filtered:
                print(f"  - {plane.callsign} ({plane.icao24})")
        else:
            print("  ❌ Самолёты не найдены.")

    # Шаг 4: Удаление самолёта по ICAO24
    icao_to_delete = input("Введите ICAO24 самолёта для удаления (или оставьте пустым): ").strip()
    if icao_to_delete:
        saver.delete_aeroplane(icao_to_delete)
        print(f"✅ Самолёт {icao_to_delete} удалён из файла.")


if __name__ == "__main__":
    user_interaction()