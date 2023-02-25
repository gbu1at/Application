import json
from SETTING import *
from functions import ContainerInfo


def set_cost_container(container: ContainerInfo, new_cost: float):
    name = container.name
    volume = container.volume

    with open(container_json_path, 'r') as f:
        data = json.load(f)

    data[name][str(volume)]["cost"] = new_cost

    with open(container_json_path, 'w') as f:
        json.dump(data, f, ensure_ascii=False)


def find_container_json(container: ContainerInfo):
    with open(container_json_path, 'r') as f:
        data = json.load(f)

    if container.name in data:
        return str(container.volume) in data[container.name]
    return False


def get_cost_container(container: ContainerInfo):
    with open(container_json_path, 'r') as f:
        data = json.load(f)
    return data[container.name][str(container.volume)]["cost"]


def add_container_json(container: ContainerInfo):
    with open(container_json_path, 'r') as f:
        data = json.load(f)
    if container.name not in data:
        data[container.name] = {}
    data[container.name][str(container.volume)] = {"count": 0, "cost": 0}

    with open(container_json_path, "w") as f:
        json.dump(data, f)


def del_container_json(container: ContainerInfo):
    with open(container_json_path, 'r') as f:
        data = json.load(f)

    data[container.name].pop(str(container.volume))

    with open(container_json_path, "w") as f:
        json.dump(data, f)


def plus_container_count_json(container: ContainerInfo, count):
    with open(container_json_path, 'r') as f:
        data = json.load(f)

    data[container.name][str(container.volume)]["count"] += count

    with open(container_json_path, 'w') as f:
        json.dump(data, f)
