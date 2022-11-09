from PyQt5.QtWidgets import QWidget
from helpwidget import Ui_Form


class Help(QWidget, Ui_Form):

    # класс помогает получить описание программы из текстового файла

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Help')

        with open('help.txt', encoding='utf8') as file:
            file = file.readlines()
            for i in file:
                self.plainTextEditHelp.insertPlainText(i)
