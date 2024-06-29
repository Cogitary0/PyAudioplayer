import threading
import os
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, QCoreApplication, Qt, QSize, QTimer


class MediaPlaybackThread(threading.Thread):
    def __init__(self, media_player, folder_path, filename, position_slider):
        threading.Thread.__init__(self)
        self.media_player = media_player
        self.folder_path = folder_path
        self.filename = filename
        self.position_slider = position_slider

    def run(self):
        self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(os.path.join(self.folder_path, self.filename))))
        self.media_player.play()
        while self.media_player.state() == QMediaPlayer.PlayingState:
            position = self.media_player.position()
            self.position_slider.setValue(position)
            QTimer.singleShot(25, lambda: None)  # Update the GUI every 100ms
