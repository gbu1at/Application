from FUNC.function_product import *
from SETTING import *


class Product:
    def __init__(self, root):
        self.root = root
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
            self.update_table(is_show_line=lambda x: product in x['name'])

    def update_table(self, is_show_line=lambda x: True):
        update_product_sum_cost()
        update_table(product_path, self.root.ProductTable, is_show_line)

    def update_excel(self):
        write_to_excel(product_excel_path, data_product_processing_for_excel())

    def add(self, product, mass):
        if not find_product_json(product):
            add_product_json(product)
        plus_product_mass_json(product, mass)

    def reboot_csv(self):
        self.update_cost_product()
        with open(product_path, 'w') as f:
            w = csv.DictWriter(f, fieldnames=['name', 'mass', 'cost', "sum cost"])
            w.writeheader()
            rows = data_product_to_csv()
            w.writerows(rows)
        self.update_table()

    def update_cost_product(self):
        with open(product_json_path) as f:
            data = json.load(f)

        for product in data:
            if product == "product": continue
            update_cost_product(product)

    def minus(self, product, mass):
        if not find_product_json(product):
            raise Exception("нет продукта")
        self.add(product, -mass)

    def find(self, product):
        with open(product_json_path) as f:
            data = json.load(f)
        if product in data:
            return data[product]
        return None
