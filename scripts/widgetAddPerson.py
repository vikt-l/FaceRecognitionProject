from PIL import Image
from PyQt5.Qt import *

from person_info_window import Ui_Form
from funcAddTodb import f_addPersontodb


class NotAllInfo(Exception):
    pass


class PersonInfoAdd(QWidget, Ui_Form):

    # форма для добавления информации о человеке в базу данных

    def __init__(self, theme):
        super().__init__()
        self.theme = theme
        self.setupUi(self)
        self.initUI()
        self.changeColor()

    def initUI(self):
        self.btn_addPhoto.clicked.connect(self.photo)
        self.bth_addPerson_done.clicked.connect(self.done)

        self.lbl_err = QLabel(self)
        self.lbl_err.setText('Введите полную информацию')
        self.lbl_err.hide()

        self.fname = None

    def photo(self):
        # получение фото, добавление его на форму

        try:
            self.fname = QFileDialog.getOpenFileName(self, '', '')[0]
            img = QImage(self.fname).scaled(200, 200, Qt.KeepAspectRatio)
            self.lbl_photo.setPixmap(QPixmap.fromImage(img))

        except Exception as ex:
            print(ex)

    def done(self):
        # добавление информации о человеке в бд

        self.lbl_err.hide()
        try:
            name = self.lineEdit_name.text()
            surname = self.lineEdit_surname.text()
            age = self.spinBoxAge.value()
            year = self.calendarWidget.selectedDate()
            year = year.toString('yyyy-MM-dd')
            info = self.plainTextEditInfo.toPlainText()
            path_photo = self.fname

            if not all([name, surname, age, year, info, path_photo]):
                raise NotAllInfo

            img = Image.open(path_photo)
            img.save(f"../people/{name}_{surname}.jpeg")

            f_addPersontodb(name, surname, age, year, info, path_photo)
            self.close()

        except NotAllInfo:
            self.lbl_err.show()

        except Exception:
            self.lbl_err.show()

    def changeColor(self):

        # меняет тему приложения

        if self.theme == 'dark':
            self.setDarkTheme()
        elif self.theme == 'light':
            self.setLightTheme()

    def setLightTheme(self):

        # устанавливает светлую тему

        self.setStyleSheet('background-color: #f4f5f6')
        self.plainTextEditInfo.setStyleSheet('color: #0b1016; background-color: #cacfd5')
        self.btn_addPhoto.setStyleSheet('color: #0b1016; background-color: #cacfd5')
        self.bth_addPerson_done.setStyleSheet('color: #0b1016; background-color: #cacfd5')
        self.lineEdit_name.setStyleSheet('color: #0b1016; background-color: #cacfd5')
        self.lineEdit_surname.setStyleSheet('color: #0b1016; background-color: #cacfd5')
        self.spinBoxAge.setStyleSheet('color: #0b1016; background-color: #cacfd5')
        self.lbl_name.setStyleSheet('color: #0b1016')
        self.lbl_surname.setStyleSheet('color: #0b1016')
        self.lbl_age.setStyleSheet('color: #0b1016')
        self.lbl_year.setStyleSheet('color: #0b1016')
        self.lbl_info.setStyleSheet('color: #0b1016')

    def setDarkTheme(self):

        # устанавливает темную тему

        self.setStyleSheet('background-color: #38444c')
        self.plainTextEditInfo.setStyleSheet('color: #f0f2f3; background-color: #697278')
        self.btn_addPhoto.setStyleSheet('color: #f0f2f3; background-color: #697278')
        self.bth_addPerson_done.setStyleSheet('color: #f0f2f3; background-color: #697278')
        self.lineEdit_name.setStyleSheet('color: #f0f2f3; background-color: #697278')
        self.lineEdit_surname.setStyleSheet('color: #f0f2f3; background-color: #697278')
        self.spinBoxAge.setStyleSheet('color: #f0f2f3; background-color: #697278')
        self.lbl_name.setStyleSheet('color: #f0f2f3')
        self.lbl_surname.setStyleSheet('color: #f0f2f3')
        self.lbl_age.setStyleSheet('color: #f0f2f3')
        self.lbl_year.setStyleSheet('color: #f0f2f3')
        self.lbl_info.setStyleSheet('color: #f0f2f3')
