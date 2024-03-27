from csv import DictReader
from datetime import time


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


def info_count_groups(stations):
    """
    Вывод информации о группах, у которых остановилось время
    с период с 00.00 до 12.00 и с период с 12.01 до 23.59

    stations - все станции
    """

    time_after_group = []
    time_before_group = []

    left = time(hour=0)
    right = time(hour=12)
    second_left = time(hour=12, minute=1)
    second_right = time(hour=23, minute=59)

    for station in stations:
        date = parse_time(station['timeStop'])

        if left <= date <= right:
            time_before_group.append(station)
        elif second_left <= date <= second_right:
            time_after_group.append(station)

    print(f"{len(time_before_group)} станций остановилось с период с 00.00 до 12.00")
    print(f"{len(time_after_group)} станций остановилось с период с 12.01 до 23.59")


with open("astronaut_time.txt", encoding="utf-8") as file:
    next(file)  # пропуск headers
    headers = ["WatchNumber", "numberStation", "cabinNumber", "timeStop", "count"]
    stations = list(DictReader(file, delimiter=">", fieldnames=headers))


add_time_now(stations)
info_count_groups(stations)
