from SETTING import *
from functions import MarkInfo
import json


def get_cost_mark(mark: MarkInfo):
    with open(mark_json_path) as f:
        data = json.load(f)
    return data[mark.name][str(mark.container_volume)]["cost"]


def find_mark_json(mark: MarkInfo):
    with open(mark_json_path, "r") as f:
        data = json.load(f)
    if mark.name in data:
        return str(mark.container_volume) in data[mark.name]
    return False


def set_cost_mark(mark: MarkInfo, new_cost):
    with open(mark_json_path, 'r') as f:
        data = json.load(f)

    data[mark.name][str(mark.container_volume)]["cost"] = new_cost

    with open(mark_json_path, 'w') as f:
        json.dump(data, f, ensure_ascii=False)


def add_mark_json(mark: MarkInfo):
    with open(mark_json_path, 'r') as f:
        data = json.load(f)
    if mark.name not in data:
        data[mark.name] = {}
    data[mark.name][mark.container_volume] = {"count": 0, "cost": 0}

    with open(mark_json_path, 'w') as f:
        json.dump(data, f, ensure_ascii=False)


def plus_mark_count_json(mark: MarkInfo, count):
    with open(mark_json_path, 'r') as f:
        data = json.load(f)

    data[mark.name][str(mark.container_volume)]["count"] += count

    with open(mark_json_path, 'w') as f:
        json.dump(data, f)
