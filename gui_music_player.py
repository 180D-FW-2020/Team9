from modules.music_player.vlc_audio_player import VLC_Audio_Player
from modules.music_player.music_dataframe import Music_Dataframe

from tkinter.filedialog import *
from tkinter import *

import random
import time

from threading import Timer, Thread, Event
import os

import subprocess

from modules.MQTT.transmitSong import MQTTTransmitter
from modules.MQTT.receiveSong import MQTTReceiver


class FrameApp(Frame):
    def __init__(self, parent):
        super(FrameApp, self).__init__(parent)

        self.grid()
        self.player = VLC_Audio_Player()
        self.df_songs = Music_Dataframe()
        self.transmitter = MQTTTransmitter()
        self.receiver = MQTTReceiver()

        self.emotion = 4
        self.emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}

        self.button_play_pause = Button(
            self, text="Play/Pause", command=self.play_pause_music, width=20)
        self.button_play_pause.grid(row=1, column=0)

        self.button_stop = Button(
            self, text="Stop", command=self.stop, width=20)
        self.button_stop.grid(row=2, column=0)

        self.button_previous = Button(self, text="Previous", command=self.previous_song,
                                      width=20)
        self.button_previous.grid(row=3, column=0)

        self.button_next = Button(
            self, text="Next", command=self.next_song, width=20)
        self.button_next.grid(row=4, column=0)

        self.button_add_songs = Button(self, text="Add Song Directory", command=self.add_to_list,
                                       width=20)
        self.button_add_songs.grid(row=5, column=0)

        self.button_add_songs = Button(self, text="Random Playlist", command=self.play_random_playlist,
                                       width=20)
        self.button_add_songs.grid(row=6, column=0)

        self.button_test = Button(self, text="Test Button", command=self.test,
                                  width=20)
        self.button_test.grid(row=7, column=0)

        self.button_test = Button(self, text="Transmit", command=self.transmit,
                                  width=20)
        self.button_test.grid(row=8, column=0)

        self.button_test = Button(self, text="Receive", command=self.receive,
                                  width=20)
        self.button_test.grid(row=9, column=0)

        self.button_emotion_detection = Button(
            self, text="Detect Emotion!", command=self.detect_user_emotion, width=20)
        self.button_emotion_detection.grid(row=10, column=0)

        self.export_csv = Button(
            self, text="Export Smartify Data", command=self.export_csv, width=20)
        self.export_csv.grid(row=11, column=0)

        self.import_csv = Button(
            self, text="Import Smartify Data", command=self.import_csv, width=20)
        self.import_csv.grid(row=12, column=0)

        self.label1 = Label(self)
        self.label1.grid(row=14, column=0)

        # TODO: Make progressbar, delete songs from playlist, amplify volume

        """
        Following code was modified from sample code to create the progress bar
        and OnTimer/scale_sel and ttkTimer class
        Author: Patrick Fay
        Date: 23-09-2015
        """
        # Progress Bar
        self.scale_var = DoubleVar()
        self.timeslider_last_val = ""
        self.timeslider = Scale(self, variable=self.scale_var,
                                from_=0, to=1000, orient=HORIZONTAL, length=500)
        # Update only on Button Release
        self.timeslider.bind("<ButtonRelease-1>", self.scale_sel)
        self.timeslider.grid(row=13, column=0)

        self.timer = ttkTimer(self.OnTimer, 1.0)
        self.timer.start()  # start Thread

    def OnTimer(self):
        """Update the time slider according to the current movie time.
        """
        if self.player == None:
            return
        # since the self.player.get_length can change while playing,
        # re-set the timeslider to the correct range.
        length = self.player.get_length()
        dbl = length * 0.001
        self.timeslider.config(to=dbl)

        # update the time on the slider
        tyme = self.player.get_time()
        if tyme == -1:
            tyme = 0
        dbl = tyme * 0.001
        self.timeslider_last_val = ("%.0f" % dbl) + ".0"
        self.timeslider.set(dbl)

    def scale_sel(self, evt):
        if self.player == None:
            return
        nval = self.scale_var.get()
        sval = str(nval)
        if self.timeslider_last_val != sval:
            mval = "%.0f" % (nval * 1000)
            self.player.set_time(int(mval))  # expects milliseconds

    def add_to_list(self):
        """
        Opens window to browse data on disk and adds selected songs (no directories) to playlist
        :return: None
        """
        music_directory = askdirectory()
        # appends song directory on disk to playlist in memory

        # adds songs into dataframe
        self.df_songs.load(music_directory)

    def play(self):
        """
        Plays current song. Does nothing if the song is currently being played.
        """
        self.player.play()

    def pause(self):
        """
        Pause current song. Does nothing if the song is already paused.
        """
        self.player.pause()

    def play_pause_music(self):
        """
        Plays Current Song
        :return: None
        """
        if self.player.is_playing():
            self.player.pause()
        else:
            self.player.play()

    def stop(self):
        """
        Stops current song
        :return: None
        """
        self.player.stop()

    def next_song(self):
        """
        Plays next song
        :return: None
        """
        self.player.next()

    def previous_song(self):
        """
        Plays previous song
        :return: 
        """
        self.player.previous()

    def check_music(self):
        pass

    def play_random_playlist(self):
        random_playlist = self.create_random_playlist()
        self.player.addPlaylist(random_playlist)
        self.player.play()

    def create_random_playlist(self) -> list:
        """
        Creates a randomly generated playlist with ALL songs in the dataframe:
        Output - List containing paths to songs
        """
        random_ints = list(range(self.df_songs.size()))
        random.seed()
        random.shuffle(random_ints)
        random_playlist = []

        for i in random_ints:
            random_playlist.append(self.df_songs.Music.iloc[i]['path'])

        return random_playlist

    def test(self):
        """
        Whatever function we want to test
        """
        self.print_current_song_info()

    def transmit(self):
        """
        Transmit song data via MQTT
        """
        (song_metadata, songtime) = self.get_info_current_song()
        songname = song_metadata.title
        artistname = song_metadata.artist

        self.transmitter.setSongname(songname)
        self.transmitter.setArtistname(artistname)
        self.transmitter.setSongtime(songtime)
        self.transmitter.setCommand("INPUTSONG")

        client = self.transmitter.connect_mqtt()
        client.loop_start()
        self.transmitter.publish(client)
        client.loop_stop()

    def receive(self):
        """
        Receive song data from MQTT and play that song if possible
        """
        client = self.receiver.connect_mqtt()
        self.receiver.subscribe(client)
        client.loop_start()
        time.sleep(0.5)
        # without the above pause, the program doesn't have enough time to subscribe and pick up the song info before the comm link is ended
        client.loop_stop()
        command = self.receiver.getCommand()
        songname = self.receiver.getSongname()
        artistname = self.receiver.getArtistname()
        songtime = int(self.receiver.getSongtime())
        print(str(command) + ", " + str(songname) + ", " +
              str(artistname) + ", " + str(songtime))

        #Python has no switch statements, I could use a dict, but we can talk about this later
        if command == "INPUTSONG":
        	self.play_song(songname, artist=artistname, start_time=int(songtime))
        elif command == "PLAY":
            self.play()
        elif command == "PAUSE":
            self.pause()
        elif command == "TOGGLE":
            self.play_pause_music()
        elif command == "SKIPTIME":
            self.skip_time(int(songtime)*1000) #time to skip is in ms
        elif command == "NEXT":
            self.next_song()
        elif command == "PREV":
            self.previous_song()
        else: #command not recognized
            print("Command not Recognized!")


    def play_song(self, title, artist=None, start_time=0):
        """
        Looks up song given title and artist. 
        If the song is not found in local directory, nothing plays (Prints a message)
        Otherwise, the song is played from the current playlist (if it is on the playlist)
        If the song is not on current playlist, a random playlist is generated (with the song), and is played
        """

        song_path = self.df_songs.find_song(title=title, artist=artist)

        if song_path == None:
            print("Song Not Found!")
            return
        else:
            played = self.player.play_song_from_current_playlist(
                song_path, start_time=start_time)
            if not played:  # song not in playlist or can't play for some reason
                self.play_random_playlist()  # random playlist of ALL songs
                self.player.set_time(start_time)

    def get_info_current_song(self):
        """
        returns (title, artist, time_in_ms)
        Note: If no metadata is found, title and artist will be returned as None
        """
        curr_song_path, time_in_ms = self.player.get_path_and_time()

        curr_song_metadata = self.df_songs.get_metadata_tag(curr_song_path)

        return (curr_song_metadata, time_in_ms)

    def print_current_song_info(self):
        """
        Prints information from get_info_current_song()
        returns nothing
        """

        song_tag, curr_time = self.get_info_current_song()
        curr_title = song_tag.title
        curr_artist = song_tag.artist

        print("Title: %s Artist: %s Time: %.2fsec" %
              (curr_title, curr_artist, curr_time/1000))
    
    def skip_time(self, time_to_skip=5000): #time to skip in ms
        current_time = self.player.get_time()
        self.player.set_time(current_time + time_to_skip)

    def detect_user_emotion(self):
        """
        Opens a subprocess to detect emotion from user (from a webcam)
        returns: nothing
        """

        #This currenty does freezes TK inter!
        #Make it use Threads later (along with MQTT)
        self.player.stop()

        print("Please wait for our module to load...")
        print("Please place your face near the camera.")

        process = subprocess.Popen(["python", "./modules/emotionDetection/emotions.py", "--mode", "display"])
        process.wait()
        
        self.emotion = process.returncode

        print("Your Emotion is:", self.emotion_dict[self.emotion])
        print("Recommending Songs based on your Emotion!")

        self.play_emotion_playlist()

    def play_emotion_playlist(self, num_songs=20):
        """
        Creates a random playlist of a song matching the emotions
        With songs with matching emotion
        If matching songs < num_songs, playlist will contain all matching songs
        """

        emotion_playlist = self.df_songs.find_emotion_songs(self.emotion)
        random.shuffle(emotion_playlist)

        if len(emotion_playlist) > num_songs:
            emotion_playlist = emotion_playlist[:num_songs]

        if len(emotion_playlist) == 0:
            print("No songs matching your current emotion! Try adding more songs!")

        self.player.addPlaylist(emotion_playlist)
        self.player.play()

    def export_csv(self):
        """
        Returns .csv of Dataframe
        """
        self.df_songs.export_csv(file_path="./Smartify_Data.csv")
    
    def import_csv(self):
        """
        Sets Dataframe values to equal the .csv file, if the columns are valid
        """
        df_file = askopenfile()
        self.df_songs.import_csv(file_path=df_file)


class ttkTimer(Thread):
    """a class serving same function as wxTimer... but there may be better ways to do this
    """

    def __init__(self, callback, tick):
        Thread.__init__(self)
        self.callback = callback
        #print("callback= ", callback())
        self.stopFlag = Event()
        self.tick = tick
        self.iters = 0

    def run(self):
        while not self.stopFlag.wait(self.tick):
            self.iters += 1
            self.callback()
            #print("ttkTimer start")

    def stop(self):
        self.stopFlag.set()

    def get(self):
        return self.iters


def _quit():
    print("Closing App...")
    root = Tk()
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
    # Fatal Python Error: PyEval_RestoreThread: NULL tstate
    os._exit(1)


if __name__ == '__main__':
    root = Tk()
    root.geometry("500x500")
    root.protocol("WM_DELETE_WINDOW", _quit)
    app = FrameApp(root)
    app.mainloop()
