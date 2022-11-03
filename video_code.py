import sys
import cv2
import numpy
import threading

from PyQt5.QtWidgets import QApplication, QLabel, QWidget
from PyQt5.QtCore import pyqtSignal, QThread, QObject
from PyQt5.QtGui import QImage, QPixmap


class VideoCapture(QWidget):
    def __init__(self):
        super().__init__()
        self.label = QLabel(self)
        self.label.setGeometry(0, 0, 640, 480)
        self.work_thread = WorkThread()
        self.thread = threading.Thread(target=self.work_thread.func)
        self.thread.start()


    def closeEvent(self, event):
        self.thread.stop()
        event.accept()

    def draw(self, img):
        print("I should Redraw")
        height, width, channel = img.shape
        bpl = 3 * width
        self.qImg = QImage(img, width, height, bpl, QImage.Format_RGB888)
        pix = QPixmap(self.qImg)
        self.label.setPixmap(pix)
        self.label.show()


class WorkThread(QObject):
    camera = cv2.VideoCapture(0)
    signal = pyqtSignal()

    def func(self):
        while True:
            b, self.frame = self.camera.read()
            self.signal.emit()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    video_capture_widget = VideoCapture()
    video_capture_widget.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())