from SETTING import *
from functions import *
import json


def comp_json_add(component: str):
    data = read_json(comp_json_path)
    key_comp = get_key_str(component)
    data[key_comp] = {"name": component, "mass": 0, "min_mass": 0, "cost": 0}
    write_json(comp_json_path, data)


def comp_json_add_mass(component, mass, min_mass):
    data = read_json(comp_json_path)

    key_comp = get_key_str(component)
    data[key_comp]["mass"] += mass
    if min_mass is not None:
        data[key_comp]["min_mass"] = min_mass

    write_json(comp_json_path, data)


def del_component_json(component):
    data = read_json(comp_json_path)

    key_comp = get_key_str(component)
    data.pop(key_comp)

    write_json(comp_json_path, data)


def set_cost_component(component, new_cost):
    data = read_json(comp_json_path)

    key_comp = get_key_str(component)

    data[key_comp]["cost"] = float(new_cost)

    write_json(comp_json_path, data)


def find_component_json(component):
    data = read_json(comp_json_path)

    key_comp = get_key_str(component)

    return key_comp in data


def get_cost_component(component):
    data = read_json(comp_json_path)

    key_comp = get_key_str(component)

    return data[key_comp]
