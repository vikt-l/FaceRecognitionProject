import sys
import sqlite3
from PIL import Image

import face_recognition as fr
import cv2
import os

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.Qt import QDateTime
from PyQt5.QtGui import QPixmap

from mainWindow import Ui_MainWindow
from widgetAddPerson import PersonInfoAdd
from func import f_addVideotodb
from getHelpWidget import Help
from PyQt5 import QtCore, QtWidgets
from PyQt5.Qt import *

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class Form(QMainWindow, Ui_MainWindow):
    # главная форма

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.theme = 'light'

        self.addPeople.clicked.connect(self.f_addpeople)
        self.dateTimeEd.setDateTime(QDateTime.currentDateTime())
        self.btn_theme.clicked.connect(self.changeColor)
        self.setLightTheme()

        self.cBoxNames.activated.connect(self.get_info)
        self.btn_help.clicked.connect(self.get_help())

        self.thread1 = ThreadOpenCV()
        self.thread1.start()
        self.thread1.changePixmap.connect(self.set_video)

    def f_addpeople(self):
        # создает форму для довабления информации о человеке в базу данных

        self.form_to_add_people = PersonInfoAdd(self.theme)
        self.form_to_add_people.show()

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
        self.pushButton.setStyleSheet('color: #0b1016; background-color: #cacfd5')
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
        self.pushButton.setStyleSheet('color: #f0f2f3; background-color: #697278')
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

    def set_video(self, image, find_faces, peoples, names):
        # добавление видео и информации на форму

        self.namesPeoples.clear()
        self.infoPeople.clear()
        self.img_photo.clear()
        self.cBoxNames.clear()

        self.lcdNumberPeople.display(find_faces)
        self.namesPeoples.setPlainText(names)
        self.cBoxNames.addItems(peoples)

        self.video_pixmap = QPixmap('../photo/image_2.jpeg')
        self.video.setPixmap(self.video_pixmap)

    def get_info(self):
        # добавляет на форму информацию о выбранном человеке

        n = self.cBoxNames.currentText().split()
        name = n[0]
        surname = n[1]

        con = sqlite3.connect('person_db.sqlite')
        cur = con.cursor()
        res = cur.execute(f"""SELECT * FROM person
        WHERE name LIKE '{name}' AND surname LIKE '{surname}'""").fetchall()
        print(res)

        age, year, information, photoPath = res[0]
        self.infoPeople.setPlainText(f'{name} {surname}\nвозраст: {age}, дата рождения: {year}\n{information}')

        photo = Image.open(photoPath)
        fixed_height = 150
        percent = fixed_height / float(photo.size[0])
        width_size = int((float(photo.size[1]) * float(percent)))
        img = photo.resize((fixed_height, width_size))
        img.save('result.jpeg')

        self.pixmap = QPixmap('result.jpeg')
        self.lbl_photo.setPixmap(self.pixmap)

        self.img_photo.setPixmap(photo)

    # def start_recording(self):
    #     # начало записи видео
    #
    #     self.sp_peoples = set()
    #     self.count_not_known = 0
    #     self.flag_recording = True
    #     self.number_recording += 1
    #     self.dt_rec = self.dateTimeEd.dateTime()
    #
    #     frame_width = int(self.cap.get(3))
    #     frame_height = int(self.cap.get(4))
    #     fourcc = cv2.VideoWriter_fourcc(*'MPEG')
    #     self.video_recording = cv2.VideoWriter(f'../recording_video/recording_{self.number_recording}.avi', fourcc,
    #                                            20.0, (frame_width, frame_height))
    #
    # def stop_recording(self):
    #     # остановка записи видео и внесение информации в базу данных
    #
    #     self.flag_recording = False
    #     f_addVideotodb(1, self.sp_peoples, self.count_not_known,
    #                    f'../recording_video/recording_{self.number_recording}.avi')

    def get_help(self):
        # открывает форму для получения описания программы

        self.window_help = Help()
        self.window_help.show()


class ThreadOpenCV(QThread):
    changePixmap = pyqtSignal(QImage, int, str, str)

    def __init__(self):
        super().__init__()
        self.flag_recording = False
        self.peoples = []
        self.number_recording = 0

    def video_run(self):
        # получение доступа к камере, поиск и идентификация лиц

        # вывести find_facec, image, name - surname/ unknown

        cap = cv2.VideoCapture('../test_media/video.mp4')
        known_people = os.listdir('../people')

        while cap.isOpened():

            success, self.img = cap.read()
            if not success:
                if self.flag_recording:
                    self.stop_recording()
                break

            cv2.imwrite('../photo/image.jpeg', self.img)

            img_fr = fr.load_image_file('../photo/image.jpeg')
            faces_loc = fr.face_locations(img_fr)
            find_faces = len(faces_loc)

            self.current_k_Npeople = 0

            for i in range(find_faces):

                y, x1, y1, x = faces_loc[i]
                cv2.imwrite('../photo/image_face.jpeg', self.img[y:y1, x:x1])
                cv2.rectangle(self.img, (x, y), (x1, y1), (250, 250, 0), 2)
                result = False

                for i_face in known_people:
                    known_face = fr.load_image_file(f'../people/{i_face}')
                    known_face_enc = fr.face_encodings(known_face)[0]

                    unknown_face = fr.load_image_file('../photo/image_face.jpeg')
                    unknown_face_enc = fr.face_encodings(unknown_face)[0]

                    result = fr.compare_faces([known_face_enc], unknown_face_enc)

                    if result:
                        name = i_face[:i_face.find('.')].split('_')[0]
                        surname = i_face[:i_face.find('.')].split('_')[1]
                        cv2.putText(self.img, f"{name} {surname}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                    (20, 20, 0), 2,
                                    cv2.LINE_AA)
                        self.peoples.append(f"{name} {surname}")
                        #
                        # if self.flag_recording:
                        #     self.sp_peoples.add(f"{name} {surname}")
                        break

                if not result:
                    cv2.putText(self.img, 'unknown', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 200, 0), 1,
                                cv2.LINE_AA)

                    self.current_k_Npeople += 1
                    #
                    # if self.flag_recording:
                    #     self.count_not_known += 1

            self.names = '\n'.join(self.peoples)
            if self.current_k_Npeople:
                self.names += f"\nнеизвестные: {self.current_k_Npeople}"

            cv2.imwrite('../photo/image_2.jpeg', self.img)

            rgbImage = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
            h, w, ch = rgbImage.shape
            bytesPerLine = ch * w
            convertToQtFormat = QImage(
                rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
            p = convertToQtFormat.scaled(500, 500, Qt.KeepAspectRatio)
            self.changePixmap.emit(p, find_faces, self.peoples, self.names)

            # if self.flag_recording:
            #     self.video_recording.write(self.img)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec())
