from src.utils.parse import Settings
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, QCoreApplication, Qt, QSize, QTimer
from PyQt5.QtGui import QColor, QPalette, QIcon
from PyQt5.QtWidgets import (QWidget, 
                             QVBoxLayout, 
                             QPushButton, 
                             QFileDialog, 
                             QLabel,
                             QHBoxLayout,
                             QShortcut,
                             QLineEdit)


class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.settings = Settings('config\\settings.toml')
        self.setStyleSheet(self.get_style_file('settings'))
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        intervalUpdateMusicLayout = QHBoxLayout()
        intervalMoveMusicLayout = QHBoxLayout()
        volumeUpEditLayout = QHBoxLayout()
        voumeUpLabelLayout = QHBoxLayout()
        volumeDownEditLayout = QHBoxLayout()
        volumeDownLabelLayout = QHBoxLayout()
        musicPlusEditLayout = QHBoxLayout()
        musicPlayLabelLayout = QHBoxLayout()
        musicMinusEditLayout = QHBoxLayout()
        musicMinusLabelLayout =QHBoxLayout()
        
    
        self.intervalUpdateMusicLabel = QLabel("Interval to update music (ms):")
        self.intervalUpdateMusicEdit = QLineEdit(str(self.settings.get('interval_update_music')))

        self.intervalMoveMusicLabel = QLabel("Interval to move music (ms):")
        self.intervalMoveMusicEdit = QLineEdit(str(self.settings.get('interval_move_music')))


        self.volumeUpLabel = QLabel("Volume up shortcut:")
        self.volumeUpEdit = QLineEdit(self.settings.get('btn_volume_up'))


        self.volumeDownLabel = QLabel("Volume down shortcut:")
        self.volumeDownEdit = QLineEdit(self.settings.get('btn_volume_down'))


        self.musicPlusLabel = QLabel("Music plus shortcut:")
        self.musicPlusEdit = QLineEdit(self.settings.get('btn_music_plus'))

        self.musicMinusLabel = QLabel("Music minus shortcut:")
        self.musicMinusEdit = QLineEdit(self.settings.get('btn_music_minus'))

        self.saveButton = QPushButton("Save")
        self.saveButton.clicked.connect(self.saveSettings)
        
        intervalUpdateMusicLayout.addWidget(self.intervalUpdateMusicLabel, stretch=3)
        intervalUpdateMusicLayout.addWidget(self.intervalUpdateMusicEdit, stretch=1)
        intervalMoveMusicLayout.addWidget(self.intervalMoveMusicLabel, stretch=3)
        intervalMoveMusicLayout.addWidget(self.intervalMoveMusicEdit, stretch=1)
        voumeUpLabelLayout.addWidget(self.volumeDownLabel, stretch=3)
        volumeUpEditLayout.addWidget(self.volumeUpEdit, stretch=1)
        volumeDownLabelLayout.addWidget(self.volumeDownLabel, stretch=3)
        volumeDownEditLayout.addWidget(self.volumeDownEdit, stretch=1)
        musicPlayLabelLayout.addWidget(self.musicPlusLabel, stretch=3)
        musicPlusEditLayout.addWidget(self.musicPlusEdit, stretch=1)
        musicMinusLabelLayout.addWidget(self.musicMinusLabel, stretch=3)
        musicMinusEditLayout.addWidget(self.musicMinusEdit, stretch=1)
        
        layout.addLayout(intervalUpdateMusicLayout)
        layout.addLayout(intervalMoveMusicLayout)
        layout.addLayout(volumeUpEditLayout)
        layout.addLayout(voumeUpLabelLayout)
        layout.addLayout(volumeDownEditLayout)
        layout.addLayout(volumeDownLabelLayout)
        layout.addLayout(musicPlusEditLayout)
        layout.addLayout(musicPlayLabelLayout)
        layout.addLayout(musicMinusEditLayout)
        layout.addLayout(musicMinusLabelLayout)

        layout.addWidget(self.saveButton)

        self.setLayout(layout)

    def saveSettings(self):
        self.settings.set('interval_update_music', int(self.intervalUpdateMusicEdit.text()))
        self.settings.set('interval_move_music', int(self.intervalMoveMusicEdit.text()))
        self.settings.set('btn_volume_up', self.volumeUpEdit.text())
        self.settings.set('btn_volume_down', self.volumeDownEdit.text())
        self.settings.set('btn_music_plus', self.musicPlusEdit.text())
        self.settings.set('btn_music_minus', self.musicMinusEdit.text())
        self.close()
        

    @staticmethod
    def get_style_file(nameStyle:str)->dict[str]:
        with open(f'src\\assets\\css\\{nameStyle}.css', 'r') as styleFile:
            return styleFile.read()