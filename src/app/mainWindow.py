import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl

class MusicPlayer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def style(self, fileStyle):
        self.setStyle(fileStyle)

    def initUI(self):
        self.setWindowTitle("Music Player")
        self.setGeometry(100, 100, 400, 200)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.open_button = QPushButton("Open")
        self.open_button.clicked.connect(self.open_file)
        self.layout.addWidget(self.open_button)

        self.play_button = QPushButton("Play")
        self.play_button.clicked.connect(self.play_song)
        self.layout.addWidget(self.play_button)

        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop_song)
        self.layout.addWidget(self.stop_button)

        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)

    def open_file(self):
        self.filename, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Audio Files (*.mp3 *.wav)")
        if self.filename:
            self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(self.filename)))

    def play_song(self):
        if self.filename:
            self.media_player.play()

    def stop_song(self):
        self.media_player.stop()

