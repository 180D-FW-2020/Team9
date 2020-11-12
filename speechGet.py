import speech_recognition as sr
#print(sr.__version__)
#3.8.1
rec = sr.Recognizer()
mic = sr.Microphone()
with mic as source:
	rec.adjust_for_ambient_noise(source)
	#wait a second for the above function to adjust for ambient noise before inputting a voice command
	audio = rec.listen(source)
	strinput = rec.recognize_google(audio)
	wordsinput = strinput.split(" ")
	#convert string input to array of words
	playind = -1
	byind = -1
	#find indices of 'play' and 'by' in order to pull out the song and artist names
	for i in range(0, len(wordsinput)):
		if playind == -1 and wordsinput[i] == 'play':
			playind = i
		if byind == -1 and wordsinput[i] == 'by':
			byind = i
	if byind > playind + 1 and len(wordsinput) > byind + 1 and playind > -1:
		songname = ""
		artistname = ""
		for i in range(playind+1, byind):
			songname = songname + wordsinput[i] + " "
		for i in range(byind+1, len(wordsinput)):
			artistname = artistname + wordsinput[i] + " "
		songname = songname[:-1]
		artistname = artistname[:-1]
		#write to a text file
		speechfile = open("speechInput.txt", "w")
		speechfile.write(songname)
		speechfile.write('\n')
		speechfile.write(artistname)
		speechfile.close()






