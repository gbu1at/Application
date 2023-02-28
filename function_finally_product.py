from SETTING import *
from functions import *
import json
from function_product import get_cost_product
from function_container import get_cost_container
from function_mark import get_cost_mark


def get_cost_finally_product(product: FinallyProduct):
    cost_product = get_cost_product(product.product.name)
    cost_mark = get_cost_mark(product.mark)
    cost_container = get_cost_container(product.product.container)

    return cost_product * product.product.container_volume + cost_mark + cost_container


def plus_count_finally_product(product: FinallyProduct, count):
    data = read_json(finally_product_json_path)
    name = get_key_str(product.product.name)
    volume = product.container_volume
    key = get_key_str(product.container_name) + "&" + get_key_str(product.mark.name)
    data[name][key][volume]["count"] += count
    write_json(finally_product_json_path, data)


def add_finally_product_json(product: FinallyProduct):
    data = read_json(finally_product_json_path)

    name = product.product.name
    cnt_name = product.container_name
    mark = product.mark.name

    key_name = get_key_str(name)
    key_cnt_name = get_key_str(cnt_name)
    key_mark = get_key_str(mark)
    volume = str(product.container_volume)
    if key_name not in data:
        data[key_name] = {}
    key = f"{key_cnt_name}&{key_mark}"
    if key not in data[key_name]:
        data[key_name][key] = {}
    data[key_name][key][volume] = {"name": name,
                                   "container name": cnt_name,
                                   "mark": mark,
                                   "count": 0,
                                   "cost": 0,
                                   "volume": volume}
    write_json(finally_product_json_path, data)


def find_finally_product_json(product: FinallyProduct):
    data = read_json(finally_product_json_path)
    name = get_key_str(product.product.name)
    volume = product.container_volume
    if name in data:
        key = f"{get_key_str(product.container_name)}&{get_key_str(product.mark.name)}"
        if key in data[name]:
            return str(volume) in data[name][key]
        return False
    return False


def set_cost_finaly_product(product: FinallyProduct, new_cost):
    data = read_json(finally_product_json_path)
    name = get_key_str(product.product.name)
    cnt_name = get_key_str(product.container_name)
    mark = get_key_str(product.mark.name)
    volume = str(product.container_volume)
    key = f"{cnt_name}&{mark}"

    data[name][key][volume]["cost"] = new_cost

    write_json(finally_product_json_path, data)


def update_finally_product(product: FinallyProduct):
    update_cost_finally_product(product)
    update_volume_finally_product(product)


def update_cost_finally_product(product: FinallyProduct):
    cost = get_cost_finally_product(product)
    set_cost_finaly_product(product, cost)


def update_volume_finally_product(product: FinallyProduct):
    ...
