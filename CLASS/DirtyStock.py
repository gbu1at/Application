from functions import *
from SETTING import *
import csv


class DirtyStock():
    def __init__(self, root):
        self.root = root
        self.initUI()

    def setting_btn(self):
        self.root.btn_find_product_dirty_stock.clicked.connect(self.click_btn_find_product_dirty_stock)

    def initUI(self):
        self.setting_btn()
        self.update_table()

    def click_btn_find_product_dirty_stock(self):
        product = self.root.edit_find_product_dirty_stock.text()
        if product == "":
            self.update_table()
        else:
            self.update_table(is_show_line=lambda x: x['name'] == product)

    def update_table(self, is_show_line=lambda x: True):
        update_table(dirtystock_path, self.root.DirtyStockTable, is_show_line)

    def add(self, product: ProductInfo, count):
        writer = open_csv_file(dirtystock_path)
        if not find_dirtystock_in_csv(product):
            writer.append({"name": product.name, "container_volume": product.container_volume, "count": 0, "volume": 0})

        writer = sorted(writer, key=lambda x: (x['name'], float(x['container_volume'])))

        with open(dirtystock_path, "w") as f:
            write = csv.DictWriter(f, fieldnames=["name", "container_volume", "count", "volume"])
            write.writeheader()
            for line in writer:
                line["volume"] = float(line["count"]) * float(line["container_volume"])
                if line['name'] == product.name and float(line["container_volume"]) == float(product.container_volume):
                    line["count"] = str(float(line['count']) + float(count))
                    line["volume"] = float(line["count"]) * float(line["container_volume"])
                write.writerow(line)

    def minus(self, product: ProductInfo, count):
        if not find_dirtystock_in_csv(product):
            raise DirtyStockEx("на грязном складе нет данной продукции")
        self.add(product, -count)
