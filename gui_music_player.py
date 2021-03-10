from modules.music_player.vlc_audio_player import VLC_Audio_Player
from modules.music_player.music_dataframe import Music_Dataframe

from tkinter.filedialog import *
from tkinter import *

import random
import time

from threading import Timer, Thread, Event
import threading
import os
import sys

import subprocess

from modules.MQTT.transmitSong import MQTTTransmitter
import json
from paho.mqtt import client as mqtt_client

from modules.VoiceRecognition.speechGet import Voice_Recognition

import pafy
from youtubesearchpython import VideosSearch

running_subprocesses = []

pp_indicator = 0


class FrameApp(Frame):
    def __init__(self, parent):
        super(FrameApp, self).__init__(parent)

        # Setup window frame
        root.title("Smartify Player")
        root.geometry("470x320")

        # Configure menu bar
        smartify_menu = Menu(root)
        root.config(menu=smartify_menu)

        # Create menu bar items
        file_menu = Menu(smartify_menu)
        smartify_menu.add_cascade(label="File", menu=file_menu)

        file_menu.add_command(label="Add Song Directory",
                              command=self.add_to_list)
        file_menu.add_command(label="Clear Smartify Data",
                              command=self.clear_smartify_data)

        emotion_menu = Menu(smartify_menu)
        smartify_menu.add_cascade(label="Emotion", menu=emotion_menu)

        emotion_menu.add_command(
            label="Export Emotion Data", command=self.export_csv)
        emotion_menu.add_command(
            label="Import Emotion Data", command=self.import_csv)
        emotion_menu.add_command(
            label="Run Emotion Detection", command=self.thread_detect_user_emotion)

        player_menu = Menu(smartify_menu)
        smartify_menu.add_cascade(label="Player", menu=player_menu)

        player_menu.add_command(
            label="Play/Pause", command=self.play_pause_music)
        player_menu.add_command(label="Previous", command=self.previous_song)
        player_menu.add_command(label="Next", command=self.next_song)
        player_menu.add_command(label="Stop", command=self.stop)
        player_menu.add_command(label="Play Random Song",
                                command=self.play_random_playlist)

        self.grid(padx=20, pady=20)
        self.player = VLC_Audio_Player()
        self.df_songs = Music_Dataframe()
        self.df_songs.import_csv(".smartify.csv")  # import from default path

        self.voice = Voice_Recognition()
        self.voice_thread = Thread(target=self.speechGet)
        self.voice_on = False

        # Default Topic for MQTT is "/ECE180DA/Team9/"
        self.default_topic = "/ECE180DA/Team9/"

        # MQTT Transmitter (from MQTT module)
        self.transmitter = MQTTTransmitter()
        self.transmitter_client = self.transmitter.connect_mqtt()
        self.transmit_msg = False

        self.transmitter_thread = Thread(target=self.transmit)

        # MQTT Receiver (Inside the player itself)
        # These are variables to initialize the Receiver
        self.receive_msg = False
        self.broker = 'broker.emqx.io'
        self.receiver_topic = self.default_topic
        self.client_id = 'python-mqtt'+str(random.randint(0, 1000))

        self.client = self.initialize_mqtt()  # connect to broker and subscribe

        self.emotion = 4
        self.emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful",
                             3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}

        # --------------
        # GUI code below
        # --------------

        self.button_transmit = Button(
            self, text="Transmitter: OFF", command=self.thread_transmit, width=12)
        self.button_transmit.grid(row=1, column=0)
        self.TChannel = Entry(self, width=14)
        self.TChannel.grid(row=2, column=0)
        self.button_TChannel = Button(
            self, text="Load", command=self.transmit_channel, width=12)
        self.button_TChannel.grid(row=3, column=0)

        self.button_receive = Button(
            self, text="Receiver: OFF", command=self.receive, width=12)
        self.button_receive.grid(row=1, column=2)
        self.RChannel = Entry(self, width=14)
        self.RChannel.grid(row=2, column=2)
        self.button_RChannel = Button(
            self, text="Load", command=self.receive_channel, width=12)
        self.button_RChannel.grid(row=3, column=2)

        self.button_emotion_detection = Button(
            self, text="Detect Emotion", command=self.thread_detect_user_emotion, width=12)
        self.button_emotion_detection.grid(row=4, column=0)

        # Voice recognition
        # row 4, column 2
        self.button_voice = Button(
            self, text="Voice Command", command=self.thread_voice, width=12)
        self.button_voice.grid(row=4, column=2)

        self.button_add_songs = Button(
            self, text="Shuffle", command=self.play_random_playlist, width=12)
        self.button_add_songs.grid(row=3, column=1)

        # Song name
        # row 5, column 0, columnspan 3

        self.button_play_pause = Button(
            self, text="▶️", command=self.play_pause_music, width=12)
        self.button_play_pause.grid(row=6, column=1)

        self.button_previous = Button(
            self, text="⏮", command=self.previous_song, width=12)
        self.button_previous.grid(row=6, column=0)

        self.button_next = Button(
            self, text="⏭", command=self.next_song, width=12)
        self.button_next.grid(row=6, column=2)

        self.button_stop = Button(self, text="⏹", command=self.stop, width=12)
        self.button_stop.grid(row=7, column=1)

        # Volume minus
        # row 7, column 0

        # Volume plus
        # row 7, column 2

        # self.button_add_songs = Button(self, text="Add Song Directory", command=self.add_to_list, width=20)
        # self.button_add_songs.grid(row=5, column=0)

        # self.button_test = Button(self, text="Test Button", command=self.test, width=20)
        # self.button_test.grid(row=8, column=0)

        # self.button_export_csv = Button(self, text="Export Smartify Data", command=self.export_csv, width=20)
        # self.button_export_csv.grid(row=11, column=0)

        # self.button_import_csv = Button(self, text="Import Smartify Data", command=self.import_csv, width=20)
        # self.button_import_csv.grid(row=12, column=0)

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

        self.timeslider = Scale(
            self, variable=self.scale_var, from_=0, to=1000, orient=HORIZONTAL, length=410)

        # Update only on Button Release
        self.timeslider.bind("<ButtonRelease-1>", self.scale_sel)
        self.timeslider.grid(row=15, column=0, columnspan=3)

        self.label1 = Label(self, text="Time Slider")
        self.label1.grid(row=16, column=1)

        self.timer = ttkTimer(self.OnTimer, 1.0)
        self.timer.start()  # start Thread

        self.volume_var = IntVar()

        self.volslider = Scale(self, variable=self.volume_var, command=self.volume_sel,
                               from_=0, to=100, orient=HORIZONTAL, length=410)

        self.volslider.grid(row=20, column=0, columnspan=3)

        self.label1 = Label(self, text="Volume Slider")
        self.label1.grid(row=21, column=1)

    """
    MQTT COMMANDS
    """

    def initialize_mqtt(self):
        """
        same as connect_mqtt() and subscribe_mqtt()
        returns client
        """
        client = self.connect_mqtt()
        self.subscribe_mqtt(client, self.receiver_topic)
        return client

    def connect_mqtt(self):
        """
        create MQTT client instance
        connect to MQTT broker:
        return: client instance (MQTT)
        """
        client = mqtt_client.Client(self.client_id)
        client.on_connect = self.on_connect
        try:
            client.connect(self.broker)  # default port is 1883
        except Exception as error:  # catch most exceptions, except few:
            # for details, check https://docs.python.org/3.5/library/exceptions.html#exception-hierarchy
            print('An exception occurred: {}'.format(error), file=sys.stderr)
            print("WARNING: Transmit and Receive Can't be used!")
        return client

    def subscribe_mqtt(self, client, topic):
        client.subscribe(topic)
        client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        """
        Prints Message when player is connected to MQtt
        """
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print(
                "Failed to connect to MQTT Broker, Transmit/Recieve will not work, return code %d\n", rc)

    def on_message(self, client, userdata, msg):
        """
        The function we call when we receive a message from MQTT broker
        """
        print(
            f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

        self.parse_command(json.loads(msg.payload.decode()))

    """
    END OF MQTT OOMMANDS
    """

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

    def volume_sel(self, evt):
        if self.player.listPlayer.get_media_player() == None:  # nothing being played
            return
        volume = self.volume_var.get()
        if self.player.audio_set_volume(volume) == -1:
            print("Failed to set volume")

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
        Note: this is different behavior from VLC-python's Pause which acts like "Toggle"
        """
        self.player.pause()

    def play_pause_music(self):
        """
        Plays song if Paused, Pauses song if Playing.
        """
        if self.player.is_playing():
            self.button_play_pause.configure(text="▶️")
            self.player.pause()
        else:
            self.button_play_pause.configure(text="⏸")
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

    def play_random_playlist(self):
        random_playlist = self.create_random_playlist()
        self.player.addPlaylist(random_playlist)
        self.player.play()

    def set_playlist_as_random_playlist(self):
        random_playlist = self.create_random_playlist()
        self.player.addPlaylist(random_playlist)

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
        self.player.change_volume(-10)

    def thread_transmit(self):
        """
        Sets self.transmit_msg to On/Off (Switch for Transmitter, not atomic)
        If transmitter is turned on, sends a message to client every interval.
        """
        if self.transmit_msg == True:
            self.transmit_msg = False
            self.button_transmit.configure(text="Trasmitter: OFF")
            print("Transmitter Turned Off")

        else:
            self.transmit_msg = True

            if not self.transmitter_thread.is_alive():
                # only start thread if thread is not alive
                self.transmitter_thread = Thread(target=self.transmit)
                self.transmitter_thread.start()

            self.button_transmit.configure(text="Trasmitter: ON")
            print("Transmitter Turned On")

    def transmit_channel(self):
        input = self.TChannel.get()
        self.transmitter.topic = self.default_topic + str(input)
        print("the transmitter channel name has been changed to: " +
              self.transmitter.topic)

    def transmit(self):
        """
        Transmit song data via MQTT every Interval (loops forever as long as tramsitter is on, use a thread)
        """
        while self.transmit_msg == True:
            (song_metadata, songtime) = self.get_info_current_song()

            if song_metadata is not None:
                songname = song_metadata.title
                artistname = song_metadata.artist

                self.transmitter.setSongname(songname)
                self.transmitter.setArtistname(artistname)
                self.transmitter.setSongtime(songtime)

                if self.player.is_playing():
                    self.transmitter.setCommand("INPUTSONG")
                else:
                    self.transmitter.setCommand("PAUSE")

                self.transmitter.publish(self.transmitter_client)

            time.sleep(3)  # Interval to sleep between each message

    def receive_channel(self):
        input = self.RChannel.get()
        # unsubscribe from previous topic
        self.client.unsubscribe(self.receiver_topic)

        self.receiver_topic = self.default_topic + \
            str(input)  # change topic of receiver
        self.client.subscribe(self.receiver_topic)
        print("the receiver channel name has been changed to: " + self.receiver_topic)

    def receive(self):
        """
        If Receiver is off: turns receiver on, player will parse any message received via MQTT
        If Recevier is on: turns receiver off

        Side note: on_message() calls parse_command, so we just need the MQTTclient to be on to parse commands
        """
        if self.receive_msg == False:
            self.client.loop_start()
            self.button_receive.configure(text="Receiver: Toggle ON")
            print("Receiver Turned On!")
            self.receive_msg = True
        else:
            self.client.loop_stop()
            self.button_receive.configure(text="Receiver: Toggle OFF")
            print("Receiver Turned Off!")
            self.receive_msg = False

    def parse_command(self, msg):
        """
        Parses commands given msg (dictionary), and calls correct functions accordingly
        """
        command = msg["command"]
        songname = msg["songname"]
        artistname = msg["artistname"]
        songtime = msg["songtime"]

        # Python has no switch statements, I could use a dict, but we can talk about this later
        if command == "INPUTSONG":
            # If song is same as current song being played
            (player_song_metadata, player_songtime) = self.get_info_current_song()

            if player_song_metadata is None:  # edge case with no song being played
                player_song_name = None
            else:
                player_song_name = player_song_metadata.title

            if player_song_name == songname:  # songname matches
                # only change timestamp of song when off by more than 5 sec.
                if abs(player_songtime - songtime) > 5000:
                    self.play_song(songname, artist=artistname,
                                   start_time=int(songtime))
            else:
                self.play_song(songname, artist=artistname,
                               start_time=int(songtime))

        elif command == "PLAY":
            self.play()
        elif command == "PAUSE":
            self.pause()
        elif command == "TOGGLE":
            self.play_pause_music()
        elif command == "SKIPTIME":
            self.skip_time(songtime)
        elif command == "NEXT":
            self.next_song()
        elif command == "PREV":
            self.previous_song()
        else:  # command not recognized
            print("Command not Recognized!")

    def play_song(self, title, artist=None, start_time=0):
        """
        Looks up song given title and artist. 
        If the song is not found in local directory, nothing plays (Prints a message)
        Otherwise, the song is played from the current playlist (if it is on the playlist)
        If the song is not on current playlist, a random playlist is generated (with the song), and is played
        """
        # Don't do anything on when given null
        if title is None:
            return

        song_path = self.df_songs.find_song(title=title, artist=artist)

        # CHANGE THIS LINE LATER S0 we can let user decide:
        self.enable_youtube_search = True

        if song_path == None:
            if self.enable_youtube_search:
                song_info = {'title': title, 'artist': artist}
                # search song on separate thread
                youtube_link = self.search_song_online(song_info)
                video = pafy.new(youtube_link)
                audio = video.getbestaudio()
                audio_link = audio.url

                self.df_songs.insert(audio_link, song_info)

                # Now play the song
                self.set_playlist_as_random_playlist()  # random playlist of ALL songs
                played = self.player.play_song_from_current_playlist(
                    audio_link, start_time=start_time)
            else:
                print("Song Not Found!")
                return
        else:
            played = self.player.play_song_from_current_playlist(
                song_path, start_time=start_time)
            if not played:  # song not in playlist or can't play for some reason
                self.set_playlist_as_random_playlist()  # random playlist of ALL songs
                played = self.player.play_song_from_current_playlist(
                    song_path, start_time=start_time)

    def thread_voice(self):
        """
        Sets self.voice_msg to On/Off
        If voice is turned on, gets a voice command from user until a valid one is received.
        """
        if self.voice_on == False:
                # do nothing if user presses button while we're currently getting the voice command
            self.voice_on = True
            if not self.voice_thread.is_alive():
                self.voice_thread = Thread(target=self.speechGet)
                self.voice_thread.start()

    def speechGet(self):
        print("Please enter your voice command.")
        self.voice.speechGet()
        voiceattempt = 0
        while self.voice.getCommand() == "ERROR" and voiceattempt < 2:
            print("Unrecognized input. Please enter your voice command again.")
            self.voice.speechGet()
            voiceattempt = voiceattempt + 1
        if self.voice.getCommand() == "ERROR":
            print(
                "Sorry, we couldn't hear anything from your mic. Please try again later.")
        else:
            print("Got it. We're on it now.")
            command_dict = self.voice.getDict()
            print(command_dict)
            self.parse_command(command_dict)
        self.voice_on = False

    def search_song_online(self, song_info):
        """
        input: song_info - dictionary of metadata
        returns: youtube_link of video (of Youtube video)
        """
        search_str = str(song_info['title']) + " " + str(song_info['artist'])

        song_search = VideosSearch(search_str, limit=5)

        video_link = song_search.result()['result'][0]['link']

        return video_link

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

    def skip_time(self, time_to_skip=5000):  # time to skip in ms
        current_time = self.player.get_time()
        self.player.set_time(current_time + time_to_skip)

    def thread_detect_user_emotion(self):
        """
        Same as detect_user_emotion(), but creates a new daemon thread
        and runs it on a separte thread (call this in the gui)
        """
        t = Thread(target=self.detect_user_emotion)
        t.start()

    def detect_user_emotion(self):
        """
        Opens a subprocess to detect emotion from user (from a webcam)
        returns: nothing
        """

        # Use Threads to prevent freezing;
        # Using thread.join() with this function seems to freeze GUI as well (most likely due to the subprocess, my guess)
        """
        print("In the Function")
        print("Main Thread:", threading.main_thread())
        print("Current Thread:", threading.current_thread())
        print("Current Thread Count:", threading.active_count())
        """

        print("Please wait for our module to load...")
        print("Please place your face near the camera.")

        emotion_subprocess = subprocess.Popen(
            ["python", "./modules/emotionDetection/emotions.py", "--mode", "display"])
        # add to list of running subprocesses
        running_subprocesses.append(emotion_subprocess)

        emotion_subprocess.wait()
        running_subprocesses.remove(
            emotion_subprocess)  # remove once completed

        self.emotion = emotion_subprocess.returncode

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

    def clear_smartify_data(self):
        self.df_songs = Music_Dataframe()


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
    for subprocess in running_subprocesses:
        subprocess.terminate()  # kill all running subprocesses

    app.df_songs.clear_all_youtube_links()
    app.df_songs.export_csv(file_path=".smartify.csv")

    root = Tk()
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
    # Fatal Python Error: PyEval_RestoreThread: NULL tstate
    os._exit(1)


if __name__ == '__main__':
    root = Tk()
    root.geometry("800x500")
    root.protocol("WM_DELETE_WINDOW", _quit)
    app = FrameApp(root)
    app.mainloop()
