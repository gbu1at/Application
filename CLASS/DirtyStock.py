from FUNC.function_dirty_stock import *
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
        self.reboot_csv()

    def click_btn_find_product_dirty_stock(self):
        product = self.root.edit_find_product_dirty_stock.text()
        if product == "":
            self.update_table()
        else:
            self.update_table(is_show_line=lambda x: product in x['name'])

    def update_table(self, is_show_line=lambda x: True):
        update_dirtystock_sum_cost()
        update_table(dirtystock_path, self.root.DirtyStockTable, is_show_line)

    def update_excel(self):
        write_to_excel(dirtystock_excel_path, data_dirty_stock_processing_for_excel())

    def add(self, product: ProductInfo, count):
        if not find_dirty_stock_json(product):
            add_dirty_stock_json(product)
        plus_count_dirty_stock_json(product, count)
        update_dirty_stock_product(product)
        self.reboot_csv()

    def reboot_csv(self):
        data = read_json(dirty_stock_json_path)
        with open(dirtystock_path, "w") as f:
            write = csv.DictWriter(f, fieldnames=list(data["product"]["container name"]["container volume"]))
            write.writeheader()
            df = data_dirtystock_to_csv()
            write.writerows(df)
        self.update_table()

    def minus(self, product: ProductInfo, count):
        if not find_dirty_stock_json(product):
            raise DirtyStockEx("на грязном складе нет данной продукции")
        self.add(product, -count)
