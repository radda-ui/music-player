# changed to use pygame.mixer due an issue with audioplayer
# audioplayer is not thread-safe, has blocking .play(), no callback when it finish playing 
# added b64 icon to so that pystray use that and no need for real icon
import tkinter as tk
import os
import fnmatch
import pygame
import base64
import io
import threading
from pystray import Icon, MenuItem, Menu
from PIL import Image, ImageDraw

# Base64-encoded 64x64 icon PNG (white text "MP" on black background)
ICON_BASE64 = '''iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAMAAABg3Am1AAAAAXNSR0IArs4c6QAAABhQTFRF7u7u////AAAAWlpaMTExqqqqysrKg4ODQ8UruAAAAN1JREFUSImtVEEOwyAMAxfK/3/crtJWCDHE0pA4AHFiE0PKOSVv1ubvu5ufCRAAgwAslQqQKf1RA1QNBMAp+bKXAK/GipJWAyA1lpSAKmhoLqmlNR5empfqXGNnjVuG6CVDam/vgkPQMNSKabBPKQBItwhFwyxbBEQoYZ9/AJRT1SD2Iat9SHIfmualVMzZ3kvjWYBSJH//HgxgS+kM1vgCmj2bQs/ndzmiGip+gwCs1Hew6+gXCABYfpDr4ABGqFuWPr7Qlr4Lw0jTEMg/ALjH3Gvl4XOv6/28FsE5X2XyBlAFv4/iAAAAAElFTkSuQmCC
'''


class SimpleMusicPlayer:
    def __init__(self, root):
        self.root = root
        # Desired window size
        win_width, win_height = 300, 50
        self.root.geometry(f"{win_width}x{win_height}")

        # Position it bottom-right
        self.root.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = screen_width - win_width - 10  # 10 px from right edge
        y = screen_height - win_height - 50  # ~50 px from bottom for taskbar

        self.root.geometry(f"{win_width}x{win_height}+{x}+{y}")
        self.bg_dark = '#2e2e2e'
        self.fg_white = 'white'
        self.btn_dark = '#3c3c3c'
        self.active_bg = '#4a4a4a'
        self.root.config(bg=self.bg_dark)

        pygame.mixer.init()
        self.current_song_index = 0
        self.songs = []
        self.is_playing = False
        self.music_directory = "."
        self.allowed_extensions = ["*.mp3", "*.wav"]

        self.load_songs_from_directory(self.music_directory)
        if not self.songs:
            self.songs = ["No songs available"]
            self.current_song_index = -1

        self.create_widgets()
        self.update_window_title()
        self.root.protocol("WM_DELETE_WINDOW", self.hide_to_tray)

        self.icon = None
        self.create_tray_icon()

    def load_songs_from_directory(self, directory):
        for root_dir, _, files in os.walk(directory):
            for ext in self.allowed_extensions:
                for file in fnmatch.filter(files, ext):
                    self.songs.append(os.path.join(root_dir, file))
        self.songs.sort()

    def create_widgets(self):
        control_frame = tk.Frame(self.root, bg=self.bg_dark)
        control_frame.pack(pady=5)

        state = tk.NORMAL if self.current_song_index != -1 else tk.DISABLED

        self.prev_button = tk.Button(control_frame, text="Prev", command=self.prev_song,
                                     state=state, bg=self.btn_dark, fg=self.fg_white,
                                     activebackground=self.active_bg)
        self.play_stop_button = tk.Button(control_frame, text="Play", command=self.toggle_play_stop,
                                          state=state, bg=self.btn_dark, fg=self.fg_white,
                                          activebackground=self.active_bg)
        self.next_button = tk.Button(control_frame, text="Next", command=self.next_song,
                                     state=state, bg=self.btn_dark, fg=self.fg_white,
                                     activebackground=self.active_bg)

        self.prev_button.grid(row=0, column=0, padx=5)
        self.play_stop_button.grid(row=0, column=1, padx=5)
        self.next_button.grid(row=0, column=2, padx=5)

    def load_song(self, index):
        if 0 <= index < len(self.songs):
            return self.songs[index]
        return None

    def play_song(self):
        if self.current_song_index == -1:
            return

        pygame.mixer.music.stop()

        song_path = self.load_song(self.current_song_index)
        if song_path and os.path.exists(song_path):
            try:
                pygame.mixer.music.load(song_path)
                pygame.mixer.music.play()
                self.is_playing = True
                self.play_stop_button.config(text="Stop")
                self.update_window_title()
                self.check_music_end()
            except Exception:
                self.update_window_title("Error playing song")
        else:
            self.update_window_title("Song not found")

    def stop_song(self):
        pygame.mixer.music.stop()
        self.is_playing = False
        self.play_stop_button.config(text="Play")

    def toggle_play_stop(self, *args):
        if self.is_playing:
            self.stop_song()
        else:
            self.play_song()

    def prev_song(self, *args):
        if self.current_song_index > 0:
            self.current_song_index -= 1
        else:
            self.current_song_index = len(self.songs) - 1
        self.play_song()

    def next_song(self, *args):
        self.current_song_index = (self.current_song_index + 1) % len(self.songs)
        self.play_song()

    def check_music_end(self):
        if not pygame.mixer.music.get_busy() and self.is_playing:
            self.is_playing = False
            self.next_song()
        else:
            self.root.after(500, self.check_music_end)

    def update_window_title(self, message=None):
        if message:
            title = message
        elif self.current_song_index != -1:
            title = os.path.basename(self.songs[self.current_song_index])
        else:
            title = "No songs"
        prefix = "Playing: " if self.is_playing else ""
        self.root.title(prefix + title)

    def hide_to_tray(self):
        self.root.withdraw()

    def show_window(self, *args):
        self.root.after(0, self.root.deiconify)

    def quit_app(self, *args):
        self.stop_song()
        pygame.mixer.quit()
        if self.icon:
            self.icon.stop()
        self.root.quit()

    def create_tray_icon(self):
        try:
            img_data = base64.b64decode(ICON_BASE64)
            image = Image.open(io.BytesIO(img_data))
        except Exception:
            image = Image.new('RGB', (64, 64), color='black')
            draw = ImageDraw.Draw(image)
            draw.text((10, 20), "MP", fill='white')
        menu = Menu(
            MenuItem('▶ Play / Stop', self.toggle_play_stop),
            MenuItem('⏮ Prev', self.prev_song),
            MenuItem('⏭ Next', self.next_song),
            Menu.SEPARATOR,
            MenuItem('🪟 Show', self.show_window),
            MenuItem('❌ Hide', self.hide_to_tray),
            MenuItem('⛔ Quit', self.quit_app)
        )
        self.icon = Icon("SimpleMusicPlayer", image, "Music Player", menu)
        threading.Thread(target=self.icon.run, daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleMusicPlayer(root)
    root.mainloop()
