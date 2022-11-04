from PyQt5 import QtCore
from PyQt5.Qt import *
from PyQt5.QtWidgets import *

import sys
import cv2
import numpy as np


class Form(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 500, 500)

        self.video = QLabel(self)
        self.video.move(100, 100)

        self.btn_start = QPushButton(self)
        self.btn_start.setText('start')
        self.btn_start.clicked.connect(self.start)

        self.thread1 = ThreadOpenCV()
        self.thread1.changePixmap.connect(self.set_video)

    def start(self):
        self.thread1.start()

    def set_video(self, image):
        self.video.setPixmap(QPixmap.fromImage(image))


class ThreadOpenCV(QThread):
    changePixmap = pyqtSignal(QImage)

    def __init__(self):
        super().__init__()

    def video_run(self):

        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        cap.set(cv2.CAP_PROP_FPS, 24)

        while True:
            success, self.img = cap.read()
            if success:

                rgbImage = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(
                    rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(500, 500, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)
            self.msleep(20)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec())

