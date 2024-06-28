import customtkinter
from tkinter import filedialog
from pygame import mixer

class MusicPlayer(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("400x200")
        self.title("PyPy Musicplayer")

        self.mixer = mixer
        self.mixer.init()

        self.track = customtkinter.CTkLabel(self, text="No song playing")
        self.track.pack(pady=20)

        self.open_button = customtkinter.CTkButton(self, text="Open", command=self.open_file)
        self.open_button.pack(pady=10)

        self.play_button = customtkinter.CTkButton(self, text="Play", command=self.play_song)
        self.play_button.pack(pady=10)

        self.stop_button = customtkinter.CTkButton(self, text="Stop", command=self.stop_song)
        self.stop_button.pack(pady=10)

    def open_file(self):
        self.filename = filedialog.askopenfilename(filetypes=[('Audio Files', ['*.mp3', '*.wav'])])
        if self.filename:
            self.track.config(text=self.filename)

    def play_song(self):
        if self.filename:
            self.mixer.music.load(self.filename)
            self.mixer.music.play()

    def stop_song(self):
        self.mixer.music.stop()

