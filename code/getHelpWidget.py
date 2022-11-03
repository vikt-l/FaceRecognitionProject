from PyQt5.QtWidgets import QWidget
from helpwidget import Ui_Form


class Help(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        with open('help.txt') as file:
            file = file.readlines()
            for i in file:
                self.plainTextEditHelp.setPlainText(i)

        self.btn_closeHelp.clicked.connect(self.close)

    def close(self):
        self.plainTextEditHelp.clear()
        self.close()
