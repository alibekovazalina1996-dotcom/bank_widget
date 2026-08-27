import pytest
from src.aeroplane import Aeroplane


def test_aeroplane_creation():
    """Тест создания самолёта."""
    plane = Aeroplane("abc123", "France", speed=100.5, altitude=5000.0, callsign="AFR123")
    assert plane.icao24 == "abc123"
    assert plane.country == "France"
    assert plane.speed == 100.5
    assert plane.altitude == 5000.0
    assert plane.callsign == "AFR123"


def test_aeroplane_invalid_speed():
    """Тест валидации скорости."""
    plane = Aeroplane("abc123", "France", speed=-10.0)
    assert plane.speed == 0.0


def test_aeroplane_invalid_altitude():
    """Тест валидации высоты."""
    plane = Aeroplane("abc123", "France", altitude=-500.0)
    assert plane.altitude == 0.0


def test_aeroplane_comparison():
    """Тест сравнения самолётов по скорости."""
    plane1 = Aeroplane("abc123", "France", speed=100.0)
    plane2 = Aeroplane("def456", "Germany", speed=200.0)
    assert plane1 < plane2
    assert plane2 > plane1
    assert plane1 == plane1


def test_aeroplane_cast_to_object_list():
    """Тест преобразования сырых данных в объекты."""
    raw_data = [
        ["abc123", "AFR123", "France", None, 2.0, 3.0, None, 5000.0, None, 100.0],
        ["def456", None, "Germany", None, 5.0, 6.0, None, 3000.0, None, 200.0],
    ]
    objects = Aeroplane.cast_to_object_list(raw_data)
    assert len(objects) == 2
    assert objects[0].icao24 == "abc123"
    assert objects[0].callsign == "AFR123"
    assert objects[1].country == "Germany"