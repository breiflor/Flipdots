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
        self.layout = [[sg.Image(filename='', key='-IMAGE-'),[sg.Image(filename='', key='-RAW-')]],
                       [sg.Slider(range=(0,250), key='min', default_value=100, size=(40,15), orientation='horizontal')],
                        [sg.Slider(range=(0,250),  key='max',default_value=200, size=(40,15), orientation='horizontal')],
                        [sg.Slider(range=(1, 479),  key='size', default_value=400, size=(40, 15), orientation='horizontal')],
                        [sg.Button("Play", key='-PLAY-',  button_color=sg.theme_background_color(), border_width=0),sg.Button("Save", key='-SAVE-',  button_color=sg.theme_background_color(), border_width=0)]]
        self.window = sg.Window('Demo Application - OpenCV Integration', self.layout, location=(800,400),
                           no_titlebar=False, grab_anywhere=True)  # if trying Qt, you will need to remove this right click menu
        self.cap = cv2.VideoCapture(0)
        self.connector = mqtt_designer()
        self.connect = False
        self.img_nr = 0

    def loop(self):
        while True:
            event, values = self.window.read(timeout=20)
            if event in ('Exit', None):
                break
            if event == "-PLAY-":
                self.connect = not self.connect
            ret, frame = self.cap.read()
            image = Image()
            image.from_frame(frame,values['min'],values['max'],values['size'])# Read image from capture device (camera)
            if event == "-SAVE-":
                image.save(str(self.img_nr)+".txt")
                self.img_nr+=1
            if self.connect: self.connector.display_image(image)
            imgbytes=cv2.imencode('.png', frame)[1].tobytes()   # Convert the image to PNG Bytes
            self.window['-IMAGE-'].update(data=imgbytes)
            img = np.zeros((28, 28))
            img = (img + image.getData())*250
            img = cv2.resize(img,(500, 500), interpolation = cv2.INTER_AREA)
            imgbytes=cv2.imencode('.png',img)[1].tobytes()# Change the Image Element to show the new image
            self.window['-RAW-'].update(data=imgbytes)

    def __del__(self):
        self.window.close()

if __name__ == "__main__":
    live = Live_mode()
    live.loop()