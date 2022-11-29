import serial
from Image import *

class Display:
    header = bytearray([0x80, 0x83])
    endbyte = bytearray([0x8F])

    def __init__(self,debug=False):
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
    display = Display(True)
    image = Image()
    display.sendImage(image)

