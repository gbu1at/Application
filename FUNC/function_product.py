import json
from SETTING import *
from FUNC.functions import *


def find_product_json(product):
    data = read_json(product_json_path)

    key_product = get_key_str(product)

    return key_product in data


def get_cost_product(product):
    with open(product_json_path, 'r') as f:
        data_product = json.load(f)
    with open(comp_json_path, 'r') as f:
        data_component = json.load(f)

    cost = 0
    key_product = get_key_str(product)

    for comp in data_product[key_product]["recipe"]:
        key_comp = get_key_str(comp)
        cost_comp = data_component[key_comp]["cost"] * data_product[key_product]["recipe"][comp] / 100
        cost += cost_comp
    return cost


def set_recipe(product, recipe):
    data = read_json(product_json_path)

    key_product = get_key_str(product)
    data[key_product]["recipe"] = recipe

    with open(product_json_path, 'w') as f:
        json.dump(data, f, ensure_ascii=False)


def add_product_json(product):
    data = read_json(product_json_path)

    key_product = get_key_str(product)

    data[key_product] = {"name": product, "mass": 0, "cost": 0, "recipe": None, "sum cost": 0}

    write_json(product_json_path, data)


def plus_product_mass_json(product, mass):
    data = read_json(product_json_path)
    key_product = get_key_str(product)

    data[key_product]["mass"] += mass

    write_json(product_json_path, data)


def update_cost_product(product):
    data = read_json(product_json_path)
    key_product = get_key_str(product)

    data[key_product]["cost"] = get_cost_product(product)

    write_json(product_json_path, data)


def get_recipe(product):
    data = read_json(product_json_path)
    key_product = get_key_str(product)

    return data[key_product]["recipe"]


def update_product_sum_cost():
    data = read_json(product_json_path)
    for key in data:
        obj = data[key]
        obj["sum cost"] = float(obj["cost"]) * float(obj["mass"])
    write_json(product_json_path, data)


def data_product_processing_for_excel():
    data = read_json(product_json_path)
    df = {}
    for key in data["product"]:
        if key == "recipe": continue
        df[key] = []
    for key in data:
        if key == "product": continue
        for col in data[key]:
            if col == "recipe": continue
            df[col].append(data[key][col])
    return df
