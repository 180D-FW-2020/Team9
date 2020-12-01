import speech_recognition as sr


class Voice_Recognition:
    def __init__(self):
        # Command tells the music player what type of a command was entered by the user via an audio input
        self.Command = ""
        # CommandInfo is a list of additional fields that may be needed to perform the command
        self.CommandInfo = []

    def commandGet(self):
        return self.Command

    def commandInfoGet(self):
        return self.CommandInfo

    def speechGet(self):
        # print(sr.__version__)
        # 3.8.1
        rec = sr.Recognizer()
        mic = sr.Microphone()
        with mic as source:
            # wait a second for to adjust for ambient noise before inputting a voice command
            rec.adjust_for_ambient_noise(source)
            audio = rec.listen(source)
            strinput = rec.recognize_google(audio)
            # for an offline version use:
            # strinput = rec.recognize_sphinx(audio)
            # Karunesh: However the speech recognition seems much worse than the gooogle API
            strinput = strinput.lower()
            # convert string input into array of words
            wordsinput = strinput.split(" ")
            # check if command is play/pause
            if len(wordsinput) == 1 and wordsinput[0] == "pause":
                self.Command = "Pause"
                return
            if len(wordsinput) == 1 and wordsinput[0] == "play":
                self.Command = "Play"
                return
            # now to check if the user asked to play a certain song
            playind = -1
            byind = -1
            # find indices of 'play' and 'by' in order to pull out the song and artist names
            for i in range(0, len(wordsinput)):
                if playind == -1 and wordsinput[i] == "play":
                    playind = i
                if byind == -1 and wordsinput[i] == "by":
                    byind = i
            # if the command is of the format play ____ by ___
            if byind > playind + 1 and len(wordsinput) > byind + 1 and playind > -1:
                self.Command = "InputSong"
                songname = ""
                artistname = ""
                for i in range(playind + 1, byind):
                    songname = songname + wordsinput[i] + " "
                for i in range(byind + 1, len(wordsinput)):
                    artistname = artistname + wordsinput[i] + " "
                songname = songname[:-1]
                artistname = artistname[:-1]
                self.CommandInfo = [songname, artistname]
                return
            # check if the command is of the format skip ___ seconds
            if len(wordsinput) == 3 and wordsinput[0] == 'skip' and wordsinput[2] == 'seconds':
                self.Command = "SkipTime"
                self.CommandInfo = [wordsinput[1]]
                return
            # if no recognizable command is detected
            self.Command = "Error"
            self.CommandInfo = [strinput]
            return
