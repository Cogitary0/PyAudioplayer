import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QColor, QPalette, QIcon

WINW = 360
WINH = 140

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(300, 300, WINW, WINH)
        self.setFixedSize(WINW, WINH)
        self.setWindowTitle('Music Player')
        self.initUI()
        
        with open("src\\assets\\css\\styles.css", 'r') as styleFile:
            self.setStyleSheet(styleFile.read())
        
        self.media_player = QMediaPlayer(None, QMediaPlayer.StreamPlayback)
        self.media_player.mediaStatusChanged.connect(self.printMediaData)
        
        self.filename = None
        self.playing = False
        self.play_icon = QIcon('src\\assets\\icons\\play.png')
        self.stop_icon = QIcon('src\\assets\\icons\\stop.png')

        

    def initUI(self):
        layout = QVBoxLayout()
        
        self.statusLabel = QLabel()
        layout.addWidget(self.statusLabel)

        self.openFileButton = QPushButton('Open File')
        self.openFileButton.clicked.connect(self.open_file)
        layout.addWidget(self.openFileButton)
        
        self.playStopButton = QPushButton("")
        self.playStopButton.clicked.connect(self.play_stop_song)
        self.playStopButton.setEnabled(False)
        layout.addWidget(self.playStopButton)
        

        self.setLayout(layout)


    def printLabel(self, text) -> None:
        self.statusLabel.setText(text)


    def open_file(self):
        self.filename, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Audio Files (*.mp3 *.wav)")
        if self.filename:
            self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(self.filename)))
            self.playStopButton.setEnabled(True)
            self.playStopButton.setIcon(self.play_icon)

    def play_stop_song(self):
        if self.filename:
            if not self.playing:
                self.media_player.play()

                self.playStopButton.setIcon(self.stop_icon)
                self.playing = True
            else:
                self.media_player.stop()

                self.playStopButton.setIcon(self.play_icon)
                self.playing = False


    def printMediaData(self):
        if self.media_player.mediaStatus() == 6:
            if self.media_player.isMetaDataAvailable():
                title = self.media_player.metaData("Title")
                author = self.media_player.metaData("Author")
                
                self.printLabel("{} {}".format(title,author))
                
                print(f"Title: {title}, Author: {author}")
            else:
                print("no metaData available")