import datetime
import time

from Image import *
from Animation import *

class Music:

    def __init__(self):
        self.title = "Wating for Playback"
        self.duration = 1
        self.due = 0
        self.pose = 0
        self.playing = False
        self.txt = Textgen(self.title, 0, 20)
        self.progessbar = Animation("progressbar")

    def getframe(self):
        img = self.generate_image()
        return img,0.3 #refresh rate

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
        progress = 1-(self.due - time.time())/self.duration
        segments = round(26*progress,0)
        if progress > 1 : 
            segments = 26
        img = self.progessbar.get_entry(int(segments))[0]
        return img


if __name__ == "__main__":
    music = Music()
    music.enter_infos("{\"status\":\"True\",\"title\":\"test\",\"duration\":60,\"pose\":5}")
    # Homeassistant template {"status":"{{is_state("media_player.spotify_mrbreitkopf", "playing")}}","title":"{{state_attr("media_player.spotify_mrbreitkopf","media_title")}}","duration":{{state_attr("media_player.spotify_mrbreitkopf","media_duration")}},"pose":{{state_attr("media_player.spotify_mrbreitkopf","media_position")}}}
    while True:
        music.getframe()[0].show()


