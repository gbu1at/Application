from SETTING import *
from functions import MarkInfo
from functions import *
import json


def get_cost_mark(mark: MarkInfo):
    data = read_json(mark_json_path)
    key_mark = get_key_str(mark.name)

    return data[key_mark][str(mark.container_volume)]["cost"]


def find_mark_json(mark: MarkInfo):
    data = read_json(mark_json_path)
    key_mark = get_key_str(mark.name)

    if key_mark in data:
        return str(mark.container_volume) in data[key_mark]
    return False


def set_cost_mark(mark: MarkInfo, new_cost):
    data = read_json(mark_json_path)

    key_mark = get_key_str(mark.name)

    data[key_mark][str(mark.container_volume)]["cost"] = new_cost

    write_json(mark_json_path, data)


def add_mark_json(mark: MarkInfo):
    data = read_json(mark_json_path)

    key_mark = get_key_str(mark.name)

    if key_mark not in data:
        data[key_mark] = {}
    data[key_mark][mark.container_volume] = {"name": mark.name, "volume": mark.container_volume, "count": 0, "cost": 0}

    write_json(mark_json_path, data)


def plus_mark_count_json(mark: MarkInfo, count):
    data = read_json(mark_json_path)

    key_mark = get_key_str(mark.name)

    data[key_mark][str(mark.container_volume)]["count"] += count

    write_json(mark_json_path, data)


def del_mark_json(mark: MarkInfo):
    data = read_json(mark_json_path)
    key_container = get_key_str(mark.name)

    data[key_container].pop(str(mark.container_volume))

    write_json(mark_json_path, data)