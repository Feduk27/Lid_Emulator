import gdown
from PyQt5 import uic, QtWidgets
from App_ import NotificationWindow
from file_exchange import gdrive_upload

Form, _ = uic.loadUiType("ConfigFile.ui")



# Application class
class Ui(QtWidgets.QDialog, Form):
    def __init__(self):
        super(Ui, self).__init__()
        self.setupUi(self)
        self.pushButton_save.clicked.connect(self.save)

    def save(self):
        no_error_flag = True
        # Checking time range validity
        try:
            time_from, time_to = map(int,(self.textEdit_time_from.toPlainText(), self.textEdit_time_to.toPlainText()))
            if time_from >= time_to or time_to > 23 or time_from > 23:
                message_time = 'Проверьте правильность введенного диапазона времени'
                NotificationWindow(message_time)
        except:
            message_time = 'Проверьте правильность введенного диапазона времени'
            NotificationWindow(message_time)
            no_error_flag = False

        #Checking percentange validity
        try:
            percentage = int(self.textEdit_percentage.toPlainText())
            if percentage > 100:
                message_percentage = 'Проверьте правильность введенного количества обрабатываемых сайтов'
                NotificationWindow(message_percentage)
        except:
            message_percentage = 'Проверьте правильность введенного количества обрабатываемых сайтов'
            NotificationWindow(message_percentage)
            no_error_flag = False

        # Checking repeatability validity
        try:
            repeatability = int(self.textEdit_repeatability.toPlainText())
            if repeatability > 5:
                message_repeatability = 'Количество повторных посещений должно быть в диапазоне от 0 до 5.'
                NotificationWindow(message_repeatability)
        except:
            message_repeatability = 'Проверьте правильность введенного количества повторных посещений'
            NotificationWindow(message_repeatability)
            no_error_flag = False

        # Checking time on website validity
        try:
            time_on_website_from, time_on_website_to = map(int, (self.textEdit_time_on_website_from.toPlainText(), self.textEdit_time_on_website_to.toPlainText()))
            if time_on_website_from >= time_on_website_to or time_on_website_from > 10 or time_on_website_to > 10 or time_on_website_to < 1 or time_on_website_from < 1:
                message_website_time = 'Проверьте диапазон. Время нахождения на странице должно быть в диапазоне от 1 до 10 минут'
                NotificationWindow(message_website_time)
        except:
            message_website_time = 'Проверьте правильность введенного времени нахождения на странице'
            NotificationWindow(message_website_time)
            no_error_flag = False

        # Checking transition amount validity
        try:
            transition_amount_from, transition_amount_to = map(int, (self.textEdit_transition_amount_from.toPlainText(), self.textEdit_transition_amount_to.toPlainText()))
            if transition_amount_from >= transition_amount_to or transition_amount_from not in range(1,6) or transition_amount_to not in range(1,6):
                message_transition_amount = 'Проверьте диапазон.  Количество страниц перехода должно быть от 1 до 5'
                NotificationWindow(message_transition_amount)
        except:
            message_transition_amount = 'Проверьте правильность введенного количества переходов'
            NotificationWindow(message_transition_amount)
            no_error_flag = False

        # Checking robot id validity
        try:
            robot_id = int(self.textEdit_robot_id.toPlainText())
        except:
            message_repeatability = 'Проверьте правильность введенного ID робота. ID должно быть числом.'
            NotificationWindow(message_repeatability)
            no_error_flag = False


        # Creating file string
        if no_error_flag:
            config_str = f"{time_from} {time_to} {percentage} {repeatability} {time_on_website_from} {time_on_website_to} " \
               f"{transition_amount_from} {transition_amount_to} {robot_id} {1 if self.checkBox_adv else 0} " \
               f"{1 if self.checkBox_search else 0}\n{self.textEdit_urls.toPlainText()}"
            # Downloading file on google drive
            gdrive_upload(f'config_{robot_id}.txt', config_str)
            message_success = 'Файл успешно загружен.'
            NotificationWindow(message_success)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = Ui()
    w.show()
    sys.exit(app.exec_())