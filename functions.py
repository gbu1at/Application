import csv
import json
from SETTING import *
from PyQt5.QtWidgets import QTableWidgetItem


class ProductInfo:
    def __init__(self, name, container_volume: float, cost):
        self.name = name
        self.container_volume = float(container_volume)
        self.cost = cost


class MarkInfo:
    def __init__(self, mark, container_volume):
        self.name = mark
        self.container_volume = float(container_volume)


class ContainerInfo:
    def __init__(self, name, volume):
        self.name = name
        self.volume = float(volume)


class FinallyProduct:
    def __init__(self, product: ProductInfo, mark: MarkInfo, container: ContainerInfo):
        self.product = product
        self.mark = mark
        self.container = container


def update_table(path_csv, tableWidget, is_show_line):
    with open(path_csv, encoding="utf8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        title = reader.fieldnames
        # title = next(reader)
        tableWidget.setColumnCount(len(title))
        tableWidget.setHorizontalHeaderLabels(title)
        tableWidget.setRowCount(0)
        i = 0
        for row in reader:
            if is_show_line(row):
                tableWidget.setRowCount(
                    tableWidget.rowCount() + 1)
                for j, elem in enumerate(row):
                    tableWidget.setItem(
                        i, j, QTableWidgetItem(row[elem]))
                i += 1
    tableWidget.resizeColumnsToContents()


def open_csv_file(file):
    data_list = []
    with open(file, 'r') as f:
        data = csv.DictReader(f)
        for line in data:
            data_list.append(line)
    return data_list


def set_cost_component(component, new_cost):
    with open(comp_json_path, 'r') as f:
        data = json.load(f)

    data[component] = float(new_cost)
    with open(comp_json_path, 'w') as f:
        json.dump(data, f, ensure_ascii=False)


def set_cost_mark(mark: MarkInfo, new_cost):
    with open(mark_json_path, 'r') as f:
        data = json.load(f)

    if mark.name not in data:
        data[mark.name] = {}
    data[mark.name][str(mark.container_volume)] = new_cost

    with open(mark_json_path, 'w') as f:
        json.dump(data, f, ensure_ascii=False)


def set_cost_container(container: ContainerInfo, new_cost: float):
    name = container.name
    volume = container.volume

    with open(container_json_path, 'r') as f:
        data = json.load(f)

    if name not in data:
        data[name] = {}
    data[name][str(volume)] = new_cost

    with open(container_json_path, 'w') as f:
        json.dump(data, f, ensure_ascii=False)


def set_cost(self):
    self.PRODUCT.update_cost_product()
    self.STOCK.update_cost_product()


def find_component_json(component):
    with open(comp_json_path, 'r') as f:
        data = json.load(f)
    return component in data


def find_product_json(product):
    with open(product_json_path, 'r') as f:
        data = json.load(f)
    return product in data


def find_mark_json(mark: MarkInfo):
    with open(mark_json_path, "r") as f:
        data = json.load(f)
    if mark.name in data:
        return mark.container_volume in data[mark.name]
    return False


def find_container_json(container: ContainerInfo):
    with open(container_json_path, 'r') as f:
        data = json.load(f)

    if container.name in data:
        return container.volume in data[container.name]
    return False


def find_product_in_csv(product):
    data = open_csv_file(product_path)
    for line in data:
        if line["name"] == product:
            return True
    return False


def find_dirtystock_in_csv(product: ProductInfo):
    data = open_csv_file(dirtystock_path)
    for line in data:
        if line['name'] == product.name and float(line["container_volume"]) == float(product.container_volume):
            return True
    return False


def find_finish_product_in_csv(product: ProductInfo):
    with open(stock_path, "r") as f:
        data = csv.DictReader(f)
        for line in data:
            if line['name'] == product.name and float(line["container_volume"]) == float(product.container_volume):
                return True
    return False


def find_mark_in_csv(mark: MarkInfo):
    data = open_csv_file(mark_path)
    for line in data:
        if line["name"] == mark.name and line["container_volume"] == str(mark.container_volume):
            return True
    return False


def find_container_in_csv(container: ContainerInfo):
    data = open_csv_file(container_path)
    for line in data:
        if line["name"] == container.name and float(line["volume"]) == float(container.volume):
            return True
    return False


def get_cost_component(component):
    with open(comp_json_path, 'r') as f:
        data = json.load(f)
    return data[component]


def get_cost_mark(mark: MarkInfo):
    with open(mark_json_path) as f:
        data = json.load(f)
    return data[mark.name][str(mark.container_volume)]


def get_cost_container(container: ContainerInfo):
    with open(container_json_path, 'r') as f:
        data = json.load(f)
    return data[container.name][str(container.volume)]


def get_cost_product(product):
    with open(product_json_path, 'r') as f:
        data_product = json.load(f)
    with open(comp_json_path, 'r') as f:
        data_component = json.load(f)

    cost = 0
    for comp in data_product[product]:
        cost_comp = data_component[comp] * data_product[product][comp] / 100
        cost += cost_comp
    return cost


def get_cost_finally_product(product: FinallyProduct):
    cost_product = get_cost_product(product.product.name)
    cost_mark = get_cost_mark(product.mark)
    cost_container = get_cost_container(product.container)

    return cost_product * product.product.container_volume + cost_mark + cost_container


def set_recipe(product, recipe):
    with open(product_json_path) as f:
        data = json.load(f)

    data[product] = recipe

    with open(product_json_path, 'w') as f:
        json.dump(data, f, ensure_ascii=False)


def update(root):
    set_cost(root)
    root.COMPONENT.update_table()
    root.PRODUCT.update_table()
    root.STOCK.update_table()
