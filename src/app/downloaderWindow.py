import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QSlider, QHBoxLayout
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, QCoreApplication, Qt, QSize, QTimer
from PyQt5.QtGui import QColor, QPalette, QIcon

class DownloaderWindow(QWidget):
    def __init__(self):
        super().__init__()