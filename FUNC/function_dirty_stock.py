from FUNC.functions import *
from FUNC.function_product import get_cost_product
from FUNC.function_container import get_cost_container
from SETTING import *


def find_dirty_stock_json(product: ProductInfo):
    data = read_json(dirty_stock_json_path)
    key_product = get_key_str(product.name)
    if key_product in data:
        return str(product.container_volume) in data[key_product]
    return False


def add_dirty_stock_json(product: ProductInfo):
    data = read_json(dirty_stock_json_path)
    key_product = get_key_str(product.name)

    if key_product not in data:
        data[key_product] = {}
    data[key_product][product.container_volume] = \
        {"name": product.name,
         "container volume": product.container_volume,
         "count": 0,
         "volume": 0,
         "cost": 0,
         "container name": product.container_name,
         "sum cost": 0
         }

    write_json(dirty_stock_json_path, data)


def plus_count_dirty_stock_json(product: ProductInfo, count):
    data = read_json(dirty_stock_json_path)
    key_product = get_key_str(product.name)

    data[key_product][str(product.container_volume)]["count"] += count
    write_json(dirty_stock_json_path, data)


def update_dirty_stock_product(product: ProductInfo):
    data = read_json(dirty_stock_json_path)
    key_product = get_key_str(product.name)

    x = data[key_product][str(product.container_volume)]
    x["volume"] = x["count"] * float(product.container_volume)
    x["cost"] = get_cost_dirty_stok(product)
    data[key_product][str(product.container_volume)] = x
    write_json(dirty_stock_json_path, data)


def set_cost_dirty_stock(product: ProductInfo):
    data = read_json(dirty_stock_json_path)
    key_product = get_key_str(product.name)

    data[key_product][str(product.container_volume)]["cost"] = get_cost_dirty_stok(product)
    write_json(dirty_stock_json_path, data)


def get_cost_dirty_stok(product: ProductInfo):
    data = read_json(dirty_stock_json_path)
    key_product = get_key_str(product.name)

    line = data[key_product][str(product.container_volume)]
    volume = line["container volume"]
    cost = get_cost_container(
        ContainerInfo(product.container_name, product.container_volume)) + volume * get_cost_product(product.name)
    return cost


def data_dirty_stock_processing_for_excel():
    data = read_json(dirty_stock_json_path)
    df = {}
    for key in data["product"]["container volume"]:
        df[key] = []
    for key in data:
        if key == "product": continue
        for vol in data[key]:
            for col in data[key][vol]:
                df[col].append(data[key][vol][col])
    return df


def update_dirtystock_sum_cost():
    data = read_json(dirty_stock_json_path)
    for key in data:
        if key == "product": continue
        for vol in data[key]:
            obj = data[key][vol]
            obj["sum cost"] = float(obj["count"]) * float(obj["cost"])
    write_json(dirty_stock_json_path, data)