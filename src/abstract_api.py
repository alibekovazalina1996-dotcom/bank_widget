from abc import ABC, abstractmethod
from typing import List, Dict, Any


class AbstractAPI(ABC):
    """Абстрактный класс для работы с API."""

    @abstractmethod
    def get_country_coordinates(self, country_name: str) -> List[float]:
        """Получает географические координаты страны."""
        pass

    @abstractmethod
    def get_aeroplanes(self, country_name: str) -> List[Dict[str, Any]]:
        """Получает информацию о самолётах в воздушном пространстве страны."""
        pass