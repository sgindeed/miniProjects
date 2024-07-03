import os
import tkinter as tk
from tkinter import filedialog
import pygame

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Music Player")
        
        self.playlist = []
        self.current_track = 0

        self.create_ui()
        pygame.mixer.init()

    def create_ui(self):
        # Create UI elements
        self.track_label = tk.Label(self.root, text="", font=("Helvetica", 12))
        self.track_label.pack(pady=10)

        self.play_button = tk.Button(self.root, text="Play", command=self.play_music)
        self.play_button.pack()
        
        self.stop_button = tk.Button(self.root, text="Stop", command=self.stop_music)
        self.stop_button.pack()
        
        self.prev_button = tk.Button(self.root, text="Previous", command=self.prev_track)
        self.prev_button.pack()
        
        self.next_button = tk.Button(self.root, text="Next", command=self.next_track)
        self.next_button.pack()

        self.load_button = tk.Button(self.root, text="Load Music", command=self.load_music)
        self.load_button.pack(pady=10)

    def load_music(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("MP3 Files", "*.mp3")])
        if file_paths:
            self.playlist = list(file_paths)
            self.current_track = 0
            self.play_music()

    def play_music(self):
        if self.playlist:
            track = self.playlist[self.current_track]
            pygame.mixer.music.load(track)
            pygame.mixer.music.play()
            self.track_label.config(text=os.path.basename(track))

    def stop_music(self):
        pygame.mixer.music.stop()
        self.track_label.config(text="")

    def prev_track(self):
        if self.playlist:
            self.current_track = (self.current_track - 1) % len(self.playlist)
            self.play_music()

    def next_track(self):
        if self.playlist:
            self.current_track = (self.current_track + 1) % len(self.playlist)
            self.play_music()

if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayer(root)
    root.mainloop()
