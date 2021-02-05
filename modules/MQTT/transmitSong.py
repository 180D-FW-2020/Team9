# Author: Karunesh Sachanandani
# To be used in conjunction with transmit() in gui_music_player.py
import time
import random
import json
from paho.mqtt import client as mqtt_client


class MQTTTransmitter:
    def __init__(self):
        #self.broker = 'mqtt.eclipse.org'
        self.broker = 'broker.emqx.io'
        self.port = 1883
        self.default_topic = "/ECE180DA/Team9/"
        self.topic = self.default_topic
        self.client_id = 'python-mqtt'+str(random.randint(0, 1000))
        self.command = None
        self.songname = None
        self.artistname = None
        self.songtime = 0

    def connect_mqtt(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("failed to connect, return code %d\n", rc)
        client = mqtt_client.Client(self.client_id)
        client.on_connect = on_connect
        client.connect(self.broker, self.port)
        return client

    def setCommand(self, command):
        self.command = command

    def setSongname(self, songname):
        self.songname = songname

    def setArtistname(self, artistname):
        self.artistname = artistname

    def setSongtime(self, songtime):
        self.songtime = songtime

    def setTopic(self, new_topic):
        self.topic = self.default_topic + new_topic

    def publish(self, client):
        msg_count = 0
        # without sleeping for 0.5 sec, the receiver cannot pick up the message
        time.sleep(0.5)
        msgstr = {}
        msgstr['command'] = self.command
        msgstr['songname'] = self.songname
        msgstr['artistname'] = self.artistname
        msgstr['songtime'] = self.songtime
        msg = json.dumps(msgstr)
        result = client.publish(self.topic, msg, 0, True)
        status = result[0]
        if status == 0:
            print("Send " + msg + " to topic " + self.topic)
        else:
            print("Failed to send message to topic " + self.topic)
        msg_count += 1
