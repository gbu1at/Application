import json
from SETTING import *
from FUNC.functions import *


def set_cost_container(container: ContainerInfo, new_cost: float):
    key_container = get_key_str(container.name)
    volume = container.volume

    data = read_json(container_json_path)

    data[key_container][str(volume)]["cost"] = new_cost

    write_json(container_json_path, data)


def find_container_json(container: ContainerInfo):
    data = read_json(container_json_path)
    key_container = get_key_str(container.name)
    if key_container in data:
        return str(container.volume) in data[key_container]
    return False


def get_cost_container(container: ContainerInfo):
    data = read_json(container_json_path)
    key_container = get_key_str(container.name)

    return data[key_container][str(container.volume)]["cost"]


def add_container_json(container: ContainerInfo):
    data = read_json(container_json_path)

    key_container = get_key_str(container.name)

    if key_container not in data:
        data[key_container] = {}
    data[key_container][str(container.volume)] = {"name": container.name, "volume": container.volume, "count": 0,
                                                  "cost": 0, "sum cost": 0}

    write_json(container_json_path, data)


def del_container_json(container: ContainerInfo):
    data = read_json(container_json_path)
    key_container = get_key_str(container.name)

    data[key_container].pop(str(container.volume))

    write_json(container_json_path, data)


def plus_container_count_json(container: ContainerInfo, count):
    data = read_json(container_json_path)
    key_container = get_key_str(container.name)
    data[key_container][str(container.volume)]["count"] += count

    write_json(container_json_path, data)


def update_container_sum_cost():
    data = read_json(container_json_path)
    for key in data:
        if key == "container": continue
        for vol in data[key]:
            obj = data[key][vol]
            obj["sum cost"] = float(obj["cost"]) * float(obj["count"])

    write_json(container_json_path, data)


def data_container_processing_for_excel():
    data = read_json(container_json_path)
    df = {}
    for key in data["container"]["volume"]:
        df[key] = []
    for key in data:
        if key == "container": continue
        for vol in data[key]:
            obj = data[key][vol]
            for col in obj:
                df[col].append(obj[col])
    return df


def data_container_to_csv():
    data = read_json(container_json_path)
    rows = []
    for container in data:
        if container == "container":
            continue
        for volume in data[container]:
            rows.append(data[container][volume])
    return rows
