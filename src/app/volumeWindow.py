from src.utils.parse import Settings

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QWidget, 
                             QHBoxLayout, 
                             QPushButton, 
                             QSlider,
                             QLineEdit)




class VolumeWindow(QWidget):
    def __init__(self, settings, style):
        super().__init__()
        
        self.settings = settings
        
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setStyleSheet(style)
        self.setFixedSize(30,10)
        
        self.init_ui()
    
    def init_ui(self):
        __layout = QHBoxLayout()
        
        self.volumeSlide = QSlider()
        
        self.setLayout(__layout)

        