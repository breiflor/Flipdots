import json
import time

from paho.mqtt import client as mqtt_client

from Animation import *

class mqtt_designer:

    def __init__(self,broker= 'homeassistant.local',port= 1883,client_id= f'Fliptot designer',settings = "mqtt_config.cfg"):
        data = json.load(open(settings))
        self.animations = []
        self.images = []
        self.image = Image()
        self.animation = Animation()
        self.client = mqtt_client.Client(client_id)
        self.client.on_connect = self.on_connect
        self.client.username_pw_set(data["user"], data["password"])
        self.client.connect(broker, port)
        self.client.loop_start()

    def __del__(self):
        self.client.loop_stop()

    def on_connect(self,client, userdata, flags, rc):
        print("connected to broker")
        self.client.subscribe("Flipdot/assets")
        self.client.subscribe("Flipdot/download_animation")
        self.client.subscribe("Flipdot/download_image")
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

    def get_animations(self):
        return self.animations

    def get_images(self):
        return self.images

    def get_animation(self,name):
        self.client.publish("Flipdot/get_animation",name)
        print(name)
        time.sleep(3)
        return copy.deepcopy(self.animation)

    def remove_asset(self,name):
        print("removing "+str(name))
        self.client.publish("Flipdot/remove", name)

    def get_image(self,name):
        self.client.publish("Flipdot/get_image",name)
        print(name)
        time.sleep(3)
        return copy.deepcopy(self.image)

    def callback(self,client,userdata,msg):
        if(msg.topic == "Flipdot/assets"):
            data = json.loads(msg.payload.decode())
            self.animations = data["Animations"]
            self.images = data["Images"]
        elif msg.topic == "Flipdot/download_animation":
            self.animation.from_string(msg.payload.decode())
        elif msg.topic == "Flipdot/download_image":
            self.image.from_string(msg.payload.decode())
