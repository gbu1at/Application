from PyQt5 import uic
from CLASS.Component import Component
from CLASS.Product import Product
from CLASS.Mark import Mark
from CLASS.FinishProduct import FinishedProducts
from CLASS.DirtyStock import DirtyStock
from CLASS.SoldGoods import SoldGoods
from CLASS.Container import Container
from functions import *
import json
import sys


class Application(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.COMPONENT = Component(self, self.tab)
        self.PRODUCT = Product(self, self.tab_2)
        self.DIRTYSTOCK = DirtyStock(self)
        self.STOCK = FinishedProducts(self)
        self.MARK = Mark(self)
        self.SOLDGOODS = SoldGoods(self)
        self.CONTAINER = Container(self)
        self.initUI()

    def setting_btn(self):
        self.btn_component__product.clicked.connect(self.click_component__product)
        self.btn_product__dirtystock.clicked.connect(self.click_product__dirtystock)
        self.btn_dirtystock__stock.clicked.connect(self.click_dirtystock__stock)
        self.btn_sold.clicked.connect(self.click_sold)
        self.btn_update.clicked.connect(lambda: update(self))

    def click_component__product(self):
        class FunctionComponent__Product(QWidget):
            def __init__(other):
                super().__init__()
                other.width = 500
                other.height = 400
                other.initUI()

            def initUI(other):
                other.setGeometry(100, 100, other.height, other.width)
                other.btnOK = QPushButton("Apply", other)
                other.btnOK.move(10, 430)
                other.btnExit = QPushButton("Exit", other)
                other.btnExit.move(110, 430)
                other.btnOK.clicked.connect(other.btnOK_click)
                other.btnExit.clicked.connect(other.btnExit_click)

                other.product_edit = QLineEdit(other)
                label_product = QLabel("продкут", other)
                label_product.move(10, 20)
                other.product_edit.move(110, 20)

                label_mass = QLabel("масса", other)
                label_mass.move(10, 100)
                other.mass_edit = QLineEdit(other)
                other.mass_edit.move(110, 100)

                other.radio_btn = QRadioButton("новая рецептура", other)
                other.recipe_text = QTextEdit(other)
                other.recipe_text.resize(350, 100)
                other.recipe_text.move(10, 150)
                other.radio_btn.move(10, 130)

                other.old_radio_btn = QRadioButton("старая рецептура", other)
                other.old_recipe_text = QTextBrowser(other)
                other.old_recipe_text.resize(350, 100)
                other.old_recipe_text.move(10, 300)
                other.old_radio_btn.move(10, 280)

                other.old_radio_btn.toggled.connect(other.click_old_radio_btn)

            def click_old_radio_btn(other):
                product = other.product_edit.text()
                recipe = self.PRODUCT.find(product)
                if recipe == None:
                    ...
                else:
                    text = ""
                    for comp in recipe:
                        text += f"{comp}={recipe[comp]};\n"
                    other.old_recipe_text.setText(text)

            def btnOK_click(other):
                try:
                    product = other.product_edit.text()
                    try:
                        mass = float(other.mass_edit.text())
                    except Exception as ex:
                        print("некорректная масса")
                        return
                    recipe = None
                    if other.radio_btn.isChecked():
                        recipe = {}
                        text = other.recipe_text.toPlainText()
                        text = text.split(";\n")
                        for line in text:
                            if line == "": continue
                            data = line.split("=")
                            comp, percent = data[0], data[1]
                            comp = comp.strip()
                            percent = percent.strip()
                            recipe[comp] = float(percent)
                    elif other.old_radio_btn.isChecked():
                        recipe = self.PRODUCT.find(product)
                        if recipe == None:
                            raise Exception
                    else:
                        raise Exception
                except Exception as ex:
                    print(ex)
                    return
                try:
                    self.component__product(product=product, mass=mass, recipe=recipe)
                    other.close()
                except Exception as ex:
                    print(ex)

            def btnExit_click(other):
                other.close()

        self.func = FunctionComponent__Product()
        self.func.show()

    def click_product__dirtystock(self):
        class FunctionProduct__Dirtystock(QWidget):
            def __init__(other):
                super().__init__()
                other.width = 280
                other.height = 280
                other.initUI()

            def initUI(other):
                other.setGeometry(100, 100, other.height, other.width)
                other.btnOK = QPushButton("Apply", other)
                other.btnOK.move(10, 240)
                other.btnExit = QPushButton("Exit", other)
                other.btnExit.move(110, 240)
                other.btnOK.clicked.connect(other.btnOK_click)
                other.btnExit.clicked.connect(other.btnExit_click)

                other.product_edit = QLineEdit(other)
                label_product = QLabel("продкут", other)
                label_product.move(10, 20)
                other.product_edit.move(110, 20)

                label_container_volume = QLabel("объем тары", other)
                label_container_volume.move(10, 100)
                other.container_volume_edit = QLineEdit(other)
                other.container_volume_edit.move(110, 100)

                label_count = QLabel("кол-во тары", other)
                label_count.move(10, 180)
                other.count = QLineEdit(other)
                other.count.move(110, 180)

            def btnOK_click(other):
                product = other.product_edit.text()
                try:
                    container_volume = float(other.container_volume_edit.text())
                    count = float(other.count.text())
                except ValueError as ex:
                    print("некорректные данные")
                    return
                try:
                    self.product__dirtystock(product=product, count=count, container_volume=container_volume)
                    other.close()
                except Exception as ex:
                    print(ex)

            def btnExit_click(other):
                other.close()

        self.func = FunctionProduct__Dirtystock()
        self.func.show()

    def click_dirtystock__stock(self):
        class FunctionDirtyStock__Stock(QWidget):
            def __init__(other):
                super().__init__()
                other.height = 400
                other.width = 440
                other.initUI()

            def initUI(other):
                other.setGeometry(100, 100, other.height, other.width)

                other.product_edit = QLineEdit(other)
                label_product = QLabel("продкут", other)
                label_product.move(10, 20)
                other.product_edit.move(110, 20)

                label_container_volume = QLabel("объем тары", other)
                label_container_volume.move(10, 100)
                other.container_volume_edit = QLineEdit(other)
                other.container_volume_edit.move(110, 100)

                label_count = QLabel("кол-во тары", other)
                label_count.move(10, 180)
                other.count = QLineEdit(other)
                other.count.move(110, 180)

                label_container_name = QLabel("название тары", other)
                label_container_name.move(10, 260)
                other.container_name_edit = QLineEdit(other)
                other.container_name_edit.move(110, 260)

                label_mark = QLabel("этикетка", other)
                label_mark.move(10, 340)
                other.mark_edit = QLineEdit(other)
                other.mark_edit.move(110, 340)

                other.btnOK = QPushButton("Apply", other)
                other.btnOK.move(10, 400)
                other.btnExit = QPushButton("Exit", other)
                other.btnExit.move(110, 400)

                other.setting_btn()

            def setting_btn(other):
                other.btnOK.clicked.connect(other.click_btnOK)
                other.btnExit.clicked.connect(other.click_btnExit)

            def click_btnOK(other):
                product = other.product_edit.text()
                mark = other.mark_edit.text()
                container_name = other.container_name_edit.text()
                try:
                    container_volume = float(other.container_volume_edit.text())
                    count = float(other.count.text())
                except ValueError as ex:
                    print("некорректные данные")
                    return

                try:
                    m = MarkInfo(mark, container_volume)
                    p = ProductInfo(product, container_volume, None)
                    c = ContainerInfo(container_name, container_volume)
                    self.dirtystock__stock(p, m, c, count)
                    other.close()
                except Exception as ex:
                    print(ex)

            def click_btnExit(other):
                other.close()

        self.func = FunctionDirtyStock__Stock()
        self.func.show()

    def click_sold(self):
        class FunctionStock__SoldGoods(QWidget):
            def __init__(other):
                super().__init__()
                other.height = 400
                other.width = 440
                other.initUI()

            def initUI(other):
                other.setGeometry(100, 100, other.height, other.width)
                other.btnOK = QPushButton("Apply", other)
                other.btnOK.move(10, 400)
                other.btnExit = QPushButton("Exit", other)
                other.btnExit.move(110, 400)

                other.product_edit = QLineEdit(other)
                label_product = QLabel("продкут", other)
                label_product.move(10, 20)
                other.product_edit.move(110, 20)

                label_container_volume = QLabel("объем тары", other)
                label_container_volume.move(10, 100)
                other.container_volume_edit = QLineEdit(other)
                other.container_volume_edit.move(110, 100)

                label_count = QLabel("кол-во тары", other)
                label_count.move(10, 180)
                other.count = QLineEdit(other)
                other.count.move(110, 180)

                label_cost = QLabel("стоимость штуки", other)
                label_cost.move(10, 260)
                other.cost_edit = QLineEdit(other)
                other.cost_edit.move(110, 260)

                label_price = QLabel("цена за штуку", other)
                label_price.move(10, 340)
                other.price_edit = QLineEdit(other)
                other.price_edit.move(110, 340)

                other.setting_btn()

            def setting_btn(other):
                other.btnOK.clicked.connect(other.click_btnOK)
                other.btnExit.clicked.connect(other.click_btnExit)

            def click_btnOK(other):
                product = other.product_edit.text()
                container_volume = float(other.container_volume_edit.text())
                count = float(other.count.text())
                cost = float(other.cost_edit.text())
                price = float(other.price_edit.text())
                try:
                    self.stock__soldgoods(product=product, count=count, cost=cost, container_volume=container_volume,
                                          price=price)
                    other.close()
                except Exception as ex:
                    print(ex)

            def click_btnExit(other):
                other.close()

        self.func = FunctionStock__SoldGoods()
        self.func.show()

    def initUI(self):
        self.setting_btn()

    def component__product(self, product: str, mass: float, recipe=None):
        """
            :param product: продукция
            :param mass: масса
            :param recipe: рецептура, по которой нужно приготовить продукт
            :return:
        """

        with open(product_json_path, 'r') as f:
            data_json = json.load(f)

        if not self.PRODUCT.find(product):
            set_recipe(product, recipe)

        if recipe is None:
            recipe = data_json[product]
        for comp in recipe:
            if not self.COMPONENT.find(comp):
                raise Exception("некорректный рецепт, компонент не найден")
        try:
            self.PRODUCT.add(product, mass)  # добавляем массу продукта к готовым продуктам
        except Exception as ex:
            raise ex
        for comp in recipe:
            # recipe[comp] - процентное соотношение
            minus_mass = recipe[comp] * mass / 100
            self.COMPONENT.minus(comp, minus_mass)  # вычитаем из таблицы компонент соответствующую массу

        self.COMPONENT.update_table()
        self.PRODUCT.update_table()

    def product__dirtystock(self, product: str, count: float, container_volume: float):
        """
            :param product: продукция
            :param count: кол-во продукции
            :param container_volume: объем тары
            :return:
        """
        mass = count * container_volume
        if self.PRODUCT.find(product) is None:
            raise Exception
        try:
            self.PRODUCT.minus(product, mass)
        except Exception as ex:
            raise ex

        try:
            self.DIRTYSTOCK.add(ProductInfo(name=product, container_volume=container_volume, cost=0), count)
        except Exception as ex:
            self.PRODUCT.add(product, mass)
            raise ex

        self.PRODUCT.update_table()
        self.DIRTYSTOCK.update_table()

    def dirtystock__stock(self, product: ProductInfo, mark: MarkInfo, container: ContainerInfo, count: float):
        try:
            self.DIRTYSTOCK.minus(product, count)
            self.MARK.minus(mark, count)
            self.CONTAINER.minus(container, count)
        except ContainerEx as ex:
            self.MARK.add(mark, count)
            self.DIRTYSTOCK.add(product, count)
            raise ex
        except MarkEx as ex:
            self.DIRTYSTOCK.add(product, count)
            raise ex
        except DirtyStock as ex:
            raise ex

        try:
            self.STOCK.add(product, mark, container, count)
        except Exception as ex:
            self.DIRTYSTOCK.add(product, count)
            self.MARK.add(mark, count)
            raise ex

        self.DIRTYSTOCK.update_table()
        self.MARK.update_table()
        self.CONTAINER.update_table()
        self.STOCK.update_table()

    def stock__soldgoods(self, product, count: float, container_volume: float, cost: float, price: float):
        try:
            p = ProductInfo(product, container_volume, cost)
            self.STOCK.minus(p, count)
            try:
                self.SOLDGOODS.add(p, count, price)
            except Exception as ex:
                self.STOCK.add(p, count)
                raise ex
        except Exception as ex:
            raise ex

        self.SOLDGOODS.update_table()
        self.STOCK.update_table()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Application()
    win.show()
    sys.exit(app.exec())
