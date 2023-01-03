import datetime
import time

from Image import *
from NumerGenerator import *

class Clock:
    #The clock is designed to be passed to the display with the same interface as the animation
    def __init__(self, time_between_frames= 1, design ="digital", background_animation=None):
        self.design = design
        self.background = background_animation
        self.time_between_frames = time_between_frames
        if(design == "digital"):
            self.numgen = NumberGenerator("numbers/numbers.json")

    def getframe(self):
        return self.generate_image(),self.time_between_frames

    def generate_image(self):
        h = datetime.datetime.now().hour
        m = datetime.datetime.now().minute
        s = datetime.datetime.now().second
        h = self.numgen.get_image(h)
        h.show()
        h.shift_and_fill(3,10)
        h.show()
        m = self.numgen.get_image(m)
        m.show()
        m.shift_and_fill(11,10)
        m.show()
        s = self.numgen.get_image(s)
        s.show()
        s.shift_and_fill(20,10)
        s.show()
        return s+h+m

if __name__ == "__main__":
    clock = Clock()
    while True:
        clock.generate_image().show()
