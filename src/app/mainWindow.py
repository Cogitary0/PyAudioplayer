import os
import time
import sys
from keyboard import add_hotkey
from PyQt5.QtCore import QSize, QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtMultimedia import QMediaPlayer
from src.app.musicPlayback import MediaPlaybackThread
from src.app.settingsWindow import SettingsWindow
from src.app.downloaderWindow import DownloaderWindow
from src.utils.parse import Settings, Language
from PyQt5.QtWidgets import (QWidget, 
                             QLabel, 
                             QVBoxLayout, 
                             QPushButton, 
                             QFileDialog, 
                             QProgressBar,
                             QHBoxLayout)


ICONS_PATH = 'src\\app\\assets\\icons\\'
STYLES_PATH = 'src\\app\\assets\\stylesheets\\'


class MainWindow(QWidget):
    
    def __init__(self, configPath, langPath):
        super().__init__()
        
        self.settings = Settings(configPath)
        self.lg = Language(langPath, self.settings.get('language')).get

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
        self.media_player.stateChanged.connect(self.media_state_changed)

        self.folder_path = self.settings.get('path_to_music')
        self.current_song = self.settings.get('current_song')
        self.music_duration = 0
        self.playing = False
        self.music_files = []
        self.audio_trigger = True

        self.init_ui()

        if self.folder_path:
            self.set_music()
        else:
            self.print_label(f" {self.lg('NoMeta')}")

    

    def init_ui(self):
        layout = QVBoxLayout()
        controlLayout = QHBoxLayout()
        utilsLayout = QHBoxLayout()

        self.statusLabel = QLabel()
        self.statusLabel.setFixedHeight(60)
        layout.addWidget(self.statusLabel)
        
        self.positionProgressBar = QProgressBar()
        self.positionProgressBar.setRange(0, 0)
        self.positionProgressBar.setValue(0)
        self.positionProgressBar.setTextVisible(False)
        self.position_plus_shortcut = add_hotkey(self.settings.get('btn_music_plus'), self.position_plus)
        self.position_plus_shortcut = add_hotkey(self.settings.get('btn_music_minus'), self.position_minus)
        layout.addWidget(self.positionProgressBar)
        
        self.volumeProgressBar = QProgressBar()
        self.volumeProgressBar.setRange(0, 100)
        self.volumeProgressBar.setValue(self.settings.get('def_volume'))
        self.volumeProgressBar.setTextVisible(False)
        self.volume_up_shortcut = add_hotkey(self.settings.get('btn_volume_up'), self.volume_up)
        self.volume_down_shortcut = add_hotkey(self.settings.get('btn_volume_down'), self.volume_down)
        layout.addWidget(self.volumeProgressBar)
        
        self.settingsButton = QPushButton()
        self.settingsButton.setIcon(self.settings_icon)
        self.settingsButton.clicked.connect(self.open_settings)
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
        self.windowDownloader.clicked.connect(self.open_downloader)
        utilsLayout.addWidget(self.windowDownloader, stretch=1)

        layout.addLayout(controlLayout)
        layout.addLayout(utilsLayout)

        self.setLayout(layout)
        self.enabled_widget(False)
        self.play_stop_song()
        
        self.timer = QTimer()
        self.timer.setInterval(self.settings.get('interval_update_music'))
        self.timer.timeout.connect(self.update_position_slider)
        self.timer.start()


    @staticmethod
    def get_style_file(nameStyle:str)->dict[str]:
        with open(f'{STYLES_PATH + nameStyle}.css', 'r') as styleFile:
            return styleFile.read()


    def print_label(self, text):
        self.statusLabel.setText(text)


    def enabled_widget(self, enabled: bool):
        if self.playing:
            self.playStopButton.setEnabled(enabled)
            self.prevButton.setEnabled(enabled)
            self.nextButton.setEnabled(enabled)
            self.positionProgressBar.setEnabled(enabled)


    def open_folder(self):
        self.folder_path = QFileDialog.getExistingDirectory(self, "Open Folder")
        if self.folder_path:
            self.set_music()
            
            
    def set_music(self):
        self.music_files = [f for f in os.listdir(self.folder_path) if f.endswith('.mp3') or f.endswith('.wav')]
        if self.music_files:
            self.enabled_widget(True)
            self.current_song = 0
            self.play_song(self.music_files[self.current_song])
            self.settings.set('path_to_music', self.folder_path)
            self.settings.set('current_song', self.current_song)
            self.settings.set("count_musics", len(self.music_files))
        else:
            self.print_label(f" {self.lg('NoMusicFiles')}.")


    def play_song(self, filename):    
        if self.playing:
            self.media_player.stop()
            
        self.media_player.setVolume(self.volumeProgressBar.value())
        
        thread = MediaPlaybackThread(self.media_player, 
                                     self.folder_path, 
                                     filename, 
                                     self.positionProgressBar)
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


    def media_state_changed(self, state):
        if state == QMediaPlayer.StoppedState and self.media_player.mediaStatus() == QMediaPlayer.EndOfMedia:
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
        self.volumeProgressBar.setValue(value)


    def print_media_data(self):
        if self.media_player.mediaStatus() == 6:
            if self.media_player.isMetaDataAvailable():
                title = self.get_music()
                # author = self.media_player.metaData('Author')
                self.print_label(" {}".format(title))
            else:
                self.print_label(f" {self.lg('NoMeta')}")


    def update_position(self, position):
        if self.playing:
            self.positionProgressBar.setValue(position)


    def update_duration(self, duration):
        self.positionProgressBar.setRange(0, duration)
        self.music_duration = duration


    def update_position_slider(self):
        position = self.media_player.position()
        self.positionProgressBar.setValue(position)
       
        
    def volume_up(self):
        current_volume = self.volumeProgressBar.value()
        if current_volume < 100:
            self.volumeProgressBar.setValue(current_volume + 1)
            self.media_player.setVolume(current_volume + 1)


    def volume_down(self):
        current_volume = self.volumeProgressBar.value()
        if current_volume > 0:
            self.volumeProgressBar.setValue(current_volume - 1)
            self.media_player.setVolume(current_volume - 1)
    
                
    def position_plus(self):
        if self.playing:
            position = self.media_player.position()
            self.media_player.pause()
            self.media_player.setPosition(position + self.settings.get('interval_move_music')) 
            self.media_player.play()


    def position_minus(self):
        if self.playing:
            position = self.media_player.position()
            self.media_player.pause()  
            self.media_player.setPosition(position - self.settings.get('interval_move_music'))
            self.media_player.play()
            
    
    def get_music(self):
        __max_len_text = 28
        __text = self.music_files[self.current_song].split('.')[0]
        return __text[:__max_len_text] + '...' if len(__text) > __max_len_text else __text[:__max_len_text]
            
            
    def open_settings(self):
        self.settings_window = SettingsWindow(self.get_style_file('settings'))
        self.settings_window.show()
    
            
    def open_downloader(self):
        self.downloader_window = DownloaderWindow(self.get_style_file('styles'), self.folder_path)
        self.downloader_window.destroyed.connect(self.set_music)
        self.downloader_window.show()