from csv import DictReader
from typing import List
from datetime import time


def swap(array: List, first: int, second: int):
    """
    Функция для взаимного перемещения значений в списке

    array - список\массив элементов
    first - первый индекс
    second - второй индекс
    """

    temp = array[first]
    array[first] = array[second]
    array[second] = temp


def sort(unsorted: List, getter=lambda value: value):
    """
    Сортировка пузырьком

    Вычислительная сложность алгоритма O(n^2)

    unsorted - неотсортированный список\массив
    getter - функция для взятия значений, по которым сортируется список\массив
    """
    for i in range(len(unsorted)):
        for j in range(len(unsorted)):
            if getter(unsorted[i]) < getter(unsorted[j]):
                swap(unsorted, i, j)


def parse_time(row_string: str) -> time:
    """
    Парсинг даты формата: "hh:mm:ss"

    row_string - изначальный вид
    """
    hours, minutes, seconds = row_string.split(":")

    return time(int(hours), int(minutes), int(seconds))


def date_format(hours: int, minutes: int, seconds: int) -> str:
    """
    Функция для приведения даты в строковый формат
    Формат: hh:mm:ss

    hours - часы
    minutes - минуты
    seconds - секунды
    """
    return f"{str(hours).zfill(2)}:{str(minutes).zfill(2)}:{str(seconds).zfill(2)}"


def add_time_now(stations):
    """
    Добавляет в модели stations актуальное время

    stations - станции, которые не имеют актуального времени
    """
    for station in stations:
        last = parse_time(station['timeStop'])

        actual_time = date_format((last.hour + int(station['count'])) % 24, last.minute, last.second)

        station.setdefault('timeNow', actual_time)


def info_first_stations(stations):
    """
    Информация о трёх первых станций, которые нужнаются в помощи

    """

    sort(unsorted=stations, getter=lambda values: int(values['WatchNumber']))
    for station in stations[:3]:
        print(
            f"На станции {station['numberStation']} в каюте {station['cabinNumber']} "
            f"восстановлено время. Актуальное время: {station['timeNow']}"
        )


with open("astronaut_time.txt", encoding="utf-8") as file:
    next(file)  # пропуск headers
    headers = ["WatchNumber", "numberStation", "cabinNumber", "timeStop", "count"]
    stations = list(DictReader(file, delimiter=">", fieldnames=headers))

add_time_now(stations)
info_first_stations(stations)
