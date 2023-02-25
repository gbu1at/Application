import json

from SETTING import *
from functions import *
from function_component import *
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
        self.root.btn_set_cost_component.clicked.connect(self.click_btn_set_cost_component)
        self.root.btn_del_component.clicked.connect(self.click_btn_del_component)

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

                min_mass = QLabel("минимальная масса", other)
                other.edit_min_mass = QLineEdit(other)

                min_mass.move(10, 90)
                other.edit_min_mass.move(140, 90)

                cost = QLabel("цена за кг", other)
                other.edit_cost = QLineEdit(other)

                cost.move(10, 130)
                other.edit_cost.move(140, 130)

                other.btnOK = QPushButton("Apply", other)
                other.btnOK.move(10, 180)
                other.btnExit = QPushButton("Exit", other)
                other.btnExit.move(110, 180)

                other.setting_btn()

            def setting_btn(other):
                other.btnOK.clicked.connect(other.click_btnOK)
                other.btnExit.clicked.connect(other.click_btnExit)

            def click_btnOK(other):
                try:
                    name = other.edit_name.text()
                    mass = float(other.edit_mass.text())
                    min_mass = float(other.edit_min_mass.text())
                    cost = float(other.edit_cost.text())
                except Exception as ex:
                    print("некорректные данные")
                    return
                self.add(name, mass, min_mass)
                set_cost_component(name, cost)
                # set_cost(self.root)
                self.reboot_csv()
                other.close()

            def click_btnExit(other):
                other.close()

        self.form = Form()
        self.form.show()

    def click_btn_del_component(self):
        text = self.root.edit_del_component.text()
        if not find_component_json(text):
            return
        del_component(text)
        self.reboot_csv()

    def update_table(self, is_show_line=lambda x: True):
        update_table(comp_path, self.root.ComponentTable, is_show_line)

    def add(self, component, mass, min_mass=None):
        if not find_component_json(component):
            comp_json_add(component)

        comp_json_add_mass(component, mass, min_mass)
        self.reboot_csv()

    def reboot_csv(self):
        with open(comp_json_path, 'r') as f:
            data = json.load(f)

        with open(comp_path, 'w') as f:
            w = csv.DictWriter(f, fieldnames=list(data["component"]))
            w.writeheader()
            for component in data:
                if component == "component":
                    continue
                row = {}
                for col in data[component]:
                    row[col] = data[component][col]
                w.writerow(row)
        self.update_table()

    def minus(self, component, mass):
        if not find_component_json(component):
            return
        self.add(component, -float(mass))

    def find(self, component):
        with open(comp_json_path, 'r') as f:
            data = json.load(f)
        return component in data
