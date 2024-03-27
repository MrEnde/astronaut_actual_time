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


def find_station_by_cabin_number(stations, cabin_number: int):
    """
    Поиск станции по cabinNumber

    stations - все станции
    cabin_number - номер кабины
    :return:
    """
    for station in stations:
        if station['cabinNumber'] != cabin_number:
            continue

        return station

    return None


with open("astronaut_time.txt", encoding="utf-8") as file:
    next(file)  # пропуск headers
    headers = ["WatchNumber", "numberStation", "cabinNumber", "timeStop", "count"]
    stations = list(DictReader(file, delimiter=">", fieldnames=headers))

add_time_now(stations)

while True:
    number = input().strip()

    if number == "none":
        break

    value = find_station_by_cabin_number(stations, number)

    if value is None:
        print("В этой каюте все хорошо")
    else:
        print(
            f"В каюте {value['cabinNumber']} восстановлено время "
            f"(время остановки: {value['timeStop']}). Актуальное время: {value['timeNow']}"
        )
