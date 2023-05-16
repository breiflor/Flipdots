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
        self.numgen_smarthome = NumberGenerator("numbers/numbers.json", 1)
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
        self.update_plants(smart_home["plants"])

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
        im = self.numgen_smarthome.get_image(int(round(abs(forecast["temp"]))))
        im.shift_and_fill(0,3)
        c = Image("icons/C.txt")
        if (forecast["temp"] < 0):
            im.toggleDot(2,0)
            im.toggleDot(2,1)
            if forecast["temp"] < -9:
                c.shift_and_fill(23,11)
            else:
                c.shift_and_fill(23,7)
        elif forecast["temp"] <10:
            im.shift_and_fill(0,-3)
            c.shift_and_fill(23, 4)
        else:
            c.shift_and_fill(23, 8)
            im.shift_and_fill(0, -3)
        im.shift_and_fill(23,0)
        try:
            name = "icons/"+forecast["weather"]+".txt"
            icon = Image(name)
        except:
            icon = Image()
        icon.shift_and_fill(17,0)
        im+=icon
        im+=c
        #Current temp
        cm = self.numgen_smarthome.get_image(int(round(abs(outdoor["temp"]))))
        cm.shift_and_fill(0, 3)
        if (outdoor["temp"] < 0):
            cm.toggleDot(2, 0)
            cm.toggleDot(2, 1)
        cm.shift_and_fill(23, 15)
        if (abs(outdoor["temp"]) < 10):
            cm.shift_and_fill(0,4)
        icon = Image("icons/C.txt")
        icon.shift_and_fill(23,26)
        cm+=icon
        self.smart_home_bg += im
        self.smart_home_bg += cm
        pass

    def update_traffic(self, param):
        print(param)
        try:
            im = self.numgen_smarthome.get_image(param["bus"]["departure 3"])
            im.shift_and_fill(5,11)
            clip = Image("icons/BUS3.txt")
            clip.shift_and_fill(5)
            self.smart_home_bg += im
            self.smart_home_bg += clip
        except:
            pass

    def update_timer(self, param):
        pass

    def update_calender(self, param):
        pass

    def update_fan(self, param):
        pass

    def update_plants(self, problem):
        if problem:
            im = Image("icons/can.txt")
            im.shift_and_fill(5,20)
            self.smart_home_bg+= im


if __name__ == "__main__":
    clock = Clock(design="digital")
    frame = "{\"windows\":{\"bad_oben\":true,\"bad_unten\":false,\"flo_bureo\":false,\"hannah_bureo\":true}," \
            "\"washer\":{\"status\":\"off\",\"remaining_time\":0},\"outdoor\":{\"temp\":7.9,\"hum\":65.0}," \
            "\"forecast\":{\"temp\":16,\"weather\":\"rainy\"},\"fan\":{\"Gustav\":\"unavailable\"," \
            "\"Venti\":\"unavailable\",\"Fritz\":\"unavailable\"},\"timer\":200,\"calender\":{\"name\":\"Linz :)\"," \
            "\"start_time\":\"2023-05-12 00:00:00\",\"end_time\":\"2023-05-15 00:00:00\"},\"traffic\":{\"bus\": " \
            "{\"departure 3\": \"21\" , \"departure 28\": \"unknown\"},\"car\": -1,\"bike\": -1},\"plants\":true}"
    #while True:
    clock.update_smarthome(frame)
    clock.getframe()[0].show()
