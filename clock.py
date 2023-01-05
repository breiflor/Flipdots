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
        #Static setup here
        if(self.design == "digital modern"):
            self.numgen = NumberGenerator("numbers/numbers.json",2)
        elif self.design == "digital":
            self.numgen = NumberGenerator("numbers/numbers.json",2)
            self.static = Image("dot.txt")
        elif self.design == "analog":
            self.numgen = Animation("analog_clock/handle.json")
            self.static = self.numgen.get_entry(0)[0]

    def getframe(self):
        return self.generate_image(),self.time_between_frames

    def generate_image(self):
        time = datetime.datetime.now()
        h = time.hour
        m = time.minute
        s = time.second
        if(self.design == "digital modern"):
            return self.image_modern_digital(h,m,s)
        elif self.design == "digital":
            return self.image_digital(h,m)
        elif self.design == "analog":
            return self.image_analog(h,m)

    def image_modern_digital(self,h,m,s):
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

    def image_digital(self, h, m):
        hi = self.numgen.get_image(h)
        hi.shift_and_fill(11,3)
        if(h<10):
            hi.shift_and_fill(0,5)
        mi = self.numgen.get_image(m)
        mi.shift_and_fill(11,17)
        if(m<10):
            mi.shift_and_fill(0,5)
            mi += self.numgen.get_image(0).shift_and_fill(11,17)
        return hi + mi + self.static


    def image_analog(self,h,m):
        big = h%12
        small = int(round(m/5,0))
        return self.numgen.get_entry(1+small*2)[0] + self.static + self.numgen.get_entry(2+big*2)[0]

if __name__ == "__main__":
    clock = Clock(design="analog")
    #while True:
    #    clock.generate_image().show()
    clock.image_analog(12,10).show()
    clock.image_analog(12,20).show()
    clock.image_analog(2,20).show()
    clock.image_analog(2,7).show()
    clock.image_analog(2,1).show()
    clock.image_analog(1,1).show()
    clock.image_analog(22,7).show()
    clock.image_analog(22,30).show()