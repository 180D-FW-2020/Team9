# Project Smartify

## Team 9: Hyounjun Chang, Karunesh Sachanandani, Gerald Ko, Justin Suh

1. [Introduction](#introduction)
2. [Setup](#paragraph1)
    1. [Project Dependencies](#subparagraph1)
    2. [Issues](#subparagraph2)
3. [Others](#paragraph2)

## Introduction <a name="introduction"></a>
Smartify is an intelligent interactive player that plays the best smacking tunes at the right time in the right place for the users! It allows users to share playlists, and even control a speaker from thousands of miles away via Wi-Fi!

## Setup <a name="paragraph1"></a>
For the current state of the Project, these are the main components:

**Music Player** -> *gui_music_player.py*  
To run the player, simply run with *python gui_music_player.py*

**IMU controller** -> */modules/IMUControl/gesture.py* 
Run with *python -m IMUControl.gesture [optional_room_name]* with pwd(current directory) in /modules

**Voice Controller** -> */modules/VoiceRecognition/speechRun.py*  
Run with *python -m VoiceRecognition.speechRun [optional_room_name]* in /modules 

To use **Emotion_Detection** Feature in the Music Player, model.h5 is required.  
Link to the most recent version of model.h5 will be inside *modules/emotionDetection/EmotionDetection_README.md*  
Download the model.h5, and place it in *modules/emotionDetection/model.h5*

Setup/Project Dependencies Pages will be re-organized once it is finalized.

**If using Conda Environment**

Please use the command
*conda env create -f environment.yml*

or 

*conda env update -f environment.yml*

**There is an issue with PyAudio Library; Please install it manually!**

Windows:
There are many reported errors with installing Pyaudio on Windows:
If pip/conda install PyAudio does not work, please download it manually here
[Download Windows Binary](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)

and install the Pyaudio for python 3.8 matching the hardware (32bit, 64bit). (current version of PyAudio is 0.2.11)
Either *PyAudio‑0.2.11‑cp38‑cp38‑win_amd64.whl* OR *PyAudio‑0.2.11‑cp38‑cp38‑win32.whl*

After downloading, open your command line and type
pip install *file for pyaudio .whl*

Non-Windows:
*conda install PyAudio or pip install Pyaudio*

If you do not want to use a conda environment, please refer to Below in **Project Dependencies* 

## Project Dependencies <a name="subparagraph1"></a>

To run the following modules, these libraries are requried.

**Music Player:**
 
To use EmotionDetection functions from the Player, Install dependent libraries for MoodDetection as well.

- Python3 [Download Python](https://www.python.org/downloads/)
- VLC Media player (requires libvlc.dll) [Download VLC](https://www.videolan.org/vlc/)  
*Installation is required on player device (as python-vlc depends on the dll)*
 
- Conda Environment (optional, install below with conda instead over pip, if possible)
 
- python-vlc (pip install python-vlc)
- youtube-dl (pip install youtube_dl)
- pafy (pip install pafy)
- Youtube-Search-Python (pip install youtube-search-python)
- TinyTag (pip install tinytag)
- Pandas (pip install pandas)
- Speech_Recognition (pip install SpeechRecognition)
- PyAudio (pip install Pyaudio): may have problems on windows! 
- paho-mqtt (pip install paho-mqtt)

**There is an issue with PyAudio Library; Please install it manually!**

Windows:
There are many reported errors with installing Pyaudio on Windows:
If pip/conda install PyAudio does not work, please download it manually here
[Download Windows Binary](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)

and install the Pyaudio for python 3.8 matching the hardware (32bit, 64bit). (current version of PyAudio is 0.2.11)
Either *PyAudio‑0.2.11‑cp38‑cp38‑win_amd64.whl* OR *PyAudio‑0.2.11‑cp38‑cp38‑win32.whl*

After downloading, open your command line and type
pip install *file for pyaudio .whl*

Non-Windows:
*conda install PyAudio or pip install Pyaudio*

**Controller (IMU/Voice):** 
The controller was meant to be used on a RaspberryPi with BerryIMU. 

- Python3 [Download Python](https://www.python.org/downloads/)
- paho-mqtt (pip install paho-mqtt)

All other required libraries are in this git repository.

**Mood Detection:**
 
EmotionDectection Module (mood-based playlist) will not work without these modules (alongside those from Music Player)
 
- Python3 [Download Python](https://www.python.org/downloads/)
- Conda Environment (optional, also install all libraries from Music Player with conda or pip)
- Numpy (pip install numpy)
- OpenCV (pip install opencv-python), with conda (conda install opencv)
- Tensorflow (pip install tensorflow) WARNING: this libary is large, and will take a lot of space!

### Issues <a name="subparagraph2"></a>
 
**I can't load the player because of error with python-vlc!**
 
Package Manager may have difficulty locating libvlc.dll. If this is the case, please run the same version (32-bit or 64-bit) Python as on the version of VLC you installed.
 
**I don't hear Anything from the player!**
 
To insert a directory (where your songs are located),
 
Go to *Menu->File->Add Song Directory*: All songs (.mp3, .wav) files will be imported.
 
In order to play a song, we need to add songs to a playlist: Press on "Random Playlist" button, with (song directory added, or Smartify data imported) to play a random playlist of songs.

**How do I share songs/playlist with my friends?**
 
There are 2 sides of sharing a song: Sender and Listener
Sender: person sharing their playlist
Listener: person listening to another's playlist

If you are a *Sender*, Press on the button "Transmitter ON/OFF" to enable/disable this feature. A log will be written to command prompt for confirmation.
Set the room name accordingly by entering the room name *UNDER* the "Transmitter ON/OFF" button and clicking "load" on its right.

If you are a *Listener*, Press on the button "Receive ON/OFF" to enable/disable this feature. A log will be written to command prompt for confirmation.
Set the room name accordingly by entering the room name *UNDER* the "Receive ON/OFF" button and clicking "load" on its right.

**I am getting WARNINGS/ERRORS!**
 
Most of the warnings/errors are not critical errors that crash the program. In some cases, the warnings that gets fixed quickly and have no impact on the player (ie. audio buffer error, often lasts less than a second). If you are having issues using a feature, we recommend you restart the program.

## Others <a name="paragraph2"></a>
Any updates regarding setup will be updated on this README
