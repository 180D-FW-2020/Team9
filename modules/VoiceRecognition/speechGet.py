import speech_recognition as sr


class Voice_Recognition:
    def __init__(self):
        # Command tells the music player what type of a command was entered by the user via an audio input
        self.command = None
        self.songname = None
        self.artistname = None
        # any possible time value that may be required to process the command
        self.songtime = 0

    def getDict(self):
        voiceDict = {"command": self.command, "songname": self.songname,
                     "artistname": self.artistname, "songtime": self.songtime}
        return voiceDict

    def getCommand(self):
        return self.command

    def getSongname(self):
        return self.songname

    def getArtistname(self):
        return self.artistname

    def getSongtime(self):
        return self.songtime

    def speechGet(self):
        # print(sr.__version__)
        # 3.8.1
        rec = sr.Recognizer()
        mic = sr.Microphone()
        with mic as source:
            # wait a second for to adjust for ambient noise before inputting a voice command
            rec.adjust_for_ambient_noise(source)
            audio = rec.listen(source)
            try:
                strinput = rec.recognize_google(audio)
            except sr.UnknownValueError as error:
                print("Hmmm. We didn't hear anything.")
                self.command = "ERROR"
                return

            # for an offline version use:
            # strinput = rec.recognize_sphinx(audio)
            # Karunesh: However the speech recognition seems much worse than the gooogle API
            strinput = strinput.lower()
            print("We think you said: " + strinput)
            # convert string input into array of words
            wordsinput = strinput.split(" ")
            # check if command is play/pause
            if len(wordsinput) == 1 and wordsinput[0] == "pause":
                self.command = "PAUSE"
                return
            if len(wordsinput) == 1 and wordsinput[0] == "play":
                self.command = "PLAY"
                return
            if len(wordsinput) == 1 and wordsinput[0] == "next":
                self.command = "NEXT"
                return
            if len(wordsinput) == 1 and wordsinput[0] == "previous":
                self.command = "PREV"
                return
            # now to check if the user asked to play a certain song
            playind = -1
            byind = -1
            atind = -1
            secondsind = -1
            minutesind = -1
            # find indices of 'play' and 'by' in order to pull out the song and artist names
            for i in range(0, len(wordsinput)):
                if playind == -1 and wordsinput[i] == "play":
                    playind = i
                elif byind == -1 and wordsinput[i] == "by":
                    byind = i
                elif atind == -1 and wordsinput[i] == "at":
                    atind = i
                elif secondsind == -1 and wordsinput[i] == "seconds":
                    secondsind = i
                elif minutesind == -1 and (wordsinput[i] == "minutes" or wordsinput[i] == "minute"):
                    minutesind = i
                    # if the command is of the format play ____ by ___
            if byind > playind + 1 and len(wordsinput) > byind + 1 and playind > -1:
                self.command = "INPUTSONG"
                songname = ""
                artistname = ""
                songtime = 0
                artistendind = len(wordsinput)
                if (atind > -1):
                    artistendind = atind
                for i in range(playind + 1, byind):
                    songname = songname + wordsinput[i] + " "
                for i in range(byind + 1, artistendind):
                    artistname = artistname + wordsinput[i] + " "
                # if the command also says at ____ seconds (start at this time)
                if secondsind - atind == 2 and atind > byind + 1:
                    songtime = int(wordsinput[atind+1])*1000
                if minutesind - atind == 2 and atind > byind + 1:
                    if wordsinput[atind+1] == "one":
                        songtime = 1000*60
                    else:
                        songtime = int(wordsinput[atind+1])*1000*60
                self.songtime = songtime
                songname = songname[:-1]
                self.songname = songname
                artistname = artistname[:-1]
                self.artistname = artistname
                return
            # check if the command is of the format skip ___ seconds
            skipyes = False
            secminyes = False
            if wordsinput[0] == "skip" or wordsinput[0] == "forward":
                skipyes = True
            if secondsind == 2 or minutesind == 2:
                secminyes = True
            if len(wordsinput) == 3 and skipyes and secminyes:
                self.command = "SKIPTIME"
                if secondsind == 2:
                    self.songtime = int(wordsinput[1])*1000
                elif minutesind == 2:
                    if wordsinput[1] == "one":
                        self.songtime = 1000*60
                    else:
                        self.songtime = int(wordsinput[1])*1000*60
                return
            # if no recognizable command is detected
            self.command = "ERROR"
            return
