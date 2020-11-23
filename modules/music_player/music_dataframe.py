import pandas as pd
import os

from tinytag import TinyTag

class Music_Dataframe:
    def __init__(self, path = None):
        """Creates a dataframe. If path is specified, it loads songs from path into dataframe."""

        self.Music = pd.DataFrame(columns=['path', 'artist', 'title'])
        self.tags = dict()
        self.supported_format = [".mp3", ".wav"]

        if path is not None:
            self.load(path)
          
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

                    all_music_data.append(current_music_data)
                    self.tags[music_path] = tag

        #pd.append must be stored into a new place, otherwise nothing happens
        self.Music = self.Music.append(all_music_data, ignore_index = True)

    def print(self):
        print(self.Music)

    def size(self):
        return self.Music.shape[0]

