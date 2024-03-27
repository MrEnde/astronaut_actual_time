from csv import DictReader, DictWriter
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


def cabin_number_info(stations):
    """
    Информация о кабине 98-OYE

    stations - все станции
    """
    for station in stations:
        if station['cabinNumber'] == '98-OYE':
            print(f"{station['timeNow']} - действительное время для каюты: {station['cabinNumber']}")


with open("astronaut_time.txt", encoding="utf-8") as file:
    next(file)  # пропуск headers
    headers = ["WatchNumber", "numberStation", "cabinNumber", "timeStop", "count"]
    stations = list(DictReader(file, delimiter=">", fieldnames=headers))

add_time_now(stations)
cabin_number_info(stations)

with open("new_time.csv", encoding="utf-8", mode="w") as file:
    new_headers = headers + ["timeNow"]
    writer = DictWriter(file, delimiter=",", fieldnames=new_headers, lineterminator="\n")
    writer.writeheader()
    writer.writerows(stations)
