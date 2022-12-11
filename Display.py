import time

import serial

import Animation
from Image import *
from Animation import *

class Display:
    header = bytearray([0x80, 0x83])
    endbyte = bytearray([0x8F])

    def __init__(self,debug=False):
        self.next_frame = time.time() #Stores Timestamp
        self.debug = debug
        if(not self.debug):
            self.ser = serial.Serial('/dev/ttyAMA0',19200)

    def build_message(self,data,adress=0xFF):
        adr = bytearray([adress])
        return self.header+adr+data+self.endbyte

    def send_message(self,data,addr=0xFF):
        if(not self.debug):
            self.ser.write(self.build_message(data,addr))
        else:
            print("DEBUG: Sent"+str(self.build_message(data,addr)))

    def _play_animation(self,animation):
        animation.init()
        while True:
            image,delay = animation.getframe()
            self.sendImage(image)
            if(delay > 0):
                time.sleep(delay)
            else:
                break

    def play_animation(self,animation):
        print(time.time())
        print(self.next_frame)
        if( time.time() > self.next_frame):
            image,delay = animation.getframe()
            self.sendImage(image)
            self.next_frame = time.time()+delay
            if(delay > 0):
                return True
            else:
                self.next_frame = time.time()
                return False
        else:
            return True

    def black(self):
        self.send_message(bytearray([ 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]))

    def white(self):
        self.send_message(bytearray([ 0x7F, 0x7F, 0x7F, 0x7F, 0x7F, 0x7F, 0x7F, 0x7F, 0x7F, 0x7F, 0x7F, 0x7F, 0x7F, 0x7F, 0x7F, 0x7F, 0x7F, 0x7F, 0x7F, 0x7F, 0x7F, 0x7F, 0x7F, 0x7F, 0x7F, 0x7F, 0x7F, 0x7F]))

    def sendImage(self,image):
        self.send_message(image.getPanel(0),0x00)
        self.send_message(image.getPanel(1),0x01)
        self.send_message(image.getPanel(2),0x02)
        self.send_message(image.getPanel(3),0x03)

if __name__ == "__main__":
    display = Display(False)
    image = Image()
    display.sendImage(image)
    animation = Animation("default_animation/")
    display._play_animation(animation)

