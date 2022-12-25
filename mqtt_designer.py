import json
from paho.mqtt import client as mqtt_client

from Animation import *

class mqtt_designer:

    def __init__(self,broker= 'homeassistant.local',port= 1883,client_id= f'Fliptot designer',settings = "mqtt_config.cfg"):
        data = json.load(open(settings))
        self.animations = []
        self.images = []
        self.client = mqtt_client.Client(client_id)
        self.client.on_connect = self.on_connect
        self.client.username_pw_set(data["user"], data["password"])
        self.client.connect(broker, port)
        self.client.loop_start()

    def __del__(self):
        self.client.loop_stop()

    def on_connect(self):
        print("connected to broker")
        self.client.subscribe("Flipdot/assets")
        self.client.on_message = self.callback
        self.refresh_installed_assets()

    def send_image(self,image):
        self.client.publish("Flipdot/add_image", image.to_string())

    def display_image(self,image):
        self.client.publish("Flipdot/live", image.to_string())

    def send_animation(self,animation):
        self.client.publish("Flipdot/add_ani",animation.to_string())

    def refresh_installed_assets(self):
        self.client.publish("Flipdot/get_assets")

    def get_assets(self):
        return self.animations,self.images

    def callback(self,client,userdata,msg):
        data = json.loads(msg.msg.payload.decode())
        self.animations = data["Animations"]
        self.images = data["Images"]

