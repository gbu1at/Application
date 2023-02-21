import csv
import json

from functions import *
from SETTING import *


class Product:
    def __init__(self, root, win):
        self.root = root
        self.win = win
        self.initUI()

    def setting_btn(self):
        self.root.btn_find_product.clicked.connect(self.click_btn_find_product)

    def initUI(self):
        self.setting_btn()
        self.update_table()

    def click_btn_find_product(self):
        product = self.root.edit_find_product.text()
        if product == "":
            self.update_table()
        else:
            self.update_table(is_show_line=lambda x: x['name'] == product)

    def update_table(self, is_show_line=lambda x: True):
        update_table(product_path, self.root.ProductTable, is_show_line)

    def add(self, product, mass):
        writer = open_csv_file(product_path)
        if not find_product_in_csv(product):
            writer.append({"name": product, "mass": 0, "cost": get_cost_product(product)})

        writer = sorted(writer, key=lambda x: x['name'])

        with open(product_path, 'w') as f:
            w = csv.DictWriter(f, fieldnames=['name', 'mass', 'cost'])
            w.writeheader()
            for line in writer:
                line['cost'] = get_cost_product(line['name'])
                if line['name'] == product:
                    line['mass'] = str(float(line['mass']) + float(mass))
                w.writerow(line)

    def update_cost_product(self):
        writer = open_csv_file(product_path)
        with open(product_path, 'w') as f:
            w = csv.DictWriter(f, fieldnames=['name', 'mass', 'cost'])
            w.writeheader()
            for line in writer:
                line['cost'] = get_cost_product(line['name'])
                w.writerow(line)

    def minus(self, product, mass):
        if not find_product_in_csv(product):
            raise Exception("нет продукта")
        self.add(product, -mass)

    def find(self, product):
        with open(product_json_path) as f:
            data = json.load(f)
        if product in data:
            return data[product]
        return None
