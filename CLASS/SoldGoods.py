from FUNC.functions import *
from FUNC.function_sold_product import *
from SETTING import *
import csv


class SoldGoods():
    def __init__(self, root):
        self.root = root
        self.initUI()

    def setting_btn(self):
        ...

    def initUI(self):
        self.setting_btn()
        self.update_table()

    def update_table(self, is_show_line=lambda x: True):
        update_table(sold_goods_path, self.root.SoldGoodsTable, is_show_line)

    def update_excel(self):
        write_to_excel(sold_goods_excel_path, data_sold_goods_processing_for_excel())

    def add(self, product: FinallyProduct, count, price):
        if not find_sold_goods_json(product):
            add_sold_goods_json(product)
        plus_count_sold_goods(product, count, price)
        self.reboot_csv()

    def reboot_csv(self):
        data = read_json(sold_goods_json_path)

        with open(sold_goods_path, "w") as f:
            write = csv.DictWriter(f, fieldnames=list(data["product"]["container&mark"]["volume"]))
            write.writeheader()
            rows = data_sold_goods_to_csv()
            write.writerows(rows)

        self.update_table()
