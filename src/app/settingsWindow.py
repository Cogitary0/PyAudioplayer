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
        # self.setFixedSize(QSize(320,230))
        # self.setFixedHeight(230)
        
        self.settings_fields = [
            {"label": "Interval to update music (ms):", 
             "edit": QLineEdit(str(self.settings.get('interval_update_music'))), 
             "stretch": 1},
            
            {"label": "Interval to move music (ms):", 
             "edit": QLineEdit(str(self.settings.get('interval_move_music'))), 
             "stretch": 1},
            
            {"label": "Start volume:", 
             "edit": QLineEdit(str(self.settings.get('def_volume'))), 
             "stretch": 1},
            
            {"label": "Volume [+/-] button:", 
             "edit": QLineEdit(self.settings.get('btn_volume_up')), 
             "stretch": 1, 
             "second_edit": QLineEdit(self.settings.get('btn_volume_down'))},
            
            {"label": "Music [+/-] button:", 
             "edit": QLineEdit(self.settings.get('btn_music_plus')), 
             "stretch": 1, 
             "second_edit": QLineEdit(self.settings.get('btn_music_minus'))},
        ]
        
        self.init_ui()
        
        

    def init_ui(self):
        
        layout = QVBoxLayout()

        for field in self.settings_fields:
            
            hlayout = QHBoxLayout()
            label = QLabel(field["label"])
            hlayout.addWidget(label, stretch=3)
            hlayout.addWidget(field["edit"], stretch=field["stretch"])
            
            if "second_edit" in field:
                hlayout.addWidget(field["second_edit"], stretch=field["stretch"])
                
            layout.addLayout(hlayout)

        save_button = QPushButton("Save")
        save_button.clicked.connect(self.saveSettings)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def saveSettings(self):
        for field in self.settings_fields:
            if field["label"] == "Interval to update music (ms):":
                self.settings.set('interval_update_music', int(field["edit"].text()))
            elif field["label"] == "Interval to move music (ms):":
                self.settings.set('interval_move_music', int(field["edit"].text()))
            elif field["label"] == "Start volume:":
                self.settings.set('def_volume', int(field["edit"].text()))
            elif field["label"] == "Volume [+/-] button:":
                self.settings.set('btn_volume_up', field["edit"].text())
                self.settings.set('btn_volume_down', field["second_edit"].text())
            elif field["label"] == "Music [+/-] button:":
                self.settings.set('btn_music_plus', field["edit"].text())
                self.settings.set('btn_music_minus', field["second_edit"].text())
        self.close()

    @staticmethod
    def get_style_file(nameStyle:str)->dict[str]:
        with open(f'src\\assets\\css\\{nameStyle}.css', 'r') as styleFile:
            return styleFile.read()