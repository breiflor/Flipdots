# python 3.6


import time
import os

from paho.mqtt import client as mqtt_client


broker = 'homeassistant.local'
port = 1883
topic = "Flipdot/shutdown"
# generate client ID with pub prefix randomly
client_id = f'Fliptot watchdog'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.username_pw_set("mqttuser", "TODOPASSWORD")
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        print(os.system("sh /home/breiflor/Flipdot_demo/shutdown.sh"))
    client.subscribe(topic)
    client.on_message = on_message

def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
