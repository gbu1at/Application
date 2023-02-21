import csv

from functions import *
from SETTING import *


class Container:
    def __init__(self, root):
        self.root = root
        self.initUI()
        self.update_table()

    def initUI(self):
        self.setting_btn()

    def setting_btn(self):
        self.root.btn_find_container.clicked.connect(self.click_btn_find_container)
        self.root.btn_add_container.clicked.connect(self.click_btn_add_container)
        self.root.btn_add_new_container.clicked.connect(self.click_btn_add_new_container)

    def click_btn_find_container(self):
        name = self.root.edit_find_container.text()
        self.update_table(lambda x: x["name"] == name)

    def click_btn_add_container(self):
        class Form(QWidget):
            def __init__(other):
                super().__init__()
                other.width = 210
                other.height = 280
                other.initUI()

            def initUI(other):
                other.setGeometry(100, 100, other.height, other.width)
                name = QLabel("название тары", other)
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
                try:
                    set_cost_container(ContainerInfo(name, container_volume), cost)
                    self.add(ContainerInfo(name, container_volume), count)
                    self.update_table()
                    other.close()
                except Exception as ex:
                    print(ex)

            def click_btnExit(other):
                other.close()

        self.form = Form()
        self.form.show()

    def click_btn_add_new_container(self):
        ...

    def update_table(self, is_show_line=lambda x: True):
        update_table(container_path, self.root.ContainerTable, is_show_line)

    def add(self, container: ContainerInfo, count):
        writer = open_csv_file(container_path)

        if not find_container_in_csv(container):
            writer.append(
                {"name": container.name, "volume": container.volume, "count": 0, "cost": get_cost_container(container)}
            )

        writer = sorted(writer, key=lambda x: (x['name'], float(x['volume'])))

        with open(container_path, 'w') as f:
            write = csv.DictWriter(f, fieldnames=["name", "volume", "count", "cost"])
            write.writeheader()
            for line in writer:
                line["cost"] = get_cost_container(ContainerInfo(line["name"], float(line["volume"])))
                if line["name"] == container.name and float(line["volume"]) == float(container.volume):
                    line["count"] = float(line["count"]) + count
                write.writerow(line)

    def minus(self, container: ContainerInfo, count):
        if not find_container_in_csv(container):
            raise ContainerEx("тара не найдена")
        self.add(container, -count)
