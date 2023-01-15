import datetime
import time

from Image import *

class Music:

    def __init__(self):
        self.title = "Wating for Playback"
        self.duration = 0
        self.due = 0
        self.pose = 0
        self.playing = False
        self.txt = Textgen(self.title, 0, 20)

    def getframe(self):
        img = self.generate_image()
        return img,1

    def enter_infos(self,dict):
        data = json.loads(dict)
        self.playing = data["status"]
        if self.title != data["title"]:
            self.title = data["title"]
            self.txt = Textgen(self.title,0,20)
        self.duration = int(data["duration"])
        self.pose = int(data["pose"])
        self.due = self.duration+time.time() - self.pose

    def generate_image(self):
        if self.playing :
            img = Image("play.txt")
        else:
            img = Image("pause.txt")
        img += self.txt.get_image()
        img += self.create_progress_bar()
        return img

    def create_progress_bar(self):
        return Image()


if __name__ == "__main__":
    music = Music()
    while True:
        music.getframe()[0].show()


