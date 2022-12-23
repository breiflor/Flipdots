import time
import os
import json

from paho.mqtt import client as mqtt_client
from Display import *


class Net_Controller:

    def __init__(self,broker= 'homeassistant.local',port= 1883,client_id= f'Fliptot watchdog',settings = "mqtt_config.cfg"):
        data = json.load(open(settings))
        self.mode = None
        self.display = Display()
        self.display.white()
        animation = Animation("startup_animation/")
        self.display._play_animation(animation)
        #animation = Animation("Adventskranz/")
        #self.display._play_animation(animation)
        self.animation = None
        self.client = mqtt_client.Client(client_id)
        self.client.on_connect = self.on_connect
        self.client.username_pw_set(data["user"],data["password"])
        self.client.connect(broker,port)
        self.subcribe("Flipdot/shutdown",self.callback)
        self.subcribe("Flipdot/live",self.callback)
        self.subcribe("Flipdot/add_ani",self.callback)
        self.subcribe("Flipdot/add_image",self.callback)
        self.subcribe("Flipdot/remove",self.callback)
        self.subcribe("Flipdot/play",self.callback)
        self.subcribe("Flipdot/play_loop",self.callback)
        self.subcribe("Flipdot/clock",self.callback)
        self.subcribe("Flipdot/music",self.callback)
        self.run_state_machine()

    def on_connect(self,client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
            return True
        else:
            print("Failed to connect, return code %d\n", rc)
            return False

    def callback(self,client,userdata,msg):
        if(msg.topic == "Flipdot/shutdown"):
            self.shutdown()
        elif (msg.topic == "Flipdot/live"):
            self.live_mode(msg)
        elif (msg.topic == "Flipdot/add_ani"):
            self.add_animation(msg)
        elif (msg.topic == "Flipdot/add_image"):
            self.add_image(msg)
        elif (msg.topic == "Flipdot/remove"):
            self.remove_asset(msg)
        elif (msg.topic == "Flipdot/play"):
            self.play(msg)
        elif (msg.topic == "Flipdot/play_loop"):
            self.play_loop(msg)
        elif (msg.topic == "Flipdot/clock"):
            self.clock_mode()
        elif (msg.topic == "Flipdot/music"):
            self.music_mode()


    def subcribe(self,topic,cb):
        self.client.subscribe(topic)
        self.client.on_message = cb

    def shutdown(self):
        print(os.system("sh shutdown.sh"))

    def live_mode(self,msg):
        try:
            image = Image()
            image.from_string(msg.payload.decode())
            self.display.sendImage()
        except:
            pass
        self.mode = "idle"

    def add_animation(self,msg):
        #stores a new animation
        print(f"Received 3`{msg.payload.decode()}` from `{msg.topic}` topic")
        pass

    def add_image(self,msg):
        #stores a new image
        print(f"Received 4`{msg.payload.decode()}` from `{msg.topic}` topic")
        pass

    def remove_asset(self,msg):
        #removes an image from the filesystem
        print(f"Received 5`{msg.payload.decode()}` from `{msg.topic}` topic")
        pass

    def play(self,msg):
        #plays asset name
        #do a switch on the payload
        ##In case of animation
        print(f"Received 6 `{msg.payload.decode()}` from `{msg.topic}` topic")
        try:
            self.animation = Animation(msg.payload.decode())
            self.animation.init()
            self.mode = "play_animation"
        except:
            self.mode = "idle"
        print("set mode")

    def play_loop(self,msg):
        #plays asset name
        #do a switch on the payload
        ##In case of animation
        print(f"Received 6 `{msg.payload.decode()}` from `{msg.topic}` topic")
        try:
            self.animation = Animation(msg.payload.decode(),True)
            self.animation.init(True)
            self.mode = "play_animation"
        except:
            self.mode = "idle"
        print("set mode")

    def clock_mode(self):
        #displays the time
        print("clock mode")
        pass

    def music_mode(self):
        #displays artwork and progress bar
        print("music mode")
        pass

    def run_state_machine(self):
        while True:
            self.client.loop(0.1)
            if self.mode == "play_animation" :
               if not self.display.play_animation(self.animation):
                    self.mode = "idle"





if __name__ == '__main__':
    com = Net_Controller()
