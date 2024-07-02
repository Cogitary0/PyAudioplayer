from src.utils.parse import Settings
from PyQt5.QtWidgets import (QWidget, 
                             QVBoxLayout, 
                             QPushButton, 
                             QLabel,
                             QHBoxLayout,
                             QLineEdit,
                             QComboBox)


class SettingsWindow(QWidget):
    def __init__(self, style):
        super().__init__()

        self.settings = Settings('config\\settings.toml')
        self.setStyleSheet(style)
        self.setWindowTitle('Settings')

        self.settings_fields = [
            {"label": "Language:", 
             "key": 'language', 
             "type": str,
             "options": ["en", "ru"]},
            
            {"label": "Theme app:", 
             "key": 'theme', 
             "type": str,
             "options": ["light", "dark"]},
            
            {"label": "Interval to update music (ms):", 
             "key": 'interval_update_music', 
             "type": int},
            
            {"label": "Interval to move music (ms):", 
             "key": 'interval_move_music', 
             "type": int},
            
            {"label": "Start volume %:", 
             "key": 'def_volume', 
             "type": int},
            
            # {"label": "Volume [+/-] button:", 
            #  "key": ('btn_volume_up', 'btn_volume_down'), 
            #  "type": str},

            # {"label": "Music [+/-] button:", 
            #  "key": ('btn_music_plus', 'btn_music_minus'), 
            #  "type": str},
        ]

        self.init_ui()


    def init_ui(self):
        layout = QVBoxLayout()

        for field in self.settings_fields:
            
            hlayout = QHBoxLayout()
            label = QLabel(field["label"])
            hlayout.addWidget(label, stretch=3)
            
            if "options" in field:
                edit = QComboBox()
                edit.addItems(field["options"])
                edit.setCurrentText(str(self.settings.get(field["key"])))
                hlayout.addWidget(edit, stretch=1)
                self.settings_fields[self.settings_fields.index(field)]["edit"] = edit
                
            else:
                edit = QLineEdit(str(self.settings.get(field["key"] if not isinstance(field["key"], tuple) else field["key"])))
                hlayout.addWidget(edit, stretch=1)
                
                if isinstance(field["key"], tuple):
                    edit2 = QLineEdit(str(self.settings.get(field["key"])))
                    hlayout.addWidget(edit2, stretch=1)
                    self.settings_fields[self.settings_fields.index(field)]["edit"] = (edit, edit2)
                
                else:
                    self.settings_fields[self.settings_fields.index(field)]["edit"] = edit
                
            layout.addLayout(hlayout)

        save_button = QPushButton("Save")
        save_button.clicked.connect(self.saveSettings)
        layout.addWidget(save_button)

        self.setLayout(layout)


    def saveSettings(self):
        for field in self.settings_fields:
            if "options" in field:
                self.settings.set(field["key"], field["edit"].currentText())
                
            # elif isinstance(field["key"], tuple):
                # self.settings.set(field["key"], field["edit"].text())
                # self.settings.set(field["key"], field["edit"][1].text())
                # print(field["edit"][0],field["edit"][1], 2)
                
            else:
                self.settings.set(field["key"], field["type"](field["edit"].text()))
                
        self.close()