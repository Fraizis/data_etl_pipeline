import json
import random


def json_handle(path: str, data):
    with open(path, mode='w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, indent=4)


sl = random.random(1, 3)
print(sl)
