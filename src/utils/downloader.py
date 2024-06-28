from pytube import YouTube
from datetime import datetime

class Downloader:
    def __init__(self, url):
        self.url = url
        self.youtube = YouTube(self.url)
        self.title = "".join(str(self.youtube.title).split())
        self.filepathAudio = 'downloads\\audio'
        self.filepathVideo = 'downloads\\video'
    
    
    def downloadAudio(self)->str:
        audioId = self.getIdTime()
        filename = "{}_{}.mp3".format(self.title, audioId)
        self.youtube.streams.filter(only_audio=True).first().download(self.filepathAudio, filename)
        
        return filename
    
    
    def downloadVideo(self)->str:
        videoId = self.getIdTime()
        filename = "{}_{}.mp4".format(self.title, videoId)
        self.youtube.streams.filter(progressive=True, file_extension='mp4').first().download(self.filepathVideo, filename)
        
        return filename


    def getTitle(self)->str:
        return self.title
    
    
    @staticmethod
    def getIdTime()->str:
        return datetime.now().strftime("%Y%m%d%H%M%S")
    

        
