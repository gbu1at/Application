from SETTING import *
from FUNC.functions import *
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
    data[key_mark][mark.container_volume] = {"name": mark.name, "volume": mark.container_volume, "count": 0, "cost": 0,
                                             "sum cost": 0}

    write_json(mark_json_path, data)


def plus_mark_count_json(mark: MarkInfo, count):
    data = read_json(mark_json_path)

    key_mark = get_key_str(mark.name)

    data[key_mark][str(mark.container_volume)]["count"] += count

    write_json(mark_json_path, data)


def del_mark_json(mark: MarkInfo):
    data = read_json(mark_json_path)
    key_mark = get_key_str(mark.name)

    data[key_mark].pop(str(mark.container_volume))

    write_json(mark_json_path, data)


def update_mark_sum_cost():
    data = read_json(mark_json_path)
    for key in data:
        line = data[key]
        for vol in line:
            obj = line[vol]
            obj["sum cost"] = float(obj["cost"]) * float(obj["count"])

    write_json(mark_json_path, data)


def data_mark_processing_for_excel():
    data = read_json(mark_json_path)
    df = {}
    for key in data["mark"]["container volume"]:
        df[key] = []
    for key in data:
        if key == "component": continue
        for vol in data[key]:
            for col in data[key][vol]:
                df[col].append(data[key][vol][col])
    return df
