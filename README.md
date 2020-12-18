# Project Smartify

## Team 9: Hyounjun Chang, Karunesh Sachanandani, Gerald Ko, Justin Suh

1. [Introduction](#introduction)
2. [Setup](#paragraph1)
    1. [Project Dependencies]
    2. [Issues](#subparagraph1)
3. [Others](#paragraph2)

## Introduction <a name="introduction"></a>
Smartify is an intelligent interactive player that plays the best smacking tunes at the right time in the right place for the users! It allows users to share playlists, and even control a speaker from thousands of miles away via Wi-Fi!

## Setup <a name="paragraph1"></a>
For the current state of the Project, these are the main components:

**Music Player** -> *gui_music_player.py*  
To run the player, simply run with *python gui_music_player.py*

**IMU controller** -> */modules/IMUControl/gesture.py* 
Run with *python -m IMUControl.gesture* with pwd(current directory) in /modules

**Voice Controller** -> */modules/VoiceRecognition/speechRun.py*  
Run with *python -m VoiceRecognition.speechRun* in /modules 

To use **Emotion_Detection** Feature in the Music Player, model.h5 is required.  
Link to the most recent version of model.h5 will be inside *modules/emotionDetection/EmotionDetection_README.md*  
Download the model.h5, and place it in *modules/emotionDetection/model.h5*

Setup/Project Dependencies Pages will be re-organized once it is finalized.

## Project Dependencies <a name="subparagraph1"></a>

**Music Player:**
- Python3 [Download Python](https://www.python.org/downloads/)
- VLC Media player (requires libvlc.dll) [Download VLC](https://www.videolan.org/vlc/)  
*Installation is required on player device (as python-vlc depends on the dll)*
- python-vlc (pip install python-vlc)
- pafy (pip install pafy)
- youtube-dl (pip install youtube_dl)
- Youtube-Search (pip install youtube-search)
- TinyTag (pip install tinytag)
- Pandas (pip install pandas)

**Controller (IMU/Voice):** (*try installing with conda before pip*)
- Python3 [Download Python](https://www.python.org/downloads/)
- Anaconda or Miniconda (Package Manger)
- OpenCV 
- paho-mqtt
- PyAudio (pip install PyAudio)
- Speech_Recognition (pip install SpeechRecognition)

**Mood Detection:**
- Python3
- Numpy
- OpenCV
- Tensorflow

### Issues <a name="subparagraph2"></a>
Current Known Issues:
Package Manager may have difficulty locating libvlc.dll. If this is the case, please run the same version (32-bit or 64-bit) Python as on the VLC 

## Others <a name="paragraph2"></a>
Any updates regarding setup will be updated on this README
