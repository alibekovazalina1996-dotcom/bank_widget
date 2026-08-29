import pytest
import os
import json
from src.json_saver import JSONSaver
from src.aeroplane import Aeroplane


def test_json_saver_add_and_get():
    """Тест добавления и получения самолётов."""
    saver = JSONSaver("test_aeroplanes.json")
    plane = Aeroplane("abc123", "France", speed=100.0, altitude=5000.0, callsign="AFR123")
    saver.add_aeroplane(plane)

    planes = saver.get_aeroplanes()
    assert len(planes) == 1
    assert planes[0].icao24 == "abc123"

    os.remove("test_aeroplanes.json")


def test_json_saver_delete():
    """Тест удаления самолёта."""
    saver = JSONSaver("test_aeroplanes.json")
    plane = Aeroplane("abc123", "France", speed=100.0, altitude=5000.0, callsign="AFR123")
    saver.add_aeroplane(plane)

    saver.delete_aeroplane("abc123")
    planes = saver.get_aeroplanes()
    assert len(planes) == 0

    os.remove("test_aeroplanes.json")