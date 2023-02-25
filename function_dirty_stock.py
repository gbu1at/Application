from functions import *
from function_product import get_cost_product
from function_container import get_cost_container
from SETTING import *


def find_dirty_stock_json(product: ProductInfo):
    data = read_json(dirty_stock_json_path)
    if product.name in data:
        return str(product.container_volume) in data[product.name]
    return False


def add_dirty_stock_json(product: ProductInfo):
    data = read_json(dirty_stock_json_path)
    if product.name not in data:
        data[product.name] = {}
    data[product.name][product.container_volume] = \
        {"name": product.name,
         "container volume": product.container_volume,
         "count": 0,
         "volume": 0,
         "cost": 0,
         "container name": product.container_name
         }

    write_json(dirty_stock_json_path, data)


def plus_count_dirty_stock_json(product: ProductInfo, count):
    data = read_json(dirty_stock_json_path)
    data[product.name][str(product.container_volume)]["count"] += count
    write_json(dirty_stock_json_path, data)


def update_dirty_stock_product(product: ProductInfo):
    data = read_json(dirty_stock_json_path)

    x = data[product.name][str(product.container_volume)]
    x["volume"] = x["count"] * float(product.container_volume)
    x["cost"] = get_cost_dirty_stok(product)
    data[product.name][str(product.container_volume)] = x
    write_json(dirty_stock_json_path, data)


def set_cost_dirty_stock(product: ProductInfo):
    data = read_json(dirty_stock_json_path)
    data[product.name][str(product.container_volume)]["cost"] = get_cost_dirty_stok(product)
    write_json(dirty_stock_json_path, data)


def get_cost_dirty_stok(product: ProductInfo):
    data = read_json(dirty_stock_json_path)
    line = data[product.name][str(product.container_volume)]
    volume = line["container volume"]
    cost = get_cost_container(
        ContainerInfo(product.container_name, product.container_volume)) + volume * get_cost_product(product.name)
    return cost
