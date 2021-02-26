import pandas as pd
import os
import random

from tinytag import TinyTag

class Music_Dataframe:
    def __init__(self, path = None):
        """Creates a dataframe. If path is specified, it loads songs from path into dataframe."""

        self.Music_cols = ['path', 'artist', 'title', 'emotion']
        self.Music = pd.DataFrame(columns=self.Music_cols)
        self.tags = dict()
        self.supported_format = [".mp3", ".wav"]

        if path is not None:
            self.load(path)

    def insert(self, path, metadata_dict):
        """
        Inserts Dataframe given its input(path, dict of metadata)
        Does not add duplicates (based upon path) (same song, different Youtube link, will be added)
        """
        #Don't add duplicates
        if path in self.tags or path == None:
            return
        
        current_music_data = {}
        current_music_data['path'] = path
        current_music_data['title'] = metadata_dict["title"]
        current_music_data['artist'] = metadata_dict["artist"]
        current_music_data['emotion'] = random.randint(0,6) #random emotion for each song

        song_tag = TinyTag(None, 0) #File handler and file-size not-relevant for this program
        song_tag.artist = current_music_data['artist']
        song_tag.title = current_music_data['title']

        #pd.append must be stored into a new place, otherwise nothing happens
        self.Music = self.Music.append(current_music_data, ignore_index = True)
        self.tags[path] = song_tag
        
          
    #stores all music info from path
    def load(self, path):
        """Takes in path, updates DataFrame AND tags.
            If path is a music file, it adds that file only.
            If path is a directory, it adds all music files within that directory (recursive)
        """
        all_music_data = []

        #If path is actually a music file
        if os.path.splitext(path)[1] in self.supported_format:
            music_path = os.path.abspath(path)

            current_music_data = {}
            current_music_data['path'] = music_path

            #Don't add duplicates
            if music_path in self.tags:
                return

            tag = TinyTag.get(music_path)
            current_music_data['title'] = tag.title
            current_music_data['artist'] = tag.artist

            self.tags[music_path] = tag

            #pd.append must be stored into a new place, otherwise nothing happens
            self.Music = self.Music.append(current_music_data, ignore_index = True)

            return


        #If given file is directory:
        for root, dirs, files in os.walk(path):
            for filename in files:
                if os.path.splitext(filename)[1] in self.supported_format:
                    music_path = os.path.join(root, filename)
                    music_path = os.path.abspath(music_path)

                    current_music_data = {}
                    current_music_data['path'] = music_path

                    #Don't add duplicates
                    if music_path in self.tags:
                        continue

                    tag = TinyTag.get(music_path)
                    current_music_data['title'] = tag.title
                    current_music_data['artist'] = tag.artist

                    current_music_data['emotion'] = random.randint(0,6) #random emotion for each song

                    all_music_data.append(current_music_data)
                    self.tags[music_path] = tag

        #pd.append must be stored into a new place, otherwise nothing happens
        self.Music = self.Music.append(all_music_data, ignore_index = True)

    def print(self):
        print(self.Music)

    def size(self):
        return self.Music.shape[0]

    def find_song(self, title, artist=None):
        """
        Returns path (string) of the song if the song with same title is found in the database.
        If only title is given, only title is used for query; otherwise, both title and artist is used for query.
        It returns first entry if there are any non-zero number of matching entries, None otherwise.
        """
        if title is None:
            return None

        if artist != None:
            bool_matching_songs = self.Music['artist'].str.contains(artist, na=False, case=False) \
                 & self.Music['title'].str.contains(title, na=False, case=False)
        else:
            bool_matching_songs = self.Music['artist'].str.contains(artist, na=False, case=False)
        
        matching_songs = self.Music[bool_matching_songs]
        num_matches = matching_songs.shape[0]

        if num_matches == 0:
            return None
        else:
            return matching_songs.iloc[0]['path']
    
    def find_emotion_songs(self, emotion):
        """
        returns list [] of paths (string) of songs that mach the emotion
        """
        matching_songs = self.Music.loc[self.Music['emotion'] == emotion]['path'].tolist()

        return matching_songs

    def get_metadata_tag(self, song_path):
        """
        Returns tag(metadata) of song given the song path.
        Returns None if not found
        """
        try:
            ret_tag = self.tags[song_path]
        except KeyError:
            return None

        return ret_tag

    def export_csv(self, file_path="Smartify_Data.csv"):
        """
        Exports Dataframe as .csv to file_path
        """
        self.Music.to_csv(file_path,index=False)

    def import_csv(self, file_path):
        """
        Imports Dataframe as .csv from file_path if valid
        And sets self.tag to Tags of paths from .csv file
        Otherwise, it does nothing (prints message)
        """
        file_extension = os.path.splitext(file_path)[1]
        if not os.path.isfile(file_path) or file_extension != ".csv": #Do nothing if file doesn't exist or is not csv
            return

        temp_df = pd.read_csv(file_path)
        col_list = temp_df.columns.tolist()

        if col_list != self.Music_cols: #do nothing if columns don't match
           return
        else:
            self.Music = temp_df

        has_error = False

        #get all tags
        song_paths = self.Music['path'].tolist()
        for music_path in song_paths:
            file_extension = os.path.splitext(music_path)[1]
            if os.path.isfile(music_path) and file_extension in self.supported_format:
                tag = TinyTag.get(music_path)
                self.tags[music_path] = tag
            else: #file doesn't exist or not supported format
                has_error = True
                self.Music = self.Music[self.Music['path'] != music_path]

        self.clear_all_youtube_links()

        if has_error:
            print("Warning: Some music files found in .csv are missing/modified")

    def clear_all_youtube_links(self):
        """
        clears All Youtube links (and related tags)
        """
        bool_matching_songs = self.Music['path'].str.contains("https://")
        matching_songs = self.Music[bool_matching_songs]

        youtube_links = matching_songs['path'].to_list()

        for link in youtube_links:
            self.tags.pop(link, None)

        self.Music = self.Music[~bool_matching_songs]