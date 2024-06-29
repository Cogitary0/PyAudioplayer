import sys
import os
import threading
import time
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, QCoreApplication, Qt, QSize, QTimer
from PyQt5.QtGui import QColor, QPalette, QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QSlider, QHBoxLayout, QProgressBar
from src.app.musicPlayback import MediaPlaybackThread
from src.app.settingsWindow import SettingsWindow
from src.app.downloaderWindow import DownloaderWindow
from src.utils.parse import Settings


ICONS_PATH = 'src\\assets\\icons\\'
STYLES_PATH = 'src\\assets\\css\\'

class MainWindow(QWidget):
    
    def __init__(self, configPath):
        super().__init__()
        
        self.settings = Settings(configPath)
        
        self.setWindowTitle('PyPy MusicPlayer')
        self.setFixedSize(QSize(self.settings.get('win_width'),
                                self.settings.get('win_height')))
        
        self.play_icon = QIcon(ICONS_PATH + 'play.png')
        self.stop_icon = QIcon(ICONS_PATH + 'stop.png')
        self.next_icon = QIcon(ICONS_PATH + 'next.png')
        self.prev_icon = QIcon(ICONS_PATH + 'prev.png')
        self.folder_icon = QIcon(ICONS_PATH + 'folderOpen.png')
        self.downloader_icon = QIcon(ICONS_PATH + 'downloader.png')
        self.settings_icon = QIcon(ICONS_PATH + 'settings.png')
        self.setStyleSheet(self.get_style_file('styles'))

        self.media_player = QMediaPlayer(None, QMediaPlayer.StreamPlayback)
        self.media_player.mediaStatusChanged.connect(self.print_media_data)
        self.media_player.positionChanged.connect(self.update_position)
        self.media_player.durationChanged.connect(self.update_duration)
        self.media_player.stateChanged.connect(self.mediaStateChanged)

        self.folder_path = self.settings.get('path_to_music')
        self.current_song = self.settings.get('current_song')
        self.playing = False
        self.music_files = []

        self.init_ui()

        if self.folder_path:
            self.music_files = [f for f in os.listdir(self.folder_path) if f.endswith('.mp3') or f.endswith('.wav')]
            if self.music_files:
                self.enabled_widget(True)
                self.play_song(self.music_files[self.current_song])
            else:
                self.print_label(" No music files found in the folder.")
        else:
            self.print_label(" No metadata available")

    

    def init_ui(self):
        layout = QVBoxLayout()
        controlLayout = QHBoxLayout()
        utilsLayout = QHBoxLayout()

        self.statusLabel = QLabel()
        self.statusLabel.setFixedHeight(60)
        layout.addWidget(self.statusLabel)
        
        self.positionSlider = QSlider(orientation=Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.valueChanged.connect(self.seek_position)
        self.positionSlider.setStyleSheet(self.get_style_file('slider'))
        layout.addWidget(self.positionSlider)
        
        self.volumeSlider = QSlider(orientation=Qt.Horizontal)
        self.volumeSlider.setRange(0, 100)
        self.volumeSlider.setValue(self.settings.get('def_volume'))
        # self.volumeSlider.setStyleSheet(self.get_style_file('slider'))
        self.volumeSlider.valueChanged.connect(self.change_volume)
        layout.addWidget(self.volumeSlider)
        
        self.settingsButton = QPushButton()
        self.settingsButton.setIcon(self.settings_icon)
        self.settingsButton.clicked.connect(self.open_folder)
        utilsLayout.addWidget(self.settingsButton, stretch=1)

        self.openFolderButton = QPushButton()
        self.openFolderButton.setIcon(self.folder_icon)
        self.openFolderButton.clicked.connect(self.open_folder)
        utilsLayout.addWidget(self.openFolderButton, stretch=4)

        self.prevButton = QPushButton()
        self.prevButton.setIcon(self.prev_icon)
        self.prevButton.clicked.connect(self.prev_song)
        controlLayout.addWidget(self.prevButton)

        self.playStopButton = QPushButton()
        self.playStopButton.setIcon(self.play_icon)
        self.playStopButton.clicked.connect(self.play_stop_song)
        controlLayout.addWidget(self.playStopButton)

        self.nextButton = QPushButton()
        self.nextButton.setIcon(self.next_icon)
        self.nextButton.clicked.connect(self.next_song)
        controlLayout.addWidget(self.nextButton)

        self.windowDownloader = QPushButton()
        self.windowDownloader.setIcon(self.downloader_icon)
        # self.windowDownloader.clicked.connect(self.next_song)
        utilsLayout.addWidget(self.windowDownloader, stretch=1)

        layout.addLayout(controlLayout)
        layout.addLayout(utilsLayout)

        self.setLayout(layout)
        self.enabled_widget(False)
        
        self.timer = QTimer()
        self.timer.setInterval(self.settings.get('interval_slider'))  # Update every 1 second
        self.timer.timeout.connect(self.update_position_slider)
        self.timer.start()
        

    @staticmethod
    def get_style_file(nameStyle:str)->dict[str]:
        with open(STYLES_PATH + nameStyle + '.css', 'r') as styleFile:
            return styleFile.read()
    

    def print_label(self, text):
        self.statusLabel.setText(text)


    def enabled_widget(self, enabled: bool):
        if self.playing:
            self.playStopButton.setEnabled(enabled)
            self.prevButton.setEnabled(enabled)
            self.nextButton.setEnabled(enabled)
            self.positionSlider.setEnabled(enabled)


    def open_folder(self):
        if self.folder_path:
            return
        self.folder_path = QFileDialog.getExistingDirectory(self, "Open Folder")
        if self.folder_path:
            self.music_files = [f for f in os.listdir(self.folder_path) if f.endswith('.mp3') or f.endswith('.wav')]
            if self.music_files:
                self.enabled_widget(True)
                self.current_song = 0
                self.play_song(self.music_files[self.current_song])
                self.settings.set('path_to_music', self.folder_path)
                self.settings.set('current_song', self.current_song)
            else:
                self.print_label(" No music files found in the folder.")


    def play_song(self, filename):
        if self.playing:
            self.media_player.stop()
            
        self.media_player.setVolume(self.volumeSlider.value())
        thread = MediaPlaybackThread(self.media_player, 
                                     self.folder_path, 
                                     filename, 
                                     self.positionSlider)
        thread.start()
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


    def mediaStateChanged(self, state):
        if state == QMediaPlayer.StoppedState:
            self.next_song()
            time.sleep(0.1)


    def prev_song(self):
        if len(self.music_files) > 0:
            self.current_song = (self.current_song - 1) % len(self.music_files)
            self.media_player.stop()
            self.play_song(self.music_files[self.current_song])
            self.settings.set('current_song', self.current_song)


    def next_song(self):
        if len(self.music_files) > 0:
            self.current_song = (self.current_song + 1) % len(self.music_files)
            self.media_player.stop()
            self.play_song(self.music_files[self.current_song])
            self.settings.set('current_song', self.current_song)


    def change_volume(self, value):
        self.media_player.setVolume(value)


    def print_media_data(self):
        if self.media_player.mediaStatus() == 6:
            if self.media_player.isMetaDataAvailable():
                title = self.media_player.metaData("Title")
                author = self.media_player.metaData("Author")

                self.print_label(" {}\n {}".format(title, author))

                print(f"Title: {title}, Author: {author}")
            else:
                self.printDataLabel(" No metadata available")
                print("no metaData available")


    def update_position(self, position):
        if self.playing:
            self.positionSlider.setValue(position)


    def update_duration(self, duration):
        self.positionSlider.setRange(0, duration)


    def update_position_slider(self):
        position = self.media_player.position()
        self.positionSlider.setValue(position)


    def seek_position(self, position):
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.media_player.setPosition(position)
            
            
    