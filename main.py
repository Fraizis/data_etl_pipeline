import csv
import json
import random

with open('', 'r') as file:
    csv_reader = csv.DictReader(file)
    data = list(csv_reader)

# Преобразование в JSON
json_data = json.dumps(data, indent=4)

# Запись JSON в файл
with open('output.json', 'w') as file:
    file.write(json_data)
