from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QWidget)
from src.utils.parse import Settings

class VolumeWindow(QWidget):
    def __init__(self, configPath, style):
        super().__init__()
        
        self.settings = Settings(configPath)
        
        self.setStyleSheet(style)
        self.init_ui()
    
    def init_ui(self):
        ...
        