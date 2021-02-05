# Author: Karunesh Sachanandani
# run this if you want to enter a voice command
# run with "python -m VoiceRecognition.speechRun" in /modules/ (For now!)
import sys
from MQTT.transmitSong import MQTTTransmitter
from VoiceRecognition.speechGet import Voice_Recognition
print("Please enter your voice command")
voiceInstance = Voice_Recognition()
transmitterInstance = MQTTTransmitter()
if len(sys.argv) == 2:
    topic = sys.argv[1]
    transmitterInstance.setTopic(topic)
voiceInstance.speechGet()
transmitterInstance.setCommand(voiceInstance.getCommand())
while voiceInstance.getCommand() == "Error":
    print("Unrecognized input. Please enter your voice command again.")
    voiceInstance.speechGet()
    transmitterInstance.setCommand(voiceInstance.getCommand())
transmitterInstance.setSongname(voiceInstance.getSongname())
transmitterInstance.setArtistname(voiceInstance.getArtistname())
transmitterInstance.setSongtime(voiceInstance.getSongtime())
client = transmitterInstance.connect_mqtt()
client.loop_start()
transmitterInstance.publish(client)
client.loop_stop()
