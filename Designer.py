import datetime

from Image import *
import numpy as np
import PySimpleGUI as sg


class Designer:

    def __init__(self):
        self.file = None
        self.image = Image()
        self.window = sg.Window(title="Flipdot Panel Designer", layout=self.generate_layout())
        self.event_loop()


    def generate_layout(self):
        layout = [
            [
                sg.Text("Load image"),
                sg.In(size=(25, 1), enable_events=True, key="-FILE-"),
                sg.FileBrowse(),
                sg.Button('Load', button_color=('white', 'blue')),
            ],
            [
                self.build_button_map(),
                sg.Button('Save', button_color=('white', 'blue')),
                sg.Text("Please select a file to work with",key="-SAVE-"),
            ],
        ]
        return layout

    def load_image(self,path):
        self.image.load(path)
        self.refresh_image()


    def event_loop(self):
        while True:
            event, values = self.window.read()
            if event == "Exit" or event == sg.WIN_CLOSED:
                break
            elif event == "-FILE-":
                self.file = values["-FILE-"]
            elif event == "Load":
                if self.file is not None:
                    self.load_image(self.file)
                    self.window["-SAVE-"].update(str(datetime.datetime.now())+"      Loaded: "+self.file)
            elif event == "Save":
                self.image.save(self.file)
                self.window["-SAVE-"].update(str(datetime.datetime.now())+"      Saved: "+self.file)
            else:
                self.image.toggleDot(event[0],event[1])
                self.refresh_image()

    def refresh_image(self):
        field = self.image.getData()
        for i,col in enumerate(field):
            for j,element in enumerate(col):
                if(element > 0):
                    self.window[(i,j)].update('1', button_color=('gray','white'))
                else:
                    self.window[(i,j)].update('0', button_color=('gray','black'))

    def build_button_map(self):
        # writing this out would drastically improve the startup performace - currently not the case cause Im lazy
        return [[sg.Button(str('0'), size=(2, 1), pad=(0,0), border_width=0, key=(row,col),button_color=('gray', 'black')) for col in range(28)] for row in range(28)]


if __name__ == "__main__":
    designer = Designer()