from functions import *
from SETTING import *
import csv


class Mark:
    def __init__(self, root):
        self.root = root
        self.initUI()

    def setting_btn(self):
        self.root.btn_find_mark.clicked.connect(self.click_btn_find_mark)
        self.root.btn_add_mark.clicked.connect(self.click_btn_add_mark)

    def initUI(self):
        self.setting_btn()
        self.update_table()

    def click_btn_find_mark(self):
        mark = self.root.edit_find_mark.text()
        if mark == "":
            self.update_table()
        else:
            self.update_table(is_show_line=lambda x: x['name'] == mark)

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
                try:
                    set_cost_mark(MarkInfo(name, container_volume), cost)
                    self.add(MarkInfo(name, container_volume), count)
                    self.update_table()
                    other.close()
                except Exception as ex:
                    print(ex)

            def click_btnExit(other):
                other.close()

        self.form = Form()
        self.form.show()

    def update_table(self, is_show_line=lambda x: True):
        update_table(mark_path, self.root.MarkTable, is_show_line)

    def add(self, mark: MarkInfo, count: float):
        writer = open_csv_file(mark_path)

        if not find_mark_in_csv(mark):
            writer.append({"name": mark.name, "container_volume": mark.container_volume, "count": 0,
                           "cost": get_cost_mark(mark)})

        writer = sorted(writer, key=lambda x: (x['name'], float(x['container_volume'])))

        with open(mark_path, "w") as f:
            write = csv.DictWriter(f, fieldnames=["name", "container_volume", "count", "cost"])
            write.writeheader()
            for line in writer:
                line["cost"] = get_cost_mark(MarkInfo(line["name"], float(line["container_volume"])))
                if line['name'] == mark.name and float(line['container_volume']) == float(mark.container_volume):
                    line["count"] = str(float(line['count']) + float(count))
                write.writerow(line)

    def minus(self, mark: MarkInfo, count: float):
        if not find_mark_in_csv(mark):
            raise MarkEx("нет такой этикетки")
        self.add(mark, -count)
