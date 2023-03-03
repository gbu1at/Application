from FUNC.functions import *
from FUNC.function_product import get_cost_product
from FUNC.function_container import get_cost_container
from SETTING import *


def find_dirty_stock_json(product: ProductInfo):
    data = read_json(dirty_stock_json_path)
    key_product = get_key_str(product.name)
    key_cnt_name = get_key_str(product.container_name)

    if key_product in data:
        if key_cnt_name in data[key_product]:
            return str(product.container_volume) in data[key_product][key_cnt_name]
    return False


def add_dirty_stock_json(product: ProductInfo):
    data = read_json(dirty_stock_json_path)
    key_product = get_key_str(product.name)
    key_cnt_name = get_key_str(product.container_name)

    if key_product not in data:
        data[key_product] = {}
    if key_cnt_name not in data[key_product]:
        data[key_product][key_cnt_name] = {}
    data[key_product][key_cnt_name][product.container_volume] = \
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
    key_cnt_name = get_key_str(product.container_name)

    data[key_product][key_cnt_name][str(product.container_volume)]["count"] += count
    write_json(dirty_stock_json_path, data)


def update_dirty_stock_product(product: ProductInfo):
    data = read_json(dirty_stock_json_path)
    key_product = get_key_str(product.name)
    key_cnt_name = get_key_str(product.container_name)

    x = data[key_product][key_cnt_name][str(product.container_volume)]
    x["volume"] = x["count"] * float(product.container_volume)
    x["cost"] = get_cost_dirty_stok(product)
    data[key_product][key_cnt_name][str(product.container_volume)] = x
    write_json(dirty_stock_json_path, data)


def set_cost_dirty_stock(product: ProductInfo):
    data = read_json(dirty_stock_json_path)
    key_product = get_key_str(product.name)
    key_cnt_name = get_key_str(product.container_name)

    data[key_product][key_cnt_name][str(product.container_volume)]["cost"] = get_cost_dirty_stok(product)
    write_json(dirty_stock_json_path, data)


def get_cost_dirty_stok(product: ProductInfo):
    data = read_json(dirty_stock_json_path)
    key_product = get_key_str(product.name)
    key_cnt_name = get_key_str(product.container_name)

    line = data[key_product][key_cnt_name][str(product.container_volume)]
    volume = line["container volume"]
    cost = get_cost_container(
        ContainerInfo(product.container_name, product.container_volume)) + volume * get_cost_product(product.name)
    return cost


def data_dirty_stock_processing_for_excel():
    data = read_json(dirty_stock_json_path)
    df = {}
    for key in data["product"]["container name"]["container volume"]:
        df[key] = []
    for key in data:
        if key == "product": continue
        for cnt_name in data[key]:
            for vol in data[key][cnt_name]:
                for col in data[key][cnt_name][vol]:
                    df[col].append(data[key][cnt_name][vol][col])
    return df


def update_dirtystock_sum_cost():
    data = read_json(dirty_stock_json_path)
    for key in data:
        if key == "product": continue
        for cnt_name in data[key]:
            for vol in data[key][cnt_name]:
                obj = data[key][cnt_name][vol]
                obj["sum cost"] = float(obj["count"]) * float(obj["cost"])
    write_json(dirty_stock_json_path, data)


def data_product_processing_for_excel():
    data = read_json(product_json_path)
    df = {}
    for key in data["product"]["container name"]["container volume"]:
        df[key] = []
    for key in data:
        if key == "product": continue
        for cnt_name in data[key]:
            for vol in data[key][cnt_name]:
                line = data[key][cnt_name][vol]
                for col in line:
                    df[col].append(line[col])
    return df


def data_dirtystock_to_csv():
    data = read_json(dirty_stock_json_path)
    df = {}
    for key in data["product"]["container name"]["container volume"]:
        df[key] = []
    rows = []
    for key in data:
        if key == "product": continue
        for cnt_name in data[key]:
            for vol in data[key][cnt_name]:
                rows.append(data[key][cnt_name][vol])
    return rows
