import gdown
from PyQt5 import uic, QtWidgets
from newmain import MainCycle, download_cfg


Form, _ = uic.loadUiType("Interface.ui")


# creating parameters preview after loading a file
def create_preview(filename: str):
    file_array = []
    with open(f"/Users/admin/Desktop/LidEmulator/{filename}", "r") as urls:
        for url in urls:
            file_array.append(url.strip())
    params = file_array[0].split()
    params_string = f"Время работы с {params[0]} до {params[1]} часов\n" \
                    f"Количество обрабатываемых сайтов {params[2]}%\n" \
                    f"Количество повторных посещений {params[3]}\n" \
                    f"Время нахождения на странице от {params[4]} до {params[5]} минут\n" \
                    f"Количество страниц перехода от {params[6]} до {params[7]}\n" \
                    f"ID робота {params[8]}\n" \
                    f"Переход по рекламным баннерам {params[9]}\n" \
                    f"Эмуляция ссылок поисковиков {params[10]}\n" \
                    f"\n" \
                    f"Ссылки:"
    file_array[0] = params_string
    return file_array



# Creating and showing pop-up window with some notification
def NotificationWindow(text: str):
    error = QtWidgets.QMessageBox()
    error.setWindowTitle("Ошибка")
    error.setText(text)
    error.setIcon(QtWidgets.QMessageBox.Warning)
    error.setStandardButtons(QtWidgets.QMessageBox.Ok)
    error.exec_()

# Application class
class Ui(QtWidgets.QDialog, Form):
    def __init__(self):
        super(Ui, self).__init__()
        self.setupUi(self)
        self.pushButton_start.clicked.connect(self.start)
        self.pushButton_load.clicked.connect(self.load_config)
        self.isfileFlag = False
        self.robot_id = ''
        self.cfg_link = ''

        # Looking for a log file. If it exists - it means that something interrupted robot in previous session
        # and so now it can continue
        try:
            file = open('log.txt', 'r')
        except Exception as ex:
            pass
        else:
            with file:
                self.robot_id = file.readline().split()[0]
            self.isfileFlag = True
            self.start()

    # pressing start button
    def start(self):
        if self.isfileFlag:
            main_cycle = MainCycle(self.robot_id, self.cfg_link)
            main_cycle.main()
        else:
            err_text = 'Ошибка. Файл еще не был загружен.'
            NotificationWindow(err_text)

    # pressing load button
    def load_config(self):
        self.listWidget.clear()
        self.cfg_link = self.textEdit.toPlainText()
        self.robot_id = self.textEdit_id.toPlainText()
        try:
            # downloading config file
            download_cfg(self.cfg_link)
            self.isfileFlag = True
            # showing config file in the left window
            preview_array = create_preview(f"url_{self.robot_id}.txt")
            for line in preview_array:
                item = QtWidgets.QListWidgetItem()
                item.setText(line)
                self.listWidget.addItem(item)
            self.setWindowTitle(f"Robot {self.robot_id}")
            mess_text = 'Файл успешно загружен.'
            NotificationWindow(mess_text)
        except:
            err_text = 'Ошибка. Проверьте введенную ссылку или ID робота.'
            NotificationWindow(err_text)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = Ui()
    w.show()
    sys.exit(app.exec_())


