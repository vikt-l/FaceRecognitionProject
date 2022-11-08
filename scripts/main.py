import sys
import cv2
import numpy
import sqlite3
import os

import face_recognition as fr

from mainWindow import Ui_MainWindow
from widgetAddPerson import PersonInfoAdd
from getHelpWidget import Help
from funcAddTodb import f_addVideotodb

from PyQt5.Qt import *
from PyQt5 import QtCore, QtWidgets, QtMultimedia
from PyQt5.QtCore import Qt

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
        self.flag_recording = False
        self.number_recording = 0

        self.btn_theme.clicked.connect(self.changeColor)
        self.addPeople.clicked.connect(self.f_addpeople)
        self.btn_help.clicked.connect(self.get_help)
        self.btnRecording.clicked.connect(self.start_recording)
        self.btnStopRecording.clicked.connect(self.stop_recording)

        self.addPeople.clicked.connect(self.load_mp3)
        self.btnRecording.clicked.connect(self.load_mp3)
        self.btnStopRecording.clicked.connect(self.load_mp3)
        self.btn_theme.clicked.connect(self.load_mp3)
        self.btn_help.clicked.connect(self.load_mp3)

        self.setLightTheme()
        self.dateTimeEd.setDateTime(QDateTime.currentDateTime())
        self.cBoxNames.activated.connect(self.get_info)

        self.thread = ThreadOpenCV()
        self.thread.start()
        self.thread.changePixmap.connect(self.setVideo)
        self.thread.changePixmap.connect(self.recording)

    def setVideo(self, img, names, peoples, count):

        # добавить на форму видео и информацию о нем

        self.video.setPixmap(QPixmap.fromImage(img))

        self.names = names
        self.peoples = peoples
        self.count = count

        self.cBoxNames.clear()

        if self.flag_recording:
            for i in names:
                self.all_peoples.add(i)

        self.lcdNumberPeople.display(count)
        self.namesPeoples.setPlainText(peoples)
        self.cBoxNames.addItems(names)

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
        self.lcdNumberPeople.setStyleSheet('background-color: #697278')
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

        # начало записи видео

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

        # запись видео

        if self.flag_recording:
            args = list(args)
            self.video_record.write(args[-1])

    def stop_recording(self):

        # окончание записи видео

        if self.flag_recording:
            self.flag_recording = False

            f_addVideotodb(self.dt_rec, self.all_peoples,
                           f'../recording_video/recording_{self.number_recording}.avi')
        else:
            pass

    def keyPressEvent(self, event):

        # обработка нажатий клавиатуры

        if event.key() == Qt.Key_Q:
            self.f_addpeople()

        elif event.key() == Qt.Key_W:
            self.start_recording()

        elif event.key() == Qt.Key_E:
            self.stop_recording()

        elif event.key() == Qt.Key_R:
            self.get_help()

        elif event.key() == Qt.Key_T:
            self.changeColor()

    def get_info(self):

        # добавляет на форму информацию о выбранном человеке

        n = self.cBoxNames.currentText().split()
        name = n[0]
        surname = n[1]

        con = sqlite3.connect('../person_db.sqlite')
        cur = con.cursor()
        res = cur.execute(f"""select * from person
        where name like '{name}' and surname like '{surname}'""").fetchall()
        con.close()

        age, year, information, photoPath = tuple(list(res[0])[3:])
        self.infoPeople.setPlainText(f'{name} {surname}\nвозраст: {age}, дата рождения: {year}\n{information}')

        img = QImage(photoPath).scaled(200, 200, Qt.KeepAspectRatio)
        self.img_photo.setPixmap(QPixmap.fromImage(img))

    def load_mp3(self):

        # воспроизводит звук при нажатии кнопок

        media = QtCore.QUrl.fromLocalFile('../clickSound.mp3')
        content = QtMultimedia.QMediaContent(media)
        self.player = QtMultimedia.QMediaPlayer()
        self.player.setMedia(content)
        self.player.play()


class ThreadOpenCV(QThread):

    # класс для обработки видео и передачи инфорации на главную форму

    changePixmap = pyqtSignal(QImage, list, str, int, numpy.ndarray)

    def __init__(self):
        super().__init__()
        self.k_frame = 0

    def run(self):

        # обработка видео

        cap = cv2.VideoCapture(0)
        known_people = os.listdir('../people')

        while True:
            try:
                success, frame = cap.read()
                if success:
                    self.k_frame += 1
                    if self.k_frame == 1:
                        cv2.imwrite('../photo/image.jpeg', frame)
                        img_fr = fr.load_image_file('../photo/image.jpeg')
                        faces_loc = fr.face_locations(img_fr)
                        find_faces = len(faces_loc)
                        names = []
                        peoples = ''

                        for i in range(find_faces):
                            y, x1, y1, x = faces_loc[i]
                            cv2.imwrite('../photo/image_face.jpeg', frame[y:y1, x:x1])
                            cv2.rectangle(frame, (x, y), (x1, y1), (250, 250, 0), 2)

                            for i_face in known_people:
                                known_face = fr.load_image_file(f'../people/{i_face}')
                                known_face_enc = fr.face_encodings(known_face)[0]

                                unknown_face = fr.load_image_file('../photo/image_face.jpeg')
                                unknown_face_enc = fr.face_encodings(unknown_face)[0]

                                result = fr.compare_faces([known_face_enc], unknown_face_enc)

                                if result:
                                    name = i_face[:i_face.find('.')].split('_')[0]
                                    surname = i_face[:i_face.find('.')].split('_')[1]
                                    cv2.putText(frame, f"{name} {surname}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                                (200, 200, 200), 2,
                                                cv2.LINE_AA)
                                    names.append(f"{name} {surname}")

                                if not result:
                                    cv2.putText(frame, 'unknown', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 200, 200), 1,
                                                cv2.LINE_AA)

                            peoples = '\n'.join(names)
                            if len(names) < find_faces:
                                peoples += f'неизвестные: {find_faces - len(names)}'

                        rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        h, w, ch = rgbImage.shape
                        bytesPerLine = ch * w
                        convertToQtFormat = QImage(
                            rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                        p = convertToQtFormat.scaled(700, 700, Qt.KeepAspectRatio)
                        self.changePixmap.emit(p, names, peoples, find_faces, frame)

                    elif self.k_frame == 4:
                        self.k_frame = 0

            except Exception:
                pass

        cap.realease()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec())
