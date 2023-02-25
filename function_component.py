from SETTING import *
import json


def comp_json_add(component):
    with open(comp_json_path, 'r') as f:
        data = json.load(f)
    data[component] = {"name": component, "mass": 0, "min_mass": 0, "cost": 0}
    with open(comp_json_path, 'w') as f:
        json.dump(data, f)


def comp_json_add_mass(component, mass, min_mass):
    with open(comp_json_path, 'r') as f:
        data = json.load(f)

    data[component]["mass"] += mass
    if min_mass is not None:
        data[component]["min_mass"] = min_mass

    with open(comp_json_path, 'w') as f:
        json.dump(data, f)


def del_component(component):
    with open(comp_json_path, 'r') as f:
        data = json.load(f)
        data.pop(component)

    with open(comp_json_path, 'w') as f:
        json.dump(data, f)


def set_cost_component(component, new_cost):
    with open(comp_json_path, 'r') as f:
        data = json.load(f)

    data[component]["cost"] = float(new_cost)
    with open(comp_json_path, 'w') as f:
        json.dump(data, f, ensure_ascii=False)


def find_component_json(component):
    with open(comp_json_path, 'r') as f:
        data = json.load(f)
    return component in data


def get_cost_component(component):
    with open(comp_json_path, 'r') as f:
        data = json.load(f)
    return data[component]
