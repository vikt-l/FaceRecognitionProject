import sys
import cv2
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import *


class ThreadOpenCV(QThread):
    changePixmap = pyqtSignal(QImage, str)

    def __init__(self):
        super().__init__()

    def run(self):
        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()
            if ret:
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(
                    rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(300, 300, Qt.KeepAspectRatio)
                self.changePixmap.emit(p, 'hello')


            self.msleep(20)


class Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(300, 300, 500, 500)

        self.btn = QtWidgets.QPushButton(self)
        self.btn.clicked.connect(self.can)

        self.lbl = QtWidgets.QLabel(self)
        self.lbl.resize(500, 500)
        self.lbl.move(100, 100)

        # +++
        self.thread = ThreadOpenCV()  # +++
        self.thread.changePixmap.connect(self.setImage)  # +++

    def can(self):
        self.thread.start()  # +++

    def setImage(self, image, msg):  # +++
        self.lbl.setPixmap(QPixmap.fromImage(image))  # +++
        print(msg)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
