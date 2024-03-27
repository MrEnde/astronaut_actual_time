from csv import DictReader
from datetime import time


def parse_time(row_string: str) -> time:
    """
    Парсинг даты формата: "hh:mm:ss"

    row_string - изначальный вид
    """
    hours, minutes, seconds = row_string.split(":")

    return time(int(hours), int(minutes), int(seconds))


def info_count_groups(stations):
    """
    Вывод информации о группах, у которых остановилось время
    с период с 00.00 до 12.00 и с период с 12.01 до 23.59

    stations - все станции
    """

    time_after_group = []
    time_before_group = []

    left = time(hour=0)
    right = time(hour=12, second=59)

    for station in stations:
        date = parse_time(station['timeStop'])

        if left <= date <= right:
            time_before_group.append(station)
        else:
            time_after_group.append(station)

    print(f"{len(time_before_group)} станций остановилось с период с 00.00 до 12.00")
    print(f"{len(time_after_group)} станций остановилось с период с 12.01 до 23.59")


with open("astronaut_time.txt", encoding="utf-8") as file:
    next(file)  # пропуск headers
    headers = ["WatchNumber", "numberStation", "cabinNumber", "timeStop", "count"]
    stations = list(DictReader(file, delimiter=">", fieldnames=headers))


info_count_groups(stations)
