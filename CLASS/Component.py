import json

from SETTING import *
from functions import *
import csv


class Component:
    def __init__(self, root, win):
        self.root = root
        self.win = win
        self.initUI()

    def setting_btn(self):
        self.root.btn_find_component.clicked.connect(self.click_btn_find_component)
        self.root.radio_btn_lack_components.toggled.connect(self.click_radio_btn_lack_components)
        self.root.btn_add_component.clicked.connect(self.click_btn_add_component)
        self.root.btn_add_new_component.clicked.connect(self.click_btn_add_new_component)
        self.root.btn_set_cost_component.clicked.connect(self.click_btn_set_cost_component)

    def initUI(self):
        self.setting_btn()
        self.update_table()

    def click_btn_set_cost_component(self):
        ...

    def click_btn_find_component(self):
        component = self.root.edit_find_component.text()
        if component == "":
            self.update_table()
        else:
            self.update_table(lambda x: x['name'] == component)

    def click_radio_btn_lack_components(self):
        if self.root.radio_btn_lack_components.isChecked():
            self.update_table(is_show_line=lambda x: float(x['mass']) < float(x['min_mass']))
        else:
            self.update_table()

    def click_btn_add_new_component(self):
        class Form(QWidget):
            def __init__(other):
                super().__init__()
                other.width = 170
                other.height = 280
                other.initUI()

            def initUI(other):
                other.setGeometry(100, 100, other.height, other.width)
                name = QLabel("название компонента", other)
                other.edit_name = QLineEdit(other)
                name.move(10, 10)
                other.edit_name.move(140, 10)

                min_mass = QLabel("минимальная масса", other)
                other.edit_mass = QLineEdit(other)

                min_mass.move(10, 50)
                other.edit_mass.move(140, 50)

                cost = QLabel("рыночная цена за кг", other)
                other.edit_cost = QLineEdit(other)

                cost.move(10, 90)
                other.edit_cost.move(140, 90)

                other.btnOK = QPushButton("Apply", other)
                other.btnOK.move(10, 140)
                other.btnExit = QPushButton("Exit", other)
                other.btnExit.move(110, 140)

                other.setting_btn()

            def setting_btn(other):
                other.btnOK.clicked.connect(other.click_btnOK)
                other.btnExit.clicked.connect(other.click_btnExit)

            def click_btnOK(other):
                try:
                    name = other.edit_name.text()
                    min_mass = float(other.edit_mass.text())
                    cost = float(other.edit_cost.text())
                except Exception as ex:
                    print("некорректые данные")
                    return

                if find_component_json(name):
                    return
                set_cost_component(name, cost)
                set_cost(self.root)
                try:
                    self.add_new(name, min_mass, cost)
                    self.update_table()
                    other.close()
                except Exception as ex:
                    print(ex)

            def click_btnExit(other):
                other.close()

        self.form = Form()
        self.form.show()

    def click_btn_add_component(self):
        class Form(QWidget):
            def __init__(other):
                super().__init__()
                other.width = 170
                other.height = 280
                other.initUI()

            def initUI(other):
                other.setGeometry(100, 100, other.height, other.width)
                name = QLabel("название компонента", other)
                other.edit_name = QLineEdit(other)
                name.move(10, 10)
                other.edit_name.move(140, 10)

                mass = QLabel("масса", other)
                other.edit_mass = QLineEdit(other)

                mass.move(10, 50)
                other.edit_mass.move(140, 50)

                cost = QLabel("цена за кг", other)
                other.edit_cost = QLineEdit(other)

                cost.move(10, 90)
                other.edit_cost.move(140, 90)

                other.btnOK = QPushButton("Apply", other)
                other.btnOK.move(10, 140)
                other.btnExit = QPushButton("Exit", other)
                other.btnExit.move(110, 140)

                other.setting_btn()

            def setting_btn(other):
                other.btnOK.clicked.connect(other.click_btnOK)
                other.btnExit.clicked.connect(other.click_btnExit)

            def click_btnOK(other):
                try:
                    name = other.edit_name.text()
                    mass = float(other.edit_mass.text())
                    cost = float(other.edit_cost.text())
                except Exception as ex:
                    print("некорректные данные")
                    return
                if not find_component_json(name):
                    return
                set_cost_component(name, cost)
                set_cost(self.root)
                try:
                    self.add(name, mass)
                    self.update_table()
                    other.close()
                except Exception as ex:
                    print(ex)

            def click_btnExit(other):
                other.close()

        self.form = Form()
        self.form.show()

    def update_table(self, is_show_line=lambda x: True):
        update_table(comp_path, self.root.ComponentTable, is_show_line)

    def minus(self, component, mass):
        """
        :param component: компонент
        :param mass: масса компонента
        :return:
        """
        # открываем файл и записываем его содержимое в writer
        writer = open_csv_file(comp_path)

        # закрываем файл и у соответ. компонента вычтаем массу

        with open(comp_path, 'w') as f:
            w = csv.DictWriter(f, fieldnames=['name', 'mass', 'min_mass', 'cost'])
            w.writeheader()
            is_change = False
            for line in writer:
                line['cost'] = get_cost_component(line['name'])
                if line['name'] == component:
                    line['mass'] = str(float(line['mass']) - mass)
                    is_change = True
                w.writerow(line)
            if not is_change:
                raise ComponentEx("компонент не найден")

    def add(self, component, mass):
        self.minus(component, -float(mass))

    def add_new(self, component, min_mass, cost):
        writer = open_csv_file(comp_path)
        writer.append({"name": component, "mass": 0, "min_mass": min_mass, "cost": cost})
        writer = sorted(writer, key=lambda x: x['name'])
        with open(comp_path, 'w') as f:
            w = csv.DictWriter(f, fieldnames=['name', 'mass', 'min_mass', "cost"])
            w.writeheader()
            for line in writer:
                w.writerow(line)

    def find(self, component):
        with open(comp_json_path, 'r') as f:
            data = json.load(f)
        return component in data
