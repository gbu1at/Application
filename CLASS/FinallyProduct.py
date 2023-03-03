from FUNC.function_finally_product import *
from SETTING import *
import csv


class FinallyProducts():
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
        update_finally_product_sum_cost()
        update_table(stock_path, self.root.StockTable, is_show_line)

    def update_excel(self):
        write_to_excel(stock_excel_path, data_finally_product_processing_for_excel())

    def add(self, product: FinallyProduct, count):
        if not find_finally_product_json(product):
            add_finally_product_json(product)
        plus_count_finally_product(product, count)
        self.reboot_csv()

    def reboot_csv(self):
        data = read_json(finally_product_json_path)

        with open(stock_path, "w") as f:
            write = csv.DictWriter(f, fieldnames=list(data["product"]["container&mark"]["volume"]))
            write.writeheader()
            rows = data_finally_product_to_csv()
            write.writerows(rows)

        self.update_table()

    def minus(self, product: FinallyProduct, count):
        if not find_finally_product_json(product):
            raise StockEx("нет продукта на складе")
        self.add(product, -count)
