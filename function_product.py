import json
from SETTING import *
from functions import *


def find_product_json(product):
    with open(product_json_path, 'r') as f:
        data = json.load(f)
    return product in data


def get_cost_product(product):
    with open(product_json_path, 'r') as f:
        data_product = json.load(f)
    with open(comp_json_path, 'r') as f:
        data_component = json.load(f)

    cost = 0
    for comp in data_product[product]["recipe"]:
        cost_comp = data_component[comp]["cost"] * data_product[product]["recipe"][comp] / 100
        cost += cost_comp
    return cost


def set_recipe(product, recipe):
    data = read_json(product_json_path)

    data[product]["recipe"] = recipe

    with open(product_json_path, 'w') as f:
        json.dump(data, f, ensure_ascii=False)


def add_product_json(product):
    data = read_json(product_json_path)

    data[product] = {"mass": 0, "cost": 0, "recipe": None}

    write_json(product_json_path, data)


def plus_product_mass_json(product, mass):
    data = read_json(product_json_path)

    data[product]["mass"] += mass

    write_json(product_json_path, data)


def update_cost_product(product):
    data = read_json(product_json_path)

    data[product]["cost"] = get_cost_product(product)

    write_json(product_json_path, data)


def get_recipe(product):
    data = read_json(product_json_path)

    return data[product]["recipe"]