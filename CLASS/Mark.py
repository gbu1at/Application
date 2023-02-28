import json

from functions import *
from SETTING import *
import csv
from function_mark import *


class Mark:
    def __init__(self, root):
        self.root = root
        self.initUI()

    def setting_btn(self):
        self.root.btn_find_mark.clicked.connect(self.click_btn_find_mark)
        self.root.btn_add_mark.clicked.connect(self.click_btn_add_mark)
        self.root.btn_del_mark.clicked.connect(self.click_btn_del_mark)

    def initUI(self):
        self.setting_btn()
        self.update_table()

    def click_btn_find_mark(self):
        mark = self.root.edit_find_mark.text()
        if mark == "":
            self.update_table()
        else:
            self.update_table(is_show_line=lambda x: mark in x['name'])

    def click_btn_add_mark(self):
        class Form(QWidget):
            def __init__(other):
                super().__init__()
                other.width = 210
                other.height = 280
                other.initUI()

            def initUI(other):
                other.setGeometry(100, 100, other.height, other.width)
                name = QLabel("название этикетки", other)
                other.edit_name = QLineEdit(other)
                name.move(10, 10)
                other.edit_name.move(140, 10)

                count = QLabel("кол-во", other)
                other.edit_count = QLineEdit(other)

                count.move(10, 50)
                other.edit_count.move(140, 50)

                container_volume = QLabel("объем", other)
                other.edit_container_volume = QLineEdit(other)

                container_volume.move(10, 90)
                other.edit_container_volume.move(140, 90)

                cost = QLabel("стоимость штуки", other)
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
                name = other.edit_name.text()
                try:
                    count = float(other.edit_count.text())
                    cost = float(other.edit_cost.text())
                    container_volume = float(other.edit_container_volume.text())
                except ValueError as ex:
                    print("некорректные данные")
                    return
                self.add(MarkInfo(name, container_volume), count)
                set_cost_mark(MarkInfo(name, container_volume), cost)
                self.reboot_csv()
                other.close()

            def click_btnExit(other):
                other.close()

        self.form = Form()
        self.form.show()

    def click_btn_del_mark(self):
        name = self.root.edit_del_mark_name.text()
        volume = self.root.edit_del_mark_volume.text()
        mark = MarkInfo(name, volume)
        if not find_mark_json(mark):
            return
        del_mark_json(mark)
        self.reboot_csv()

    def update_table(self, is_show_line=lambda x: True):
        update_table(mark_path, self.root.MarkTable, is_show_line)

    def add(self, mark: MarkInfo, count: float):
        if not find_mark_json(mark):
            add_mark_json(mark)
        plus_mark_count_json(mark, count)

    def reboot_csv(self):
        with open(mark_json_path, 'r') as f:
            data = json.load(f)
        with open(mark_path, "w") as f:
            write = csv.DictWriter(f, fieldnames=["name", "container volume", "count", "cost"])
            write.writeheader()
            for mark in data:
                if mark == "mark":
                    continue
                for volume in data[mark]:
                    line = data[mark][volume]
                    row = {"name": line["name"], "container volume": line["volume"], "count": line["count"],
                           "cost": line["cost"]}
                    write.writerow(row)
        self.update_table()

    def minus(self, mark: MarkInfo, count: float):
        if not find_mark_json(mark):
            raise MarkEx("нет такой этикетки")
        self.add(mark, -count)
