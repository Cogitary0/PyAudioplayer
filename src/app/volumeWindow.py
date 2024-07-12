from keyboard import add_hotkey
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QWidget, 
                             QHBoxLayout, 
                             QSlider,)




class VolumeWindow(QWidget):
    def __init__(self, media_player, current_volume, style):
        super().__init__()
        
        self.media_player = media_player
        self.current_volume = current_volume if current_volume != None else 0
        
        self.setStyleSheet(style)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setStyleSheet(style)
        self.setFixedSize(100,50)
        
        self.init_ui()
        
    
    def init_ui(self):
        layoutVolume = QHBoxLayout()
        
        self.volumeSlider = QSlider(Qt.Orientation.Horizontal, self)
        self.volumeSlider.setRange(0, 100)
        self.volumeSlider.setValue(self.current_volume)
        self.volumeSlider.valueChanged.connect(self.volume_change)
        layoutVolume.addWidget(self.volumeSlider)
        
        self.setLayout(layoutVolume)
        
    
    def volume_change(self):
        self.media_player.setVolume(self.volumeSlider.value())
        
        
    # def volume_up(self):
    #     current_volume = self.volumeSlider.value()
    #     if current_volume < 100:
    #         self.volumeSlider.setValue(current_volume + 1)
    #         self.media_player.setVolume(current_volume + 1)


    # def volume_down(self):
    #     current_volume = self.volumeSlider.value()
    #     if current_volume > 0:
    #         self.volumeSlider.setValue(current_volume - 1)
    #         self.media_player.setVolume(current_volume - 1)




        