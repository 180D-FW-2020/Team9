# Project Smartify

## Team 9: Hyounjun Chang, Karunesh Sachanandani, Gerald Ko, Justin Suh

1. [Introduction](#introduction)
2. [Setup](#paragraph1)
    1. [Issues](#subparagraph1)
3. [Others](#paragraph2)

## Introduction <a name="introduction"></a>
Smartify is an intelligent interactive player that plays the best smacking tunes at the right time in the right place for the users! It allows users to share playlists, and even control a speaker from thousands of miles away via Wi-Fi!

## Setup <a name="paragraph1"></a>
There are 2 programs for this project: Music Player and Controller. 

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

**Controller:** (*try installing with conda before pip*)
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

### Issues <a name="subparagraph1"></a>
Current Known Issues:
Package Manager may have difficulty locating libvlc.dll. If this is the case, please run the same version (32-bit or 64-bit) Python as on the VLC 

## Others <a name="paragraph2"></a>
Any updates regarding setup will be updated on this README
