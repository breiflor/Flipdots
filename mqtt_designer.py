import json
from paho.mqtt import client as mqtt_client

from Animation import *

class mqtt_designer:

    def __init__(self,broker= 'homeassistant.local',port= 1883,client_id= f'Fliptot designer',settings = "mqtt_config.cfg"):
        data = json.load(open(settings))
        self.client = mqtt_client.Client(client_id)
        self.client.on_connect = self.on_connect
        self.client.username_pw_set(data["user"], data["password"])
        self.client.connect(broker, port)
        self.client.loop_start()

    def __del__(self):
        self.client.loop_stop()

    def on_connect(self):
        print("connected to broker")

    def send_image(self,image):
        pass

    def display_image(self,image):
        pass

    def send_animation(self,animation):
        pass

    def get_installed_animations(self):
        pass
