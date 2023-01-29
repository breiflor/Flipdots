import copy
import datetime
import cv2
from Image import *
from Animation import *
import numpy as np
import PySimpleGUI as sg

class Converter:

    def __init__(self):
        self.window = sg.Window(title="Flipdot Creator", layout=self.generate_layout(), resizable=True)
        self.file = None
        self.image = Image()
        self.animation = Animation()
        self.event_loop()


    def event_loop(self):
        while True:
            event, values = self.window.read()
            if event == "Exit" or event == sg.WIN_CLOSED:
                break
            elif event == "-FILE-":
                self.file = values["-FILE-"]
            elif event == "Convert":
                if self.file is not None:
                    suf = pathlib.Path(self.file).suffix
                    if(suf == ".mp4" or suf ==".avi"):
                        self.load_amimation(self.file,values)
                    else:
                        self.load_image(self.file,values)
            elif event == "Save-Img":
                self.image.save(values["-SAVE-"])
            elif event == "Save-Animation":
                self.animation.store(values["-SAVE-"])


    def generate_layout(self):
        layout = [[sg.Text("Load file"),
                sg.In(size=(25, 1), enable_events=True, key="-FILE-"),
                sg.FileBrowse(),
                sg.Button('Convert', button_color=('white', 'blue'))],
                  [sg.Image(filename='', key='-IMAGE-')],
                  [sg.Slider(range=(1, 60), key='fps', default_value=60, size=(20, 15), orientation='horizontal'),
                   sg.Text("fps")],
                       [sg.Slider(range=(0,250), key='min', default_value=100, size=(20,15), orientation='horizontal'),sg.Text("min")],
                        [sg.Slider(range=(0,250),  key='max',default_value=200, size=(20,15), orientation='horizontal'),sg.Text("max")],
                        [sg.Slider(range=(1, 479),  key='size', default_value=400, size=(20, 15), orientation='horizontal'),sg.Text("size")],
                  [sg.In(size=(25, 1), enable_events=True, key="-SAVE-"),sg.Button('Save-Img', button_color=('white', 'blue')),sg.Button('Save-Animation', button_color=('white', 'blue'))]]
        return layout

    def load_image(self, file,values):
        cap = cv2.VideoCapture(file)
        frame = cap.read()[1]
        self.image.from_frame(frame,values['min'],values['max'],values['size'])
        img = np.zeros((28, 28))
        img = (img + self.image.getData()) * 250
        img = cv2.resize(img, (500, 500), interpolation=cv2.INTER_AREA)
        imgbytes = cv2.imencode('.png', img)[1].tobytes()  # Change the Image Element to show the new image
        self.window['-IMAGE-'].update(data=imgbytes)

    def load_amimation(self, file,values):
        cap = cv2.VideoCapture(file)
        cnter = values["fps"]
        while True:
            sucess,frame = cap.read()
            if not sucess:
                break
            if cnter == values["fps"]:
                img = Image()
                img.from_frame(frame,values['min'],values['max'],values['size'])
                self.animation.insert(img,60/values["fps"])
                cnter = 0
            else:
                cnter = cnter+1


if __name__ == "__main__":
    converter = Converter()