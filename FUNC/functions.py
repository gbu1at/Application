import csv
import json
from SETTING import *
from PyQt5.QtWidgets import QTableWidgetItem
from pandas import DataFrame
import codecs


class ContainerInfo:
    def __init__(self, name, volume):
        self.name = name
        self.volume = float(volume)


class CapInfo(ContainerInfo):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)


class ProductInfo:
    def __init__(self, name, container: ContainerInfo):
        self.name = name
        self.container = container
        self.container_volume = float(container.volume)
        self.container_name = container.name


class MarkInfo:
    def __init__(self, mark, container_volume):
        self.name = mark
        self.container_volume = float(container_volume)


class FinallyProduct:
    def __init__(self, product: ProductInfo, mark: MarkInfo):
        self.product = product
        self.mark = mark
        self.container_volume = str(product.container_volume)
        self.container_name = product.container_name


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


def find_finish_product_in_csv(product: ProductInfo):
    with open(stock_path, "r") as f:
        data = csv.DictReader(f)
        for line in data:
            if line['name'] == product.name and float(line["container_volume"]) == float(product.container_volume):
                return True
    return False


def update(root):
    root.COMPONENT.reboot_csv()
    root.MARK.reboot_csv()
    root.CONTAINER.reboot_csv()
    root.PRODUCT.reboot_csv()
    root.DIRTYSTOCK.reboot_csv()
    root.STOCK.reboot_csv()
    root.SOLDGOODS.reboot_csv()


def read_json(file_json):
    with open(file_json, 'r', encoding='utf-8-sig') as f:
        data = json.load(f)
    return data


def write_json(file_json, data):
    with open(file_json, 'w') as f:
        json.dump(data, f, ensure_ascii=False)


def get_key_str(data: str):
    return data.replace("\n", "").replace("\t", "").replace(" ", "").lower()


def write_to_excel(excel_file, data):
    x = DataFrame(data)
    x.to_excel(excel_file)


def print_excel(root):
    root.COMPONENT.update_excel()
    root.MARK.update_excel()
    root.CONTAINER.update_excel()
    root.PRODUCT.update_excel()
    root.DIRTYSTOCK.update_excel()
    root.STOCK.update_excel()
    root.SOLDGOODS.update_excel()
