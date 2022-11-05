import os
import sys

from PyQt5.QtCore import QDir, Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel, QRadioButton,
                             QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget)
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QAction
from PyQt5.QtGui import QIcon


#
# class videoPlayer(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.initUI()
#
#     def initUI(self):
#         self.sp_videos = os.listdir('../recording_video')
#         self.sp_radio_btn = []
#
#         self.btn = QPushButton(self)
#         self.btn.setText('play video')
#         self.btn.clicked.connect(self.playVideo)
#
#         self.x1 = 40
#         self.x2 = 60
#         self.y = 40
#
#         for i in range(len(self.sp_videos)):
#             self.radio_btn = QRadioButton(self)
#             self.radio_btn.move(self.x1, self.y)
#             self.sp_radio_btn.append(self.radio_btn)
#
#             self.lbl_title_video = QLabel(self)
#             self.lbl_title_video.setText(self.sp_videos[i][self.sp_videos[i].rfind('/') + 1:])
#             self.lbl_title_video.move(self.x2, self.y)
#
#             self.y += 30
#
#         self.btn.move(self.x1, self.y + 30)
#         self.resize(300, self.y + 60)
#
#         self.player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
#         self.clip = QVideoWidget()
#         self.player.setVideoOutput(self.clip)
#
#     def playVideo(self):
#         for i in range(len(self.sp_radio_btn)):
#             self.r_btn = self.sp_radio_btn[i]
#
#             if self.r_btn.isChecked():
#                 a = self.sp_videos[i]
#                 self.player.setMedia(QMediaContent(QUrl.fromLocalFile(f'../recording_video/{a}')))
#                 self.player.play()
#                 break
#
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     form = videoPlayer()
#     form.show()
#     sys.exit(app.exec())
#
#
#
#

class VideoPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Video Player")

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        videoWidget = QVideoWidget()

        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)

        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)

        self.error = QLabel()
        self.error.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        openButton = QPushButton("Open Video")
        openButton.setToolTip("Open Video File")
        openButton.setStatusTip("Open Video File")
        openButton.setFixedHeight(24)
        openButton.clicked.connect(self.openFile)

        # Create a widget for window contents
        wid = QWidget(self)
        self.setCentralWidget(wid)

        # Create layouts to place inside widget
        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.positionSlider)

        layout = QVBoxLayout()
        layout.addWidget(videoWidget)
        layout.addLayout(controlLayout)
        layout.addWidget(self.error)
        layout.addWidget(openButton)

        # Set widget to contain window contents
        wid.setLayout(layout)

        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)

    def openFile(self):
        fileName = QFileDialog.getOpenFileName(self, "Open Movie", '')[0]

        if fileName != '':
            self.mediaPlayer.setMedia(
                QMediaContent(QUrl.fromLocalFile(fileName)))
            self.playButton.setEnabled(True)

    def exitCall(self):
        sys.exit(app.exec_())

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay))

    def positionChanged(self, position):
        self.positionSlider.setValue(position)

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)


app = QApplication(sys.argv)
videoplayer = VideoPlayer()
videoplayer.resize(640, 480)
videoplayer.show()
sys.exit(app.exec_())