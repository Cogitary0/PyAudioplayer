import threading
import os
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, QTimer


class MediaPlaybackThread(threading.Thread):
    def __init__(self, media_player, folder_path, filename, position_slider):
        super().__init__()
        self.media_player = media_player
        self.folder_path = folder_path
        self.filename = filename
        self.position_slider = position_slider

    def run(self):
        self.media_player.stop()  # Остановка предыдущей песни
        url = QUrl.fromLocalFile(os.path.join(self.folder_path, self.filename))
        content = QMediaContent(url)
        self.media_player.setMedia(content)
        self.media_player.play()
        