from FUNC.function_component import *
from PyQt5 import uic
import csv


class Component:
    def __init__(self, root):
        self.root = root
        self.initUI()

    def setting_btn(self):
        self.root.btn_find_component.clicked.connect(self.click_btn_find_component)
        self.root.radio_btn_lack_components.toggled.connect(self.click_radio_btn_lack_components)
        self.root.btn_add_component.clicked.connect(self.click_btn_add_component)
        self.root.btn_del_component.clicked.connect(self.click_btn_del_component)

    def initUI(self):
        self.setting_btn()
        self.update_table()

    def click_btn_find_component(self):
        component = self.root.edit_find_component.text()
        if component == "":
            self.update_table()
        else:
            self.update_table(lambda x: component in x['name'])

    def click_radio_btn_lack_components(self):
        if self.root.radio_btn_lack_components.isChecked():
            self.update_table(is_show_line=lambda x: float(x['mass']) < float(x['min_mass']))
        else:
            self.update_table()

    def click_btn_add_component(self):
        class Form(QWidget):
            def __init__(other):
                super().__init__()
                uic.loadUi("./UI/form_component_add.ui", other)
                other.initUI()

            def initUI(other):
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
        del_component_json(text)
        self.reboot_csv()

    def update_table(self, is_show_line=lambda x: True):
        update_component_sum_cost()
        update_table(comp_path, self.root.ComponentTable, is_show_line)

    def update_excel(self):
        write_to_excel(comp_excel_path, data_component_processing_for_excel())

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
            rows = data_component_to_csv()
            w.writerows(rows)
        self.update_table()

    def minus(self, component, mass):
        if not find_component_json(component):
            return
        self.add(component, -float(mass))

    def find(self, component):
        with open(comp_json_path, 'r') as f:
            data = json.load(f)
        return component in data
