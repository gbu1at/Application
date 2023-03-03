from FUNC.function_mark import *
from PyQt5 import uic


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
                uic.loadUi("UI/form_mark_add.ui", other)
                other.initUI()

            def initUI(other):
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
        update_mark_sum_cost()
        update_table(mark_path, self.root.MarkTable, is_show_line)

    def update_excel(self):
        write_to_excel(mark_excel_path, data_mark_processing_for_excel())

    def add(self, mark: MarkInfo, count: float):
        if not find_mark_json(mark):
            add_mark_json(mark)
        plus_mark_count_json(mark, count)

    def reboot_csv(self):
        with open(mark_json_path, 'r') as f:
            data = json.load(f)
        with open(mark_path, "w") as f:
            write = csv.DictWriter(f, fieldnames=list(data["mark"]["container volume"].keys()))
            write.writeheader()
            for mark in data:
                if mark == "mark":
                    continue
                for volume in data[mark]:
                    line = data[mark][volume]
                    write.writerow(line)
        self.update_table()

    def minus(self, mark: MarkInfo, count: float):
        if not find_mark_json(mark):
            raise MarkEx("нет такой этикетки")
        self.add(mark, -count)
