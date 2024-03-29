import copy
import datetime
import time

from Image import *
from Animation import *
import numpy as np
import PySimpleGUI as sg
from mqtt_designer import *

class Designer:

    def __init__(self):
        self.connector = None
        self.file = None
        self.live_mode = False
        self.image = Image()
        tabgroup = [[sg.TabGroup([[sg.Tab("Desginer",self.generate_layout()),sg.Tab("File Handling",self.generate_file_handling_layout())]])]]
        self.window = sg.Window("Flipdot Panel Designer", tabgroup, resizable=True)
        self.animation = None
        self.time = -1
        self.current_frame_id = 0
        self.playing = False
        self.event_loop()
        self.selected = None



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
                sg.Button("C", key='-COPY-',  button_color=sg.theme_background_color(), border_width=0),
                sg.Button("-", key='-DEL-',  button_color=sg.theme_background_color(), border_width=0),
                sg.Input('TIME',size=(5, 1),enable_events=True, key="-TIME-"),
                sg.Text("s"),
            ],
            [sg.Frame("Image",self.build_button_map(),expand_x=True,expand_y=True),],
            [

                sg.Button('Save', button_color=('white', 'blue')),
                sg.Text("Please select a file to work with",key="-SAVE-"),
                sg.Button('Connect', button_color=('white', 'red'))
            ],
        ]
        return layout

    def generate_file_handling_layout(self):
        self.connector = mqtt_designer() #TODO check if this init causes issues
        time.sleep(1)
        print(self.connector.get_animations())
        layout = [[sg.Text("Load image"),
                   sg.In(size=(25, 1), enable_events=True, key="-FILE-"),
                   sg.FileBrowse(),],
                  [sg.Listbox(values=self.connector.get_animations(),key="animations",enable_events=True,expand_x=True,expand_y=True)],
                  [sg.Listbox(values=self.connector.get_images(),key="images",enable_events=True,expand_x=True,expand_y=True)],
                  [sg.Button('del', button_color=('white', 'blue')),
                  sg.Button('download', button_color=('white', 'blue')),
                   sg.Button('upload', button_color=('white', 'blue')),],
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
            elif event == "-FILE-0":
                self.file = values["-FILE-0"]
            elif event == "-TIME-":
                if(values["-TIME-"]!=""):
                    self.time = float(values["-TIME-"])
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
                if self.animation is None :
                    self.animation = Animation()
                    self.animation.insert_entry((Image(),1),self.current_frame_id)
                else:
                    self.animation.insert_entry((Image(),1),self.current_frame_id+1)
                self.next_image()
            elif event == "-COPY-":
                self.animation.insert_entry((Image(),1),self.current_frame_id)
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
            elif event == "Connect":
                if not self.live_mode:
                    self.window["-SAVE-"].update("Connected to Panel")
                    self.start_live_mode()
                else:
                    self.window["-SAVE-"].update("Disconnected")
                    self.live_mode = False
            elif event == "upload":
                if self.file is not None:
                    suf = pathlib.Path(self.file).suffix
                    if(suf == ".json"):
                        self.load_amimation(self.file)
                        self.connector.send_animation(self.file,self.animation)
                    else:
                        self.load_image(self.file)
                        self.connector.send_image(self.file,self.image)
                    self.refresh_asset_list()
            elif event == "download":
                if self.selected == "images":
                    self.image = self.connector.get_image(values["images"][0])
                    self.refresh_image()
                elif self.selected == "animation":
                    self.animation = self.connector.get_animation(values["animations"][0])
                    self.refresh_image()
            elif event == "del":
                if self.selected == "images":
                    self.image = self.connector.remove_asset(values["images"][0])
                    self.refresh_asset_list()
                elif self.selected == "animation":
                    self.animation = self.connector.remove_asset(values["animations"][0])
                    self.refresh_asset_list()
            elif event == "animations":
                self.selected = "animation"
            elif event == "images":
                self.selected = "images"
            else:
                try:
                    self.image.toggleDot(event[0],event[1])
                    self.refresh_image()
                except:
                    print("not handled event "+str(event)+str(values))

    def refresh_asset_list(self):
        self.connector.refresh_installed_assets()
        time.sleep(1)
        self.window["animations"].update(values=self.connector.get_animations())
        self.window["images"].update(values=self.connector.get_images())

    def prev_image(self):
        self.animation.set_entry((copy.deepcopy(self.image), self.time), self.current_frame_id)
        if (self.current_frame_id == 0):
            self.current_frame_id = (len(self.animation.image_list) - 1)
        else:
            self.current_frame_id = self.current_frame_id - 1
        self.image, self.time = self.animation.get_entry(self.current_frame_id)
        self.refresh_image()

    def next_image(self):
        self.animation.set_entry((copy.deepcopy(self.image), self.time), self.current_frame_id)
        if (self.current_frame_id < (len(self.animation.image_list) - 1)):
            self.current_frame_id = self.current_frame_id + 1
        else:
            self.current_frame_id = 0
        self.image, self.time = self.animation.get_entry(self.current_frame_id)
        self.refresh_image()

    def refresh_image(self):
        field = self.image.getData()
        self.update_time()
        if self.live_mode :
            self.connector.display_image(self.image)
        for i,col in enumerate(field):
            for j,element in enumerate(col):
                if(element > 0):
                    self.window[(i,j)].update('1', button_color=('gray','white'))
                else:
                    self.window[(i,j)].update('0', button_color=('gray','black'))

    def build_button_map(self):
        # writing this out would drastically improve the startup performace - currently not the case cause Im lazy
        return [[sg.Button(str('0'), size=(2, 1), pad=(0,0), border_width=0, key=(row,col),button_color=('gray', 'black'), expand_x=True, expand_y=True) for col in range(28)] for row in range(28)]

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
                if self.live_mode:
                    self.connector.display_image(image)
                else:
                    image.show(time=delay*1000)
            else:
                if self.live_mode:
                    self.connector.display_image(image)
                else:
                    image.show(time=2000)
                break
        self.playing = False
        self.window["-PLAY-"].update(sg.SYMBOL_RIGHT)

    def start_live_mode(self):
        self.live_mode = True
        try:
            self.connector = mqtt_designer()
            self.window["Connect"].update("Disconnect")
        except:
            self.live_mode = False
            self.window["-SAVE-"].update("Error no Connection Possible")





if __name__ == "__main__":
    designer = Designer()