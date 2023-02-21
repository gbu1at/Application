from functions import *
from SETTING import *
import csv


class FinishedProducts():
    def __init__(self, root):
        self.root = root
        self.initUI()

    def setting_btn(self):
        self.root.btn_find_product_stock.clicked.connect(self.click_btn_find_product_stock)
        self.root.radio_btn_lack_product.toggled.connect(self.click_radio_btn_lack_product)

    def initUI(self):
        self.setting_btn()
        self.update_table()

    def click_radio_btn_lack_product(self):
        if self.root.radio_btn_lack_product.isChecked():
            self.update_table(is_show_line=lambda x: float(x['count']) < 100)
        else:
            self.update_table()

    def click_btn_find_product_stock(self):
        product = self.root.edit_find_product_stock.text()
        if product == "":
            self.update_table()
        else:
            self.update_table(is_show_line=lambda x: x['name'] == product)

    def update_table(self, is_show_line=lambda x: True):
        update_table(stock_path, self.root.StockTable, is_show_line)

    def add(self, product: ProductInfo, mark: MarkInfo, container: ContainerInfo, count):
        writer = open_csv_file(stock_path)

        if not find_finish_product_in_csv(product):
            writer.append(
                {"name": product.name, "container_volume": product.container_volume, "mark": mark.name,
                 "container": container.name, "count": 0,
                 "cost": get_cost_finally_product(FinallyProduct(product, mark, container)),
                 "volume": 0})

        writer = sorted(writer, key=lambda x: (x['name'], float(x['container_volume'])))

        with open(stock_path, "w") as f:
            write = csv.DictWriter(f, fieldnames=["name", "container_volume", "mark", "container", "count", "cost",
                                                  "volume"])
            write.writeheader()
            for line in writer:
                p = ProductInfo(line["name"], float(line["container_volume"]), None)
                m = MarkInfo(line["mark"], float(line["container_volume"]))
                c = ContainerInfo(line["container"], float(line["container_volume"]))
                line["volume"] = float(line["count"]) * float(line["container_volume"])
                if line['name'] == product.name and float(line["container_volume"]) == float(product.container_volume):
                    line["count"] = str(float(line['count']) + float(count))
                    line["volume"] = float(line["count"]) * float(line["container_volume"])
                    line["cost"] = get_cost_finally_product(FinallyProduct(p, m, c))
                write.writerow(line)

    def minus(self, product: ProductInfo, mark: MarkInfo, count):
        if not find_finish_product_in_csv(product):
            raise StockEx("нет продукта на складе")
        self.add(product, mark, -count)

    def update_cost_product(self):
        writer = open_csv_file(stock_path)
        with open(stock_path, 'w') as f:
            w = csv.DictWriter(f, fieldnames=["name", "container_volume", "mark", "container", "count", "cost", "volume"])
            w.writeheader()
            for line in writer:
                product = ProductInfo(line["name"], float(line["container_volume"]), None)
                mark = MarkInfo(line["mark"], float(line["container_volume"]))
                container = ContainerInfo(line["container"], float(line["container_volume"]))
                line["cost"] = get_cost_finally_product(FinallyProduct(product, mark, container))
                w.writerow(line)
