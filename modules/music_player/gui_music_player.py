from vlc_audio_player import VLC_Audio_Player
from music_dataframe import Music_Dataframe

from tkinter.filedialog import *
from tkinter import *

import random
import time
from threading import Timer,Thread,Event

class FrameApp(Frame):
    def __init__(self, parent):
        super(FrameApp, self).__init__(parent)

        self.grid()
        self.player = VLC_Audio_Player()
        self.df_songs = Music_Dataframe()

        self.button_play_pause = Button(self, text="Play/Pause", command=self.play_pause_music, width=20)
        self.button_play_pause.grid(row=1, column=0)

        self.button_stop = Button(self, text="Stop", command=self.stop, width=20)
        self.button_stop.grid(row=2, column=0)

        self.button_previous = Button(self, text="Previous", command=self.previous_song,
                         width=20)
        self.button_previous.grid(row=3, column=0)


        self.button_next = Button(self, text="Next", command=self.next_song, width=20)
        self.button_next.grid(row=4, column=0)

        self.button_add_songs = Button(self, text="Add Song Directory", command=self.add_to_list,
                         width=20)
        self.button_add_songs.grid(row=5, column=0)

        self.button_add_songs = Button(self, text="Random Playlist", command=self.random_playlist,
                         width=20)
        self.button_add_songs.grid(row=6, column=0)

        self.button_test = Button(self, text="Test Button", command=self.test,
                         width=20)
        self.button_test.grid(row=7, column=0)


        self.label1 = Label(self)
        self.label1.grid(row=9, column=0)

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
        self.timeslider = Scale(self, variable=self.scale_var, command=self.scale_sel, 
                from_=0, to=1000, orient=HORIZONTAL, length=500)
        self.timeslider.grid(row=8, column=0)
        self.timeslider_last_update = time.time()

        self.timer = ttkTimer(self.OnTimer, 1.0)
        self.timer.start()

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
        # don't want to programatically change slider while user is messing with it.
        # wait 2 seconds after user lets go of slider
        if time.time() > (self.timeslider_last_update + 2.0):
            self.timeslider.set(dbl)

    def scale_sel(self, evt):
        if self.player == None:
            return
        nval = self.scale_var.get()
        sval = str(nval)
        if self.timeslider_last_val != sval:
            self.timeslider_last_update = time.time()
            mval = "%.0f" % (nval * 1000)
            self.player.set_time(int(mval)) # expects milliseconds


    def add_to_list(self):
        """
        Opens window to browse data on disk and adds selected songs (no directories) to playlist
        :return: None
        """
        music_directory = askdirectory()
        # appends song directory on disk to playlist in memory
        
        # adds songs into dataframe
        self.df_songs.load(music_directory)



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

    def random_playlist(self):
        random_playlist = self.create_random_playlist()
        self.player.addPlaylist(random_playlist)

    def create_random_playlist(self) -> list:
        """
        Creates a randomly generated playlist:
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
        self.df_songs.print()


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

if __name__ == '__main__':
    root = Tk()
    root.geometry("350x500")
    app = FrameApp(root)
    app.mainloop()