import tkinter as tk
import audioplayer
import os
import time
import fnmatch

class SimpleMusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.geometry("300x50")

        self.bg_dark = '#2e2e2e'
        self.fg_white = 'white'
        self.btn_dark = '#3c3c3c'
        self.active_bg = '#4a4a4a'

        self.root.config(bg=self.bg_dark)

        self.player = None
        self.current_song_index = 0
        self.songs = []

        self.music_directory = "."
        self.allowed_extensions = ["*.mp3", "*.wav"]

        self.load_songs_from_directory(self.music_directory)

        if not self.songs:
            self.songs = ["No songs available"]
            self.current_song_index = -1
        else:
             self.songs.sort()

        self.is_playing = False

        self.create_widgets()
        self.update_window_title()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def load_songs_from_directory(self, directory):
        self._scan_directory(directory)

    def _scan_directory(self, current_dir):
        try:
            try:
                items = os.listdir(current_dir)
            except OSError:
                pass

            for item_name in items:
                item_path = os.path.join(current_dir, item_name)

                if os.path.isdir(item_path):
                    self._scan_directory(item_path)
                elif os.path.isfile(item_path):
                    for pattern in self.allowed_extensions:
                        if fnmatch.fnmatch(item_path.lower(), pattern.lower()):
                            self.songs.append(item_path)
                            break

        except Exception:
            pass

    def create_widgets(self):
        control_frame = tk.Frame(self.root, bg=self.bg_dark)
        control_frame.pack(pady=5)

        state = tk.NORMAL if self.current_song_index != -1 else tk.DISABLED

        self.prev_button = tk.Button(
            control_frame,
            text="Prev",
            command=self.prev_song,
            state=state,
            bg=self.btn_dark, fg=self.fg_white, activebackground=self.active_bg, activeforeground=self.fg_white,
            borderwidth=1, relief=tk.FLAT
        )
        self.play_stop_button = tk.Button(
            control_frame,
            text="Play",
            command=self.toggle_play_stop,
            state=state,
            bg=self.btn_dark, fg=self.fg_white, activebackground=self.active_bg, activeforeground=self.fg_white,
            borderwidth=1, relief=tk.FLAT
        )
        self.next_button = tk.Button(
            control_frame,
            text="Next",
            command=self.next_song,
            state=state,
            bg=self.btn_dark, fg=self.fg_white, activebackground=self.active_bg, activeforeground=self.fg_white,
            borderwidth=1, relief=tk.FLAT
        )

        self.prev_button.grid(row=0, column=0, padx=5)
        self.play_stop_button.grid(row=0, column=1, padx=5)
        self.next_button.grid(row=0, column=2, padx=5)

    def load_song(self, index):
        if 0 <= index < len(self.songs):
            return self.songs[index]
        return None

    def play_song(self):
        if self.current_song_index == -1 or not self.songs or self.songs == ["No songs available"]:
            self.is_playing = False
            return

        if self.player:
            self.stop_song()

        song_path = self.load_song(self.current_song_index)

        if song_path and os.path.exists(song_path):
            try:
                time.sleep(0.05)
                self.player = audioplayer.AudioPlayer(song_path)
                self.player.play()
                self.is_playing = True
                self.play_stop_button.config(text="Stop")
                self.update_window_title()
            except Exception:
                self.player = None
                self.is_playing = False
                self.play_stop_button.config(text="Play")
                self.update_window_title("Error playing song")
        else:
            self.player = None
            self.is_playing = False
            self.play_stop_button.config(text="Play")
            self.update_window_title("Song file not found")

    def stop_song(self):
        if self.player:
            try:
                self.player.stop()
            except Exception:
                pass
            finally:
                try:
                   del self.player
                except AttributeError:
                   pass
                self.player = None
                self.is_playing = False
                self.play_stop_button.config(text="Play")

    def toggle_play_stop(self):
        if self.current_song_index == -1 or not self.songs or self.songs == ["No songs available"]:
             return

        if self.is_playing:
             self.stop_song()
        else:
            self.play_song()

    def prev_song(self):
        if not self.songs or self.current_song_index == -1 or self.songs == ["No songs available"]:
             return

        was_playing = self.is_playing

        self.stop_song()

        self.current_song_index = (self.current_song_index - 1) % len(self.songs)

        self.update_window_title()

        if was_playing:
            self.play_song()

    def next_song(self):
        if not self.songs or self.current_song_index == -1 or self.songs == ["No songs available"]:
             return

        was_playing = self.is_playing

        self.stop_song()

        self.current_song_index = (self.current_song_index + 1) % len(self.songs)

        self.update_window_title()

        if was_playing:
            self.play_song()

    def update_window_title(self, message=None):
        if message:
            window_title_suffix = message
        elif self.current_song_index != -1 and self.songs != ["No songs available"]:
            song_name = os.path.basename(self.songs[self.current_song_index])
            window_title_suffix = song_name
        else:
             window_title_suffix = "No songs loaded"

        prefix = "Playing: " if self.is_playing else ""
        self.root.title(f"{prefix}{window_title_suffix}")

    def on_closing(self):
        self.stop_song()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleMusicPlayer(root)
    root.mainloop()