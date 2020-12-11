"""
Shoutout to Pramod on stackoverflow
Related thread can be found on 
https://stackoverflow.com/questions/28440708/python-vlc-binding-playing-a-playlist
"""

import vlc
import time
import os

class VLC_Audio_Player:
    def __init__(self):
        self.Player = vlc.Instance()
        
        self.listPlayer = self.Player.media_list_player_new()
        self.listPlayer.set_playback_mode(vlc.PlaybackMode.loop) #loop if playlist over

        self.list_songpaths = []

        self.mediaList = self.Player.media_list_new()

    def addPlaylist(self, paths):
        """
        Creates a playlist of files in the paths
        Plays the first instance of playlist
        """

        self.listPlayer.stop() #stop the player to refresh
        self.clear_playlist() #clear playlist

        self.mediaList = self.Player.media_list_new()
        for path in paths:
            self.mediaList.add_media(self.Player.media_new(path))
            self.list_songpaths.append(path)
        
        #replace to current playlist
        self.listPlayer.set_media_list(self.mediaList)

        self.listPlayer.play()

    def play(self):
        self.listPlayer.play()
    def next(self):
        self.listPlayer.next()
    def pause(self):
        self.listPlayer.pause()
    def previous(self):
        self.listPlayer.previous()
    def stop(self):
        self.listPlayer.get_media_player().stop()

    def is_playing(self):
        """
        returns true if media is playing, false otherwise.
        """
        return bool(self.listPlayer.is_playing())

    def get_time(self):
        """
        returns time in ms in current media
        """
        return self.listPlayer.get_media_player().get_time()

    def set_time(self, ms):
        """
        sets time the current media to specified time
        """
        self.listPlayer.get_media_player().set_time(ms)

    def get_length(self):
        return self.listPlayer.get_media_player().get_length()
    
    def clear_playlist(self):
        """
        Empties vlc mediaList (object for playlist)
        """
        self.mediaList.release()
        self.mediaList = self.Player.media_list_new()
        self.list_songpaths.clear()

    def play_song_from_current_playlist(self, song_path, start_time=0):
        """
        Takes in path to song, plays the song if it is the current playlist.
        Returns True if song is being played
        Returns False if song is not in the playlist
        """
        try:
            index = self.list_songpaths.index(song_path)
        except ValueError:
            return False
        played = self.listPlayer.play_item_at_index(index)
        if (played == 0):
            self.set_time(start_time)
        
        return (played == 0) #exit code 0 if played no error


    def get_path_to_current_song(self):
        """
        returns path(location of file) being currently played
        """
        curr_media = self.listPlayer.get_media_player().get_media()
        index_of_media = self.mediaList.index_of_item(curr_media)

        return self.list_songpaths[index_of_media]

    def get_path_and_time(self):
        """
        Same as calling get_time() and get_path_to_current_song(), but
        more Time-Safe (media changing between these two calls)
        returns (path, time_in_ms)
        """
        curr_player = self.listPlayer.get_media_player()
        curr_time = curr_player.get_time()
        index_of_media = self.mediaList.index_of_item(curr_player.get_media())

        try:
            return (self.list_songpaths[index_of_media], curr_time)
        except IndexError:
            return ("", curr_time)