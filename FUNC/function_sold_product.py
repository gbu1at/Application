from SETTING import *
from FUNC.functions import *


def find_sold_goods_json(product: FinallyProduct):
    data = read_json(sold_goods_json_path)
    name = get_key_str(product.product.name)
    key = f"{get_key_str(product.container_name)}&{get_key_str(product.mark.name)}"
    volume = product.container_volume
    if name in data:
        if key in data[name]:
            return str(volume) in data[name][key]
        return False
    return False


def add_sold_goods_json(product: FinallyProduct):
    data = read_json(sold_goods_json_path)

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
                                   "volume": volume,
                                   "sum price": 0}
    write_json(sold_goods_json_path, data)


def plus_count_sold_goods(product: FinallyProduct, count, price):
    data = read_json(sold_goods_json_path)
    name = get_key_str(product.product.name)
    volume = product.container_volume
    key = get_key_str(product.container_name) + "&" + get_key_str(product.mark.name)
    data[name][key][volume]["count"] += count
    data[name][key][volume]["sum price"] += count * price
    write_json(sold_goods_json_path, data)


def data_sold_goods_to_csv():
    data = read_json(sold_goods_json_path)
    rows = []
    for product in data:
        if product == "product": continue
        for key in data[product]:
            x = data[product][key]
            for volume in x:
                rows.append(x[volume])
    return rows

def data_sold_goods_processing_for_excel():
    data = read_json(sold_goods_json_path)
    df = {}
    for key in data["product"]["container&mark"]["volume"]:
        df[key] = []
    for product in data:
        if product == "product": continue
        for key in data[product]:
            for vol in data[product][key]:
                line = data[product][key][vol]
                for col in line:
                    df[col].append(line[col])
    return df

