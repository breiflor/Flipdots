import copy
import datetime
import time
import mido
import cv2

from Image import *
from Animation import *
import numpy as np
import PySimpleGUI as sg
from mqtt_designer import *

class Live_mode:

    def __init__(self,mode="camera"):
        self.mode = mode
        self.pressed = 0
        self.layout = [[sg.Image(filename='', key='-IMAGE-'),[sg.Image(filename='', key='-RAW-')]],
                       [sg.Slider(range=(0,250), key='min', default_value=100, size=(20,15), orientation='horizontal')],
                        [sg.Slider(range=(0,250),  key='max',default_value=200, size=(20,15), orientation='horizontal')],
                        [sg.Slider(range=(1, 479),  key='size', default_value=400, size=(20, 15), orientation='horizontal')],
                        [sg.Button("Play", key='-PLAY-',  button_color=sg.theme_background_color(), border_width=0),sg.Button("Save", key='-SAVE-',  button_color=sg.theme_background_color(), border_width=0),sg.Button("Midi play", key='-MIDI-',  button_color=sg.theme_background_color(), border_width=0)]]
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
            if event == "-MIDI-":
                self.mode = "midi"
            if self.connect: self.connector.display_image(image)
            if self.mode == "camera":
                imgbytes=cv2.imencode('.png', frame)[1].tobytes()   # Convert the image to PNG Bytes
                self.window['-IMAGE-'].update(data=imgbytes)
                img = np.zeros((28, 28))
                img = (img + image.getData())*250
                img = cv2.resize(img,(500, 500), interpolation = cv2.INTER_AREA)
                imgbytes=cv2.imencode('.png',img)[1].tobytes()# Change the Image Element to show the new image
                self.window['-RAW-'].update(data=imgbytes)
            if self.mode == "midi":
                with mido.open_input() as inport:
                    for msg in inport:
                        try:
                            note = msg.note
                            vel = msg.velocity
                            print(note)
                            # determine if a note is currently pressed
                            if vel==0:
                                self.pressed = self.pressed - 1
                            else:
                                self.pressed = self.pressed + 1
                                self.send_note(note)
                            if self.pressed == 0:
                                print("lol")
                                self.send_note(0)
                        except:
                            print(msg)


    def __del__(self):
        self.window.close()

    def send_note(self, note,offset=6):
        dots = int((note*offset)%(28*28))
        img = Image()
        arr = np.zeros((28*28,1),dtype=int)
        for x in range(dots):
            arr[x] = 1
        arr = arr.reshape((28,28))
        if dots != 0 : img.setData(arr)
        self.connector.display_image(img)


if __name__ == "__main__":
    live = Live_mode()
    live.loop()