from PyQt5.QtWidgets import *


class ComponentEx(Exception):
    ...


class ProductEx(Exception):
    ...


class DirtyStockEx(Exception):
    ...


class StockEx(Exception):
    ...


class MarkEx(Exception):
    ...


class ContainerEx(Exception):
    ...


comp_path = "CSV/component.csv"
product_path = "CSV/poduct.csv"
dirtystock_path = "CSV/dirty_stock.csv"
stock_path = "CSV/stock.csv"
mark_path = "CSV/mark.csv"
container_path = "CSV/container.csv"
sold_goods_path = "CSV/sold_goods.csv"

product_json_path = "JSON/product.json"
comp_json_path = "JSON/components.json"
mark_json_path = "JSON/mark.json"
container_json_path = "JSON/container.json"
dirty_stock_json_path = "JSON/dirty_stock.json"
finally_product_json_path = "JSON/finally_product.json"
