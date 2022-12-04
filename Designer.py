import datetime

from Image import *
from Animation import *
import numpy as np
import PySimpleGUI as sg


class Designer:

    def __init__(self):
        self.file = None
        self.image = Image()
        self.window = sg.Window(title="Flipdot Panel Designer", layout=self.generate_layout())
        self.animation = None
        self.time = -1
        self.current_frame_id = 0
        self.playing = False
        self.event_loop()



    def generate_layout(self):
        layout = [
            [
                sg.Text("Load image"),
                sg.In(size=(25, 1), enable_events=True, key="-FILE-"),
                sg.FileBrowse(),
                sg.Button('Load', button_color=('white', 'blue')),
                sg.Button(sg.SYMBOL_LEFT_ARROWHEAD, key='-PREV-',  button_color=sg.theme_background_color(), border_width=0),
                sg.Button(sg.SYMBOL_RIGHT, key='-PLAY-',  button_color=sg.theme_background_color(), border_width=0),
                sg.Button(sg.SYMBOL_RIGHT_ARROWHEAD, key='-NEXT-',  button_color=sg.theme_background_color(), border_width=0),
                sg.Button("+", key='-ADD-',  button_color=sg.theme_background_color(), border_width=0),
                sg.Button("-", key='-DEL-',  button_color=sg.theme_background_color(), border_width=0),
                sg.Input('TIME',size=(5, 1),enable_events=True, key="-TIME-"),
                sg.Text("s"),
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
            elif event == "-TIME-":
                if(values["-TIME-"]!=""):
                    self.time = int(values["-TIME-"])
                    self.update_time()
            elif event == "Load":
                if self.file is not None:
                    suf = pathlib.Path(self.file).suffix
                    if(suf == ".json"):
                        self.load_amimation(self.file)
                    else:
                        self.load_image(self.file)
                    self.window["-SAVE-"].update(str(datetime.datetime.now())+"      Loaded: "+self.file)
            elif event == "Save":
                suf = pathlib.Path(self.file).suffix
                if(suf == ".json"):
                    self.animation.set_entry((self.image,self.time),self.current_frame_id)
                    self.animation.store(self.file)
                else:
                    self.image.save(self.file)
                self.window["-SAVE-"].update(str(datetime.datetime.now())+"      Saved: "+self.file)
            elif event == "-PREV-":
                self.prev_image()
            elif event == "-ADD-":
                image = Image()
                print(image.data)
                self.animation.insert_entry((image,1),self.current_frame_id+1)
                self.next_image()
            elif event == "-DEL-":
                self.animation.delete_entry(self.current_frame_id)
                if (self.current_frame_id < (len(self.animation.image_list) - 1)):
                    self.image, self.time = self.animation.get_entry(self.current_frame_id)
                else:
                    self.current_frame_id = self.current_frame_id - 1
                    self.image, self.time = self.animation.get_entry(self.current_frame_id)
                self.refresh_image()
            elif event == "-PLAY-":
                if(self.playing is False):
                    self.playing = True
                    self.window["-PLAY-"].update(sg.SYMBOL_SQUARE)
                    self.play()
                else:
                    self.playing = False
                    self.window["-PLAY-"].update(sg.SYMBOL_RIGHT)
            elif event == "-NEXT-":
                self.next_image()
            else:
                self.image.toggleDot(event[0],event[1])
                self.refresh_image()

    def prev_image(self):
        self.animation.set_entry((self.image, self.time), self.current_frame_id)
        if (self.current_frame_id == 0):
            self.current_frame_id = (len(self.animation.image_list) - 1)
        else:
            self.current_frame_id = self.current_frame_id - 1
        self.image, self.time = self.animation.get_entry(self.current_frame_id)
        self.refresh_image()

    def next_image(self):
        self.animation.set_entry((self.image, self.time), self.current_frame_id)
        if (self.current_frame_id < (len(self.animation.image_list) - 1)):
            self.current_frame_id = self.current_frame_id + 1
        else:
            self.current_frame_id = 0
        self.image, self.time = self.animation.get_entry(self.current_frame_id)
        self.refresh_image()

    def refresh_image(self):
        field = self.image.getData()
        self.update_time()
        for i,col in enumerate(field):
            for j,element in enumerate(col):
                if(element > 0):
                    self.window[(i,j)].update('1', button_color=('gray','white'))
                else:
                    self.window[(i,j)].update('0', button_color=('gray','black'))

    def build_button_map(self):
        # writing this out would drastically improve the startup performace - currently not the case cause Im lazy
        return [[sg.Button(str('0'), size=(2, 1), pad=(0,0), border_width=0, key=(row,col),button_color=('gray', 'black')) for col in range(28)] for row in range(28)]

    def load_amimation(self, file):
        self.current_frame_id = 0
        self.animation = Animation(file)
        self.image,self.time = self.animation.get_entry()
        self.refresh_image()

    def update_time(self):
        self.window["-TIME-"].update(str(self.time))

    def play(self):
        self.animation.init()
        while self.playing:
            image,delay = self.animation.getframe()
            if(delay > 0):
                image.show(time=delay*1000)
            else:
                image.show(time=2000)
                break
        self.playing = False
        self.window["-PLAY-"].update(sg.SYMBOL_RIGHT)



if __name__ == "__main__":
    designer = Designer()