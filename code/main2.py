import sys
import cv2
import numpy

from mainWindow import Ui_MainWindow
from widgetAddPerson import PersonInfoAdd
from getHelpWidget import Help
from func import f_addVideotodb

from PyQt5.Qt import *
from PyQt5 import QtCore, QtWidgets

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class Form(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.theme = 'light'
        self.flag_recording = False
        self.number_recording = 0


        self.btn_theme.clicked.connect(self.changeColor)
        self.addPeople.clicked.connect(self.f_addpeople)
        self.btn_help.clicked.connect(self.get_help)
        self.btnRecording.clicked.connect(self.start_recording)
        self.btnStopRecording.clicked.connect(self.stop_recording)

        self.setLightTheme()
        self.dateTimeEd.setDateTime(QDateTime.currentDateTime())

        self.thread = ThreadOpenCV()
        self.thread.start()
        self.thread.changePixmap.connect(self.setVideo)
        self.thread.changePixmap.connect(self.recording)

    def setVideo(self, img, names, peoples, count, time):
        self.video.setPixmap(QPixmap.fromImage(img))

        self.names = names
        self.peoples = peoples
        self.count = count
        self.time = time

        for i in names:
            self.all_peoples.add(i)

    def changeColor(self):
        # меняет тему приложения

        if self.btn_theme.text() == 'тёмная тема':
            self.setDarkTheme()
            self.theme = 'dark'
        elif self.btn_theme.text() == 'светлая тема':
            self.setLightTheme()
            self.theme = 'light'

    def setLightTheme(self):
        # устанавливает светлую тему

        self.setStyleSheet('background-color: #f4f5f6')
        self.btn_theme.setText('тёмная тема')
        self.addPeople.setStyleSheet('color: #0b1016; background-color: #cacfd5')
        self.btn_help.setStyleSheet('color: #0b1016; background-color: #cacfd5')
        self.btn_theme.setStyleSheet('color: #0b1016; background-color: #cacfd5')
        self.btnRecording.setStyleSheet('color: #0b1016; background-color: #cacfd5')
        self.btnStopRecording.setStyleSheet('color: #0b1016; background-color: #cacfd5')
        self.cBoxNames.setStyleSheet('color: #0b1016; background-color: #cacfd5')
        self.namesPeoples.setStyleSheet('color: #0b1016; background-color: #cacfd5')
        self.infoPeople.setStyleSheet('color: #0b1016; background-color: #cacfd5')
        self.dateTimeEd.setStyleSheet('color: #0b1016; background-color: #cacfd5')
        self.lcdNumberPeople.setStyleSheet('background-color: #cacfd5')
        self.lbl_date.setStyleSheet('color: #0b1016')
        self.lblNumberPeople.setStyleSheet('color: #0b1016')

    def setDarkTheme(self):
        # устанавливает темную тему

        self.setStyleSheet('background-color: #38444c')
        self.btn_theme.setText('светлая тема')
        self.addPeople.setStyleSheet('color: #f0f2f3; background-color: #697278')
        self.btn_help.setStyleSheet('color: #f0f2f3; background-color: #697278')
        self.btn_theme.setStyleSheet('color: #f0f2f3; background-color: #697278')
        self.btnRecording.setStyleSheet('color: #f0f2f3; background-color: #697278')
        self.btnStopRecording.setStyleSheet('color: #f0f2f3; background-color: #697278')
        self.cBoxNames.setStyleSheet('color: #f0f2f3; background-color: #293238')
        self.namesPeoples.setStyleSheet('color: #f0f2f3; background-color: #697278')
        self.infoPeople.setStyleSheet('color: #f0f2f3; background-color: #697278')
        self.dateTimeEd.setStyleSheet('color: #f0f2f3; background-color: #293238')
        self.lcdNumberPeople.setStyleSheet('background-color: #293238')
        self.lbl_date.setStyleSheet('color: #f0f2f3')
        self.lblNumberPeople.setStyleSheet('color: #f0f2f3')

    def get_help(self):
        # открывает форму для получения описания программы

        self.window_help = Help()
        self.window_help.show()

    def f_addpeople(self):
        # создает форму для довабления информации о человеке в базу данных

        self.form_to_add_people = PersonInfoAdd(self.theme)
        self.form_to_add_people.show()

    def start_recording(self):
        self.dt_rec = self.dateTimeEd.dateTime()
        self.all_peoples = set()
        self.count_not_known = 0
        self.flag_recording = True
        self.number_recording += 1

        frame_width = 700
        frame_height = 700
        fourcc = cv2.VideoWriter_fourcc(*'MPEG')
        self.video_record = cv2.VideoWriter(f'../recording_video/recording_{self.number_recording}.avi', fourcc,
                                       20.0, (frame_width, frame_height))

    def recording(self, *args):
        if self.flag_recording:
            args = list(args)
            self.video_record.write(args[-1])

    def stop_recording(self):
        if self.flag_recording:
            self.flag_recording = False

            f_addVideotodb(self.dt_rec, self.all_peoples,
                           f'../recording_video/recording_{self.number_recording}.avi')
        else:
            pass


class ThreadOpenCV(QThread):
    changePixmap = pyqtSignal(QImage, list, str, int, str, numpy.ndarray)

    def __init__(self):
        super().__init__()

    def run(self):
        cap = cv2.VideoCapture(0)

        while True:
            success, frame = cap.read()
            if success:
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(
                    rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(700, 700, Qt.KeepAspectRatio)
                self.changePixmap.emit(p, [], '', 0, '', frame)


            self.msleep(20)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec())