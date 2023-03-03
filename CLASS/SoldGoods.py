from FUNC.functions import *
from SETTING import *
import csv


class SoldGoods():
    def __init__(self, root):
        self.root = root
        self.CSVPATH = sold_goods_path
        self.initUI()

    def setting_btn(self):
        self.root.btn_find_sold_goods.clicked.connect(self.click_btn_find_sold_goods)
        self.root.radio_btn_successful_product.toggled.connect(self.click_radio_btn_successful_product)

    def initUI(self):
        self.setting_btn()
        self.update_table()

    def func(self, x):
        return float(x['price']) > float(x['cost']) * 1.3

    def click_radio_btn_successful_product(self):
        if self.root.radio_btn_successful_product.isChecked():
            self.update_table(is_show_line=lambda x: self.func(x))
        else:
            self.update_table()

    def click_btn_find_sold_goods(self):
        product = self.root.edit_find_sold_goods.text()
        if product == "":
            self.update_table()
        else:
            self.update_table(is_show_line=lambda x: x['name'] == product)

    def update_table(self, is_show_line=lambda x: True):
        update_table(self.CSVPATH, self.root.SoldGoodsTable, is_show_line)

    def add(self, product: ProductInfo, count, price):
        writer = []
        is_change = False
        with open(self.CSVPATH, "r") as f:
            data = csv.DictReader(f)
            for line in data:
                if line['name'] == product.name and float(line["container_volume"]) == float(product.container_volume):
                    is_change = True
                writer.append(line)

        if not is_change:
            writer.append(
                {"name": product.name, "container_volume": product.container_volume, "count": 0, "cost": 0,
                 "price": 0})

        writer = sorted(writer, key=lambda x: (x['name'], x['container_volume']))

        with open(self.CSVPATH, "w") as f:
            write = csv.DictWriter(f, fieldnames=["name", "container_volume", "count", "cost", "price"])
            write.writeheader()
            for line in writer:
                if line['name'] == product.name and float(line["container_volume"]) == float(product.container_volume):
                    is_change = True
                    line["count"] = str(float(line['count']) + float(count))
                    line["cost"] = float(line["cost"]) + float(count) * float(product.cost)
                    line["price"] = float(line["price"]) + float(count) * float(price)
                write.writerow(line)
