import json
import os
from abc import ABC, abstractmethod
from typing import List, Any
from src.aeroplane import Aeroplane
from src.utils import logger


class AbstractFileSaver(ABC):
    """Абстрактный класс для работы с файлами."""

    @abstractmethod
    def add_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Добавляет информацию о самолёте в файл."""
        pass

    @abstractmethod
    def get_aeroplanes(self, filters: dict = None) -> List[Aeroplane]:
        """Получает данные о самолётах из файла."""
        pass

    @abstractmethod
    def delete_aeroplane(self, icao24: str) -> None:
        """Удаляет информацию о самолёте по ICAO24."""
        pass


class JSONSaver(AbstractFileSaver):
    """Класс для сохранения данных в JSON-файл."""

    def __init__(self, filename: str = "aeroplanes.json"):
        self.filename = filename
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        """Создаёт файл, если его нет."""
        if not os.path.exists(self.filename):
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump([], f)

    def _read_data(self) -> List[dict]:
        """Читает данные из файла."""
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _write_data(self, data: List[dict]) -> None:
        """Записывает данные в файл."""
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def add_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Добавляет самолёт в файл."""
        data = self._read_data()
        # Проверяем, нет ли уже такого ICAO24
        for item in data:
            if item.get("icao24") == aeroplane.icao24:
                logger.info(f"Самолёт {aeroplane.icao24} уже есть в файле")
                return
        # Добавляем новый
        data.append({
            "icao24": aeroplane.icao24,
            "callsign": aeroplane.callsign,
            "country": aeroplane.country,
            "speed": aeroplane.speed,
            "altitude": aeroplane.altitude,
            "longitude": aeroplane.longitude,
            "latitude": aeroplane.latitude,
        })
        self._write_data(data)
        logger.info(f"Самолёт {aeroplane.callsign} добавлен в файл")

    def get_aeroplanes(self, filters: dict = None) -> List[Aeroplane]:
        """Возвращает список самолётов из файла."""
        data = self._read_data()
        aeroplanes = []
        for item in data:
            aeroplanes.append(Aeroplane(
                icao24=item.get("icao24", ""),
                country=item.get("country", ""),
                speed=item.get("speed"),
                altitude=item.get("altitude"),
                callsign=item.get("callsign"),
                longitude=item.get("longitude"),
                latitude=item.get("latitude"),
            ))
        return aeroplanes

    def delete_aeroplane(self, icao24: str) -> None:
        """Удаляет самолёт по ICAO24."""
        data = self._read_data()
        new_data = [item for item in data if item.get("icao24") != icao24]
        if len(new_data) == len(data):
            logger.info(f"Самолёт с ICAO24 {icao24} не найден")
            return
        self._write_data(new_data)
        logger.info(f"Самолёт с ICAO24 {icao24} удалён")