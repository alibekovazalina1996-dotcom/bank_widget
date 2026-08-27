from typing import Optional, List
from src.utils import logger


class Aeroplane:
    """Класс для представления самолёта."""

    def __init__(
        self,
        icao24: str,
        country: str,
        speed: Optional[float] = None,
        altitude: Optional[float] = None,
        callsign: Optional[str] = None,
        longitude: Optional[float] = None,
        latitude: Optional[float] = None,
    ):
        self.icao24 = icao24  # Уникальный идентификатор
        self.country = country  # Страна регистрации
        self.callsign = callsign.strip() if callsign else "N/A"  # Позывной
        self.speed = self._validate_speed(speed)  # Скорость (м/с)
        self.altitude = self._validate_altitude(altitude)  # Высота (м)
        self.longitude = longitude
        self.latitude = latitude

    def _validate_speed(self, speed: Optional[float]) -> float:
        """Валидация скорости."""
        if speed is None or speed < 0:
            return 0.0
        return round(speed, 2)

    def _validate_altitude(self, altitude: Optional[float]) -> float:
        """Валидация высоты."""
        if altitude is None or altitude < 0:
            return 0.0
        return round(altitude, 2)

    def __lt__(self, other: "Aeroplane") -> bool:
        """Сравнение по скорости (для сортировки)."""
        return self.speed < other.speed

    def __gt__(self, other: "Aeroplane") -> bool:
        """Сравнение по скорости."""
        return self.speed > other.speed

    def __eq__(self, other: "Aeroplane") -> bool:
        """Сравнение по скорости."""
        return self.speed == other.speed

    def __str__(self) -> str:
        """Человекочитаемое представление."""
        return (
            f"✈️ {self.callsign} ({self.icao24})\n"
            f"   Страна: {self.country}\n"
            f"   Скорость: {self.speed} м/с\n"
            f"   Высота: {self.altitude} м"
        )

    @classmethod
    def cast_to_object_list(cls, raw_data: List) -> List["Aeroplane"]:
        """Преобразует сырые данные в список объектов Aeroplane."""
        objects = []
        for item in raw_data:
            # Согласно документации opensky, индексы:
            # 0 - icao24, 1 - callsign, 2 - country, 4 - longitude, 5 - latitude,
            # 7 - altitude, 9 - speed
            try:
                aeroplane = cls(
                    icao24=item[0],
                    callsign=item[1] if len(item) > 1 else None,
                    country=item[2] if len(item) > 2 else "Unknown",
                    longitude=item[4] if len(item) > 4 else None,
                    latitude=item[5] if len(item) > 5 else None,
                    altitude=item[7] if len(item) > 7 else None,
                    speed=item[9] if len(item) > 9 else None,
                )
                objects.append(aeroplane)
            except (IndexError, TypeError) as e:
                logger.error(f"Ошибка преобразования данных: {e}")
        return objects