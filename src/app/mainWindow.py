import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QSlider
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, QCoreApplication, Qt, QSize
from PyQt5.QtGui import QColor, QPalette, QIcon

WINW = 460
WINH = 340

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Music Player')
        self.setFixedSize(QSize(WINW, WINH))
        
        with open("src\\assets\\css\\styles.css", 'r') as styleFile:
            self.setStyleSheet(styleFile.read())
        
        self.media_player = QMediaPlayer(None, QMediaPlayer.StreamPlayback)
        self.media_player.mediaStatusChanged.connect(self.printMediaData)
        
        self.folder_path = None
        self.music_files = []
        self.current_song = 0
        self.playing = False
        
        self.play_icon = QIcon('src\\assets\\icons\\play.png')
        self.stop_icon = QIcon('src\\assets\\icons\\stop.png')
        self.next_icon = QIcon('src\\assets\\icons\\next.png')
        self.prev_icon = QIcon('src\\assets\\icons\\prev.png')

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        
        self.statusLabel = QLabel()
       

        self.openFolderButton = QPushButton('Open Folder')
        self.openFolderButton.clicked.connect(self.open_folder)
        
        
        self.playStopButton = QPushButton("")
        self.playStopButton.setIcon(self.play_icon)
        self.playStopButton.clicked.connect(self.play_stop_song)
        self.playStopButton.setEnabled(False)
        

        self.prevButton = QPushButton("")
        self.prevButton.setIcon(self.prev_icon)
        self.prevButton.clicked.connect(self.prev_song)
        self.prevButton.setEnabled(False)
        

        self.nextButton = QPushButton("")
        self.nextButton.setIcon(self.next_icon)
        self.nextButton.clicked.connect(self.next_song)
        self.nextButton.setEnabled(False)
        

        self.volumeSlider = QSlider(orientation=Qt.Horizontal)
        self.volumeSlider.setRange(0, 100)
        self.volumeSlider.setValue(50)
        self.volumeSlider.valueChanged.connect(self.change_volume)
        
        
        
        layout.addWidget(self.statusLabel)
        layout.addWidget(self.openFolderButton)
        layout.addWidget(self.playStopButton)
        layout.addWidget(self.prevButton)
        layout.addWidget(self.nextButton)
        layout.addWidget(self.volumeSlider)
        self.setLayout(layout)


    def printLabel(self, text) -> None:
        self.statusLabel.setText(text)


    def open_folder(self):
        self.folder_path = QFileDialog.getExistingDirectory(self, "Open Folder")
        if self.folder_path:
            self.music_files = [f for f in os.listdir(self.folder_path) if f.endswith('.mp3') or f.endswith('.wav')]
            if self.music_files:
                self.playStopButton.setEnabled(True)
                self.prevButton.setEnabled(True)
                self.nextButton.setEnabled(True)

            else:
                self.printLabel("No music files found in the folder.")


    def play_song(self, filename):
        self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(os.path.join(self.folder_path, filename))))
        self.media_player.play()
        self.playStopButton.setIcon(self.stop_icon)
        self.playing = True


    def play_stop_song(self):
        if self.playing:
            self.media_player.stop()
            self.playStopButton.setIcon(self.play_icon)
            self.playing = False
        else:
            self.media_player.play()
            self.playStopButton.setIcon(self.stop_icon)
            self.playing = True


    def prev_song(self):
        self.current_song = self.current_song if self.current_song > 0 else len(self.music_files)
        self.media_player.stop()
        self.play_song(self.music_files[self.current_song - 1])
        self.current_song -= 1
        


    def next_song(self):
        self.current_song = self.current_song if self.current_song < len(self.music_files) else 0
        self.media_player.stop()
        self.play_song(self.music_files[self.current_song + 1])
        self.current_song += 1


    def change_volume(self, value):
        self.media_player.setVolume(value)


    def printMediaData(self):
        if self.media_player.mediaStatus() == 6:
            if self.media_player.isMetaDataAvailable():
                title = self.media_player.metaData("Title")
                author = self.media_player.metaData("Author")
                
                self.printLabel("{} {}".format(title,author))
                
                print(f"Title: {title}, Author: {author}")
            else:
                print("no metaData available")