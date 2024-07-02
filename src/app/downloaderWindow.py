import sys
import os
from src.utils.parse import Settings
from src.utils.downloader import Downloader
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


class DownloaderWindow(QWidget):
    def __init__(self, style, path):
        super().__init__()
        
        self.setWindowTitle('Downloader')
        self.setStyleSheet(style)
        self.setFixedWidth(320)
        self.path = path
        self.is_download = False
        self.init_ui()
        
    
    def init_ui(self):

        layout = QVBoxLayout()

        self.urlInput = QLineEdit()
        layout.addWidget(self.urlInput)

        downloadAudioButton = QPushButton('Download Audio')
        downloadAudioButton.clicked.connect(self.download_audio)
        layout.addWidget(downloadAudioButton)
        
        downloadVideoButton = QPushButton("Download Video")
        downloadVideoButton.clicked.connect(self.download_video)
        layout.addWidget(downloadVideoButton)

        self.statusLabel = QLabel()
        layout.addWidget(self.statusLabel)

        self.setLayout(layout)

    
    def printLabel(self, text) -> None:
        self.statusLabel.setText(text)
    
    
    def download(self, is_audio) -> None:
        url = self.urlInput.text()
        
        try:
            if self.path:
                if url.startswith("https://www.youtube.com/watch?v="):
                    dl = Downloader(url, self.path)
                    
                    if is_audio:
                        dl.downloadAudio()
                        self.printLabel(' Audio downloaded successfully: {}'.format(dl.getTitle()))      

                    else:
                        dl.downloadVideo()
                        self.printLabel(' Video downloaded successfully: {}'.format(dl.getTitle()))
                
                else:
                    self.printLabel(' Invalid URL!')

            else:
                print('Invalid path')                
                
        except Exception as e:
            self.printLabel(f' Error: {str(e)}')
            
        self.close()


    def download_audio(self) -> None:
        self.download(True)
        

    def download_video(self) -> None:
        self.download(False)
        
