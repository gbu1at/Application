from FUNC.function_container import *
from FUNC.functions import *
from SETTING import *
from PyQt5 import uic


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
        self.root.btn_del_container.clicked.connect(self.click_btn_del_container)

    def click_btn_find_container(self):
        name = self.root.edit_find_container.text()
        self.update_table(lambda x: name in x["name"])

    def click_btn_add_container(self):
        class Form(QWidget):
            def __init__(other):
                super().__init__()
                uic.loadUi("UI/form_container_add.ui", other)
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
                self.add(ContainerInfo(name, container_volume), count)
                set_cost_container(ContainerInfo(name, container_volume), cost)
                self.reboot_csv()
                other.close()

            def click_btnExit(other):
                other.close()

        self.form = Form()
        self.form.show()

    def update_table(self, is_show_line=lambda x: True):
        update_container_sum_cost()
        update_table(container_path, self.root.ContainerTable, is_show_line)

    def update_excel(self):
        write_to_excel(container_excel_path, data_container_processing_for_excel())

    def add(self, container: ContainerInfo, count):
        if not find_container_json(container):
            add_container_json(container)
        plus_container_count_json(container, count)
        self.reboot_csv()

    def click_btn_del_container(self):
        name = self.root.edit_del_container_name.text()
        volume = self.root.edit_del_container_volume.text()
        cnt = ContainerInfo(name, volume)
        if not find_container_json(cnt):
            return
        del_container_json(cnt)
        self.reboot_csv()

    def reboot_csv(self):
        with open(container_json_path, 'r') as f:
            data = json.load(f)
        with open(container_path, 'w') as f:
            write = csv.DictWriter(f, fieldnames=list(data["container"]["volume"].keys()))
            write.writeheader()
            for container in data:
                if container == "container":
                    continue
                row = {}
                for volume in data[container]:
                    line = data[container][volume]
                    write.writerow(line)
        self.update_table()

    def minus(self, container: ContainerInfo, count):
        if not find_container_json(container):
            raise ContainerEx("тара не найдена")
        self.add(container, -count)
