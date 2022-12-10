import time
import os

from paho.mqtt import client as mqtt_client


class Net_Controller:

    def __init__(self,broker= 'homeassistant.local',port= 1883,client_id= f'Fliptot watchdog',user= "mqttuser" ,psw = "TODOPASSWD"):
        self.client = mqtt_client.Client(client_id)
        self.client.on_connect = self.on_connect
        self.client.username_pw_set(user,psw)
        self.client.connect(broker,port)

    def on_connect(self,client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)


    def subcribe(self,topic,cb):
        self.client.subscribe(topic)
        self.client.on_message = cb

    def shutdown(self,client,userdata,msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        print(os.system("sh /home/breiflor/Flipdot_demo/shutdown.sh"))

    def run_state_machine(self):
        self.client.loop_forever()


if __name__ == '__main__':
    com = Net_Controller()
    com.subcribe("Flipdot/shutdown",com.shutdown)
    com.run_state_machine()
