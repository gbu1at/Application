import json
from SETTING import dirty_stock_json_path
from FUNC.functions import *
from pprint import pprint

data = read_json(dirty_stock_json_path)

new_data = {}

for product in data:
    if product not in new_data:
        new_data[product] = {}
    for vol in data[product]:
        line = data[product][vol]
        if line["container name"] not in new_data[product]:
            new_data[product][line["container name"]] = {}
        line["sum cost"] = 0
        new_data[product][line["container name"]][vol] = line

write_json(dirty_stock_json_path, new_data)
