import requests
from typing import List, Dict, Any
from src.abstract_api import AbstractAPI
from src.utils import logger


class AeroplanesAPI(AbstractAPI):
    """Класс для работы с API nominatim и opensky."""

    def __init__(self):
        self.base_url_geo = "https://nominatim.openstreetmap.org/search"
        self.base_url_sky = "https://opensky-network.org/api/states/all"

    def get_country_coordinates(self, country_name: str) -> List[float]:
        """Получает boundingbox страны."""
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
            params = {"q": country_name, "format": "json", "limit": 1}
            response = requests.get(
                self.base_url_geo,
                params=params,
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            if data:
                box = data[0].get("boundingbox", [])
                if box:
                    logger.info(f"Координаты {country_name}: {box}")
                    return [float(coord) for coord in box]
            logger.error(f"Страна '{country_name}' не найдена")
            return []
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка API: {e}")
            return []

    def get_aeroplanes(self, country_name: str) -> List[Dict[str, Any]]:
        """Получает данные о самолётах в регионе."""
        coordinates = self.get_country_coordinates(country_name)
        if not coordinates:
            logger.warning(f"Не удалось получить координаты для {country_name}")
            return []

        params = {
            "lamin": coordinates[0],
            "lamax": coordinates[1],
            "lomin": coordinates[2],
            "lomax": coordinates[3],
        }

        try:
            response = requests.get(self.base_url_sky, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            aeroplanes = data.get("states", [])
            logger.info(f"Найдено {len(aeroplanes)} самолётов в {country_name}")
            return aeroplanes
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка при получении самолётов: {e}")
            return []