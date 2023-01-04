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
            self.numgen = NumberGenerator("numbers/numbers.json",2)

    def getframe(self):
        return self.generate_image(),self.time_between_frames

    def generate_image(self):
        h = datetime.datetime.now().hour
        m = datetime.datetime.now().minute
        s = datetime.datetime.now().second
        hi = self.numgen.get_image(h)
        hi.shift_and_fill(3,10)
        if(h<10):
            hi.shift_and_fill(0,5)
        mi = self.numgen.get_image(m)
        mi.shift_and_fill(11,10)
        if(m<10):
            mi.shift_and_fill(0,5)
        si = self.numgen.get_image(s)
        si.shift_and_fill(19,10)
        if(s<10):
            si.shift_and_fill(0,5)
        return si+hi+mi

if __name__ == "__main__":
    clock = Clock()
    while True:
        clock.generate_image().show()
