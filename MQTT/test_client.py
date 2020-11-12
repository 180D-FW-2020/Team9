#Author: Karunesh Sachanandani
import time
import random
import json
from paho.mqtt import client as mqtt_client
broker = 'mqtt.eclipse.org'
port = 1883
topic = "/ECE180DA/Team9"
client_id = 'python-mqtt'+str(random.randint(0, 1000))


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    # Set Connecting Client ID
    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def publish(client):
     msg_count = 0
     while True:
         time.sleep(1)
         with open('musicInfo.json') as musicfile:
             musicjson = json.load(musicfile)
             musicstr = json.dumps(musicjson) 
         msg = musicstr 
         result = client.publish(topic, msg)
         # result: [0, 1]
         status = result[0]
         if status == 0:
             print("Send " + msg +  " to topic " + topic)
         else:
             print("Failed to send message to topic " + topic)
         msg_count += 1

def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    run()
