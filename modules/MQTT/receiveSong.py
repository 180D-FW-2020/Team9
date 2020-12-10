# Author: Karunesh Sachanandani
# To be used in conjunction with transmit() in music_player/gui_music_player.py
import random
import json
from paho.mqtt import client as mqtt_client
import time


class MQTTReceiver:
    def __init__(self):
        #self.broker = 'mqtt.eclipse.org'
        self.broker = 'broker.emqx.io'
        self.port = 1883
        self.topic = "/ECE180DA/Team9"
        self.client_id = 'python-mqtt'+str(random.randint(0, 1000))
        self.command = ""
        self.songname = ""
        self.artistname = ""
        self.songtime = 0

    def connect_mqtt(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)

        client = mqtt_client.Client(self.client_id)
        client.on_connect = on_connect
        client.connect(self.broker, self.port)
        return client

    def getCommand(self):
        return self.command

    def getSongname(self):
        return self.songname

    def getArtistname(self):
        return self.artistname

    def getSongtime(self):
        return self.songtime

    def subscribe(self, client):
        def on_message(client, userdata, msg):
            print(
                f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
            musicinfo = json.loads(msg.payload.decode())
            self.command = musicinfo['command']
            self.songname = musicinfo['songname']
            self.artistname = musicinfo['artistname']
            self.songtime = musicinfo['songtime']
        client.subscribe(self.topic)
        client.on_message = on_message
