# Music Player

A minimalist music player application built with Tkinter and pygame.mixer , featuring basic playback controls and a system tray icon.

## Features

*   Play, Stop, Previous, and Next track controls.
*   Scans the directory and subdirectories for MP3 and WAV files.
*   Dark theme.
*   Displays current song name in the window title.
*   System tray icon for hiding/showing and quitting the application.
*   Auto-plays next/previous track if currently playing.

## Requirements

*   Python 3.6+
*   The packages listed in `requirements.txt`

## Installation (Source Code)

1.  Clone the repository:
    ```shell
    git clone https://github.com/radda-ui/music-player.git
    cd music-player
    ```

2.  Install the required Python packages:
    ```shell
    pip install -r requirements.txt
    ```

## How to Run (Source Code)

1.  Place your music files (MP3, WAV) in the same directory as the script, or in subdirectories.
2.  Ensure the `icon.png` file is in the same directory as `music_player.py`.
3.  Run the script from your terminal:
    ```shell
    py music_player.py
    ```

## Building an Executable (Optional)

To create a standalone executable (like `.exe` on Windows) that doesn't require Python or the installed libraries on the target machine, you can use `PyInstaller`.

1.  Install PyInstaller:
    ```shell
    pip install pyinstaller
    ```
2.  Navigate to the project directory in your terminal.
3.  Run the PyInstaller command:
    ```shell
    pyinstaller --onefile --noconsole --icon=icon.png music_player.py
    ```
4.  The executable will be found in the `dist` folder.
