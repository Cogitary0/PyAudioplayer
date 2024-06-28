import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QColor, QPalette

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.WINW = 360
        self.WINH = 140
        self.setGeometry(300, 300, self.WINW, self.WINH)
        self.setFixedSize(self.WINW, self.WINH)
        self.setWindowTitle('Music Player')
        self.initUI()
        
        with open("src\\assets\\css\\styles.css", 'r') as styleFile:
            self.setStyleSheet(styleFile.read())
        
        self.media_player = QMediaPlayer(None, QMediaPlayer.StreamPlayback)
        self.media_player.mediaStatusChanged.connect(self.printMediaData)

    def initUI(self):
        layout = QVBoxLayout()

        openFileButton = QPushButton('Open File')
        openFileButton.clicked.connect(self.open_file)
        layout.addWidget(openFileButton)

        playButton = QPushButton('Play')
        playButton.clicked.connect(self.play_song)
        layout.addWidget(playButton)

        stopButton = QPushButton('Stop')
        stopButton.clicked.connect(self.stop_song)
        layout.addWidget(stopButton)

        self.statusLabel = QLabel()
        layout.addWidget(self.statusLabel)

        self.setLayout(layout)

    def printLabel(self, text) -> None:
        self.statusLabel.setText(text)

    def open_file(self):
        self.filename, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Audio Files (*.mp3 *.wav)")
        if self.filename:
            self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(self.filename)))

    def play_song(self):
        if self.filename:
            self.media_player.play()

    def stop_song(self):
        self.media_player.stop()

    def printMediaData(self):
        if self.media_player.mediaStatus() == 6:
            if self.media_player.isMetaDataAvailable():
                res = str(self.media_player.metaData("Resolution")).partition("PyQt5.QtCore.QSize(").replace(", ", "x").replace(")", "")
                print("%s%s" % ("Audio Resolution = ", res))
            else:
                print("no metaData available")