from csv import DictReader


with open("astronaut_time.txt", encoding="utf-8") as file:
    next(file)  # пропуск headers
    headers = ["WatchNumber", "numberStation", "cabinNumber", "timeStop", "count"]
    stations = list(DictReader(file, delimiter=">", fieldnames=headers))


table = {}
for station in stations:
    cabinNumber = station['cabinNumber']
    station.pop('cabinNumber')
    table[cabinNumber] = station

count = 0
for value in table.values():
    if count == 10:
        break

    count += 1
    print(" ".join(value.values()))
