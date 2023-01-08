import copy
import datetime
import time

import cv2

from Image import *
from Animation import *
import numpy as np
import PySimpleGUI as sg
from mqtt_designer import *

class Live_mode:

    def __init__(self):
        self.layout = [[sg.Image(filename='', key='-IMAGE-', tooltip='Right click for exit menu')],]
        self.window = sg.Window('Demo Application - OpenCV Integration', self.layout, location=(800,400),
                           no_titlebar=False, grab_anywhere=True)  # if trying Qt, you will need to remove this right click menu
        self.cap = cv2.VideoCapture(0)
        self.connector = mqtt_designer()

    def loop(self):
        while True:
            event, values = self.window.read(timeout=20)
            if event in ('Exit', None):
                break
            ret, frame = self.cap.read()
            image = Image()
            image.from_frame(frame)# Read image from capture device (camera)
            self.connector.display_image(image)
            imgbytes=cv2.imencode('.png', frame)[1].tobytes()   # Convert the image to PNG Bytes
            self.window['-IMAGE-'].update(data=imgbytes)   # Change the Image Element to show the new image


    def __del__(self):
        self.window.close()

if __name__ == "__main__":
    live = Live_mode()
    live.loop()