from threading import Thread
from os.path import join
from PyQt5.QtMultimedia import QMediaContent
from PyQt5.QtCore import QUrl


class MediaPlaybackThread(Thread):
    def __init__(self, media_player, folder_path, filename, position_slider):
        super().__init__()
        self.media_player = media_player
        self.folder_path = folder_path
        self.filename = filename
        self.position_slider = position_slider


    def run(self):
        self.media_player.stop()  # Остановка предыдущей песни
        url = QUrl.fromLocalFile(join(self.folder_path, self.filename))
        content = QMediaContent(url)
        self.media_player.setMedia(content)
        self.media_player.play()
        