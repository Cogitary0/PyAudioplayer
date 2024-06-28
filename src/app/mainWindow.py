import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QSlider, QHBoxLayout
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, QCoreApplication, Qt, QSize, QTimer
from PyQt5.QtGui import QColor, QPalette, QIcon

WINW = 360
WINH = 240

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
        self.folder_icon = QIcon('src\\assets\\icons\\folderOpen.png')
        self.downloader_icon = QIcon('src\\assets\\icons\\downloader.png')
        
        self.initUI()

    def initUI(self):
        
        layout = QVBoxLayout()
        controlLayout = QHBoxLayout()
        utilsLayout = QHBoxLayout()
        
        self.statusLabel = QLabel()
        self.statusLabel.setFixedHeight(42)
        layout.addWidget(self.statusLabel)
        
        self.dataLabel = QLabel()
        layout.addWidget(self.dataLabel)
        
        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setMinimum(0)
        self.positionSlider.setMaximum(100)
        self.positionSlider.setValue(0)
        self.positionSlider.valueChanged.connect(self.seek_position)
        layout.addWidget(self.positionSlider)
        
        
        self.openFolderButton = QPushButton()
        self.openFolderButton.setIcon(self.folder_icon)
        self.openFolderButton.clicked.connect(self.open_folder)
        utilsLayout.addWidget(self.openFolderButton)
            
        
        self.prevButton = QPushButton()
        self.prevButton.setIcon(self.prev_icon)
        self.prevButton.clicked.connect(self.prev_song)
        self.prevButton.setEnabled(False)
        controlLayout.addWidget(self.prevButton)
        
        
        self.playStopButton = QPushButton()
        self.playStopButton.setIcon(self.play_icon)
        self.playStopButton.clicked.connect(self.play_stop_song)
        self.playStopButton.setEnabled(False)
        controlLayout.addWidget(self.playStopButton)
        
        
        self.nextButton = QPushButton()
        self.nextButton.setIcon(self.next_icon)
        self.nextButton.clicked.connect(self.next_song)
        self.nextButton.setEnabled(False)
        controlLayout.addWidget(self.nextButton)
        
        self.windowDownloader = QPushButton()
        self.windowDownloader.setIcon(self.downloader_icon)
        # self.windowDownloader.clicked.connect(self.next_song)
        utilsLayout.addWidget(self.windowDownloader)
        
        layout.addLayout(controlLayout)
        layout.addLayout(utilsLayout)
        
        
        self.volumeSlider = QSlider(orientation=Qt.Horizontal)
        self.volumeSlider.setRange(0, 100)
        self.volumeSlider.setValue(50)
        self.volumeSlider.valueChanged.connect(self.change_volume)
        layout.addWidget(self.volumeSlider)
        
        
        self.setLayout(layout)
        
        
        self.timer = QTimer(self)
        self.timer.setInterval(50)  # Update every 1 second
        self.timer.timeout.connect(self.update_slider_position)
        self.timer.start()


    def printInfoLabel(self, text):
        self.statusLabel.setText(text)
        
    
    def printDataLabel(self, text):
        self.dataLabel.setText(text)
        
        
    def seek_position(self, position):
        if self.media_player.mediaStatus() == QMediaPlayer.MediaStatus.LoadedMedia:
            self.media_player.setPosition(int(position * self.media_player.duration() / 100))
        else:
            self.positionSlider.setEnabled(False)
    
    def update_slider_position(self):
        if self.media_player.duration() != 0:
            self.positionSlider.setValue(int(self.media_player.position() * 100 / self.media_player.duration()))
        

    def open_folder(self):
        self.folder_path = QFileDialog.getExistingDirectory(self, "Open Folder")
        if self.folder_path:
            self.music_files = [f for f in os.listdir(self.folder_path) if f.endswith('.mp3') or f.endswith('.wav')]
            if self.music_files:
                self.playStopButton.setEnabled(True)
                self.prevButton.setEnabled(True)
                self.nextButton.setEnabled(True)
                self.current_song = 0
                self.play_song(self.music_files[self.current_song])
            else:
                self.printInfoLabel("No music files found in the folder.")


    def play_song(self, filename):
        self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(os.path.join(self.folder_path, filename))))
        self.media_player.play()
        self.playStopButton.setIcon(self.stop_icon)
        self.playing = True


    def play_stop_song(self):
        if self.playing:
            self.media_player.pause()
            self.playStopButton.setIcon(self.play_icon)
            self.playing = False
        else:
            self.media_player.play()
            self.playStopButton.setIcon(self.stop_icon)
            self.playing = True


    def prev_song(self):
        self.current_song = (self.current_song - 1) % len(self.music_files)
        self.media_player.stop()
        self.play_song(self.music_files[self.current_song])
        

    def next_song(self): 
        self.current_song = (self.current_song + 1) % len(self.music_files)
        self.media_player.stop()
        self.play_song(self.music_files[self.current_song])


    def change_volume(self, value):
        self.media_player.setVolume(value)


    def printMediaData(self):
        if self.media_player.mediaStatus() == 6:
            if self.media_player.isMetaDataAvailable():
                title = self.media_player.metaData("Title")
                author = self.media_player.metaData("Author")
                
                self.printInfoLabel("Title: {}\nAuth: {}".format(title,author))
                
                print(f"Title: {title}, Author: {author}")
            else:
                print("no metaData available")