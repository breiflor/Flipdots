import datetime
import time

from Image import *
from NumerGenerator import *

class Clock:
    #The clock is designed to be passed to the display with the same interface as the animation
    def __init__(self, time_between_frames= 1, design ="digital", background_animation=None):
        self.design = design
        self.background = background_animation
        self.smart_home_bg = None
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
        if self.smart_home_bg is not None:
            return self.generate_image()+self.smart_home_bg,self.time_between_frames
        elif self.background is None:
            return self.generate_image(), self.time_between_frames
        else:
            background = self.background.getframe() #assuming that the Animation was initilized with loop enabled
            return self.generate_image()+background[0],background[1]

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

    def update_smarthome(self,msg):
        smart_home = json.loads(msg)
        self.smart_home_bg = Image()
        self.update_windows(smart_home["windows"])
        self.update_washer(smart_home["washer"])
        self.update_temp(smart_home["forecast"],smart_home["outdoor"])
        self.update_traffic(smart_home["traffic"])
        self.update_timer(smart_home["timer"])
        self.update_calender(smart_home["calender"])
        self.update_fan(smart_home["fan"])

    def update_windows(self, param):
        if(param["bad_oben"]):
            img = Image("icons/shower.txt")
            img.shift_and_fill(0,0)
            self.smart_home_bg+=img
        if (param["bad_unten"]):
            img = Image("icons/tub.txt")
            img.shift_and_fill(0, 7)
            self.smart_home_bg += img
        if (param["flo_bureo"]):
            img = Image("icons/flo.txt")
            img.shift_and_fill(0, 14)
            self.smart_home_bg += img
        if (param["hannah_bureo"]):
            img = Image("icons/hannah.txt")
            img.shift_and_fill(0, 21)
            self.smart_home_bg += img

    def update_washer(self, param):
        pass

    def update_temp(self, forecast, outdoor):
        if(forecast["temp"]<0):
            im = self.numgen.get_image(int(abs(forecast["temp"])))
            im.shift_and_fill(0,3)
            im.toggleDot(2,0)
            im.toggleDot(2,1)
        else:
            im = self.numgen.get_image(int(abs(forecast["temp"])))
            im.shift_and_fill(0, 3)
        im.shift_and_fill(23,0)
        try:
            name = "icons/"+forecast["weather"]+".txt"
            icon = Image(name)
        except:
            icon = Image()
        icon.shift_and_fill(18,0)
        im+=icon
        #Current temp
        if (outdoor["temp"] < 0):
            cm = self.numgen.get_image(int(abs(outdoor["temp"])))
            cm.shift_and_fill(0, 3)
            cm.toggleDot(2, 0)
            cm.toggleDot(2, 1)
        else:
            cm = self.numgen.get_image(int(abs(outdoor["temp"])))
            cm.shift_and_fill(0, 3)
        cm.shift_and_fill(23, 11)
        icon = Image("icons/C.txt")
        icon.shift_and_fill(24,23)
        cm+=icon
        self.smart_home_bg += im
        self.smart_home_bg += cm
        pass

    def update_traffic(self, param):
        pass

    def update_timer(self, param):
        pass

    def update_calender(self, param):
        pass

    def update_fan(self, param):
        pass


if __name__ == "__main__":
    clock = Clock(design="digital")
    frame = "{\"windows\":{\"bad_oben\":false,\"bad_unten\":false,\"flo_bureo\":false,\"hannah_bureo\":false}," \
            "\"washer\":{\"status\":\"off\",\"remaining_time\":0},\"outdoor\":{\"temp\":15.2,\"hum\":65.0}," \
            "\"forecast\":{\"temp\":16.5,\"weather\":\"cloudy\"},\"fan\":{\"Gustav\":\"unavailable\"," \
            "\"Venti\":\"unavailable\",\"Fritz\":\"unavailable\"},\"timer\":200,\"calender\":{\"name\":\"Linz :)\"," \
            "\"start_time\":\"2023-05-12 00:00:00\",\"end_time\":\"2023-05-15 00:00:00\"},\"traffic\":{\"bus\": " \
            "{\"departure 3\": \"21\" , \"departure 28\": \"unknown\"},\"car\": -1,\"bike\": -1}}"
    #while True:
    clock.update_smarthome(frame)
    clock.getframe()[0].show()
