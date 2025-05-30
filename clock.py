import datetime
import time

from Image import *
from NumerGenerator import *


class Clock:
    # The clock is designed to be passed to the display with the same interface as the animation
    def __init__(self, time_between_frames=1, design="digital", background_animation=None):
        self.design = design
        self.background = background_animation
        self.calender_alert = False
        self.smart_home_bg = None
        self.shift_weather_image = False
        self.bus_drove = False
        self.freeform_icon = None
        self.freeform_unit = None
        self.freeform_number = None
        self.time_between_frames = time_between_frames
        self.time_for_calender = datetime.timedelta(minutes=5)
        self.numgen_smarthome = NumberGenerator("numbers/numbers.json", 1)
        # Static setup here
        if (self.design == "digital modern"):
            self.numgen = NumberGenerator("numbers/numbers.json", 2)
        elif self.design == "digital":
            self.numgen = NumberGenerator("numbers/numbers.json", 2)
            self.static = Image("dot.txt")
        else:
            self.numgen = Animation("analog_clock/handle.json")
            self.static = self.numgen.get_entry(0)[0]

    def getframe(self):
        if self.background is not None:
            background = self.background.getframe()
            if background[1] == -1:
                self.background = None
                return self.generate_image() + background[0], self.time_between_frames
            return self.generate_image() + background[0], background[1]
        elif self.smart_home_bg is not None:
            return self.generate_image() + self.smart_home_bg, self.time_between_frames
        else:
            return self.generate_image(), self.time_between_frames

    def generate_image(self):
        time = datetime.datetime.now()
        h = time.hour
        m = time.minute
        s = time.second
        if (self.design == "digital modern"):
            return self.image_modern_digital(h, m, s)
        elif self.design == "digital":
            return self.image_digital(h, m)
        elif self.design == "analog":
            return self.image_analog(h, m)

    def image_modern_digital(self, h, m, s):
        hi = self.numgen.get_image(h)
        hi.shift_and_fill(3, 10)
        if (h < 10):
            hi.shift_and_fill(0, 5)
        mi = self.numgen.get_image(m)
        mi.shift_and_fill(11, 10)
        if (m < 10):
            mi.shift_and_fill(0, 5)
        si = self.numgen.get_image(s)
        si.shift_and_fill(19, 10)
        if (s < 10):
            si.shift_and_fill(0, 5)
        return si + hi + mi

    def image_digital(self, h, m):
        hi = self.numgen.get_image(h)
        hi.shift_and_fill(12, 3)
        if (h < 10):
            hi.shift_and_fill(0, 5)
        mi = self.numgen.get_image(m)
        mi.shift_and_fill(12, 17)
        if (m < 10):
            mi.shift_and_fill(0, 5)
            mi += self.numgen.get_image(0).shift_and_fill(12, 17)
        return hi + mi + self.static

    def image_analog(self, h, m):
        big = h % 12
        small = int(round(m / 5, 0))
        return self.numgen.get_entry(1 + small * 2)[0] + self.static + self.numgen.get_entry(2 + big * 2)[0]

    def update_smarthome(self, msg):
        smart_home = json.loads(msg.replace("'", '"'))
        self.smart_home_bg = Image()
        self.update_freeform()
        notify, notification = self.update_plants(smart_home["plants"])
        if notify: smart_home["notifications"].append(notification)
        self.update_notifications(smart_home["notifications"])
        self.update_washer(smart_home["washer"])
        self.update_temp(smart_home["forecast"], smart_home["outdoor"])
        self.update_traffic(smart_home["traffic"])
        self.update_timer(smart_home["timer"])
        self.update_calender(smart_home["calender"])
        self.update_fan(smart_home["fan"])
        self.update_luften(smart_home["luften"])

    def update_notifications(self, notification_list):
        if len(notification_list) == 0:
            self.shift_weather_image = False
        elif len(notification_list) > 4:
            self.shift_weather_image = False
            img = self.numgen_smarthome.get_image(len(notification_list))
            message = Image("icons/notification.txt")
            if (len(notification_list) > 9):
                img.shift_and_fill(6, 16)
            else:
                img.shift_and_fill(6, 19)
            message.shift_and_fill(6, 23)
            img += message
            self.smart_home_bg += img
        else:
            self.shift_weather_image = False
            display_start = 0
            for notification in notification_list:
                try:
                    img = Image("icons/" + notification + ".txt")
                except:
                    img = Image("icons/noicon.txt")
                img.shift_and_fill(6, display_start)
                self.smart_home_bg += img
                display_start += 7

    def update_washer(self, param):
        pass

    def update_temp(self, forecast, outdoor):
        try:
            im = self.numgen_smarthome.get_image(int(round(abs(forecast["temp"]))))
            im.shift_and_fill(0, 3)
            c = Image("icons/C.txt")
            if (int(round(forecast["temp"])) < 0):
                im.toggleDot(2, 0)
                im.toggleDot(2, 1)
                if int(round(forecast["temp"])) < -9:
                    c.shift_and_fill(23, 11)
                else:
                    c.shift_and_fill(23, 7)
            elif int(round(forecast["temp"])) < 10:
                im.shift_and_fill(0, -3)
                c.shift_and_fill(23, 4)
            else:
                c.shift_and_fill(23, 8)
                im.shift_and_fill(0, -3)
            im.shift_and_fill(23, 0)
            try:
                name = "icons/" + forecast["weather"] + ".txt"
                icon = Image(name)
            except:
                icon = Image()
            if self.shift_weather_image:
                icon.shift_and_fill(17, 0)
            im += icon
            im += c
            # Current temp
            cm = self.numgen_smarthome.get_image(int(round(abs(outdoor["temp"]))))
            cm.shift_and_fill(0, 3)
            if (int(round(outdoor["temp"])) < 0):
                cm.toggleDot(2, 0)
                cm.toggleDot(2, 1)
            cm.shift_and_fill(23, 15)
            if int(round(outdoor["temp"])) < -9:
                cm.shift_and_fill(0, -4)
            if (int(round(outdoor["temp"])) < 10):
                cm.shift_and_fill(0, 4)
            icon = Image("icons/C.txt")
            icon.shift_and_fill(23, 26)
            cm += icon
            self.smart_home_bg += im
            self.smart_home_bg += cm
        except:
            pass

    def update_traffic(self, param):
        try:
            clip = Image("icons/BUS3.txt")
            clip.shift_and_fill(17,0)
            if int(param["bus"]["departure 3"]) < 5 and not self.bus_drove:
                self.bus_drove = True
                self.background = Animation()
                self.background.animate_image(clip, loop=False)
            elif int(param["bus"]["departure 3"]) >= 5:
                im = self.numgen_smarthome.get_image(param["bus"]["departure 3"])
                im.shift_and_fill(17, 11)
                self.smart_home_bg += im
                self.smart_home_bg += clip
                self.bus_drove = False
        except:
            pass

    def update_timer(self, param):
        pass

    def update_calender(self, param):
        try:
            if datetime.datetime.strptime(param["start_time"],
                                          '%Y-%m-%d %H:%M:%S') - datetime.datetime.now() < self.time_for_calender \
                    and datetime.datetime.strptime(param["start_time"],
                                                   '%Y-%m-%d %H:%M:%S') - datetime.datetime.now() > datetime.timedelta(
                0):
                cicon = Image("icons/calender.txt")
                self.background = Textgen(param["name"], 0, 28, 1, background=cicon)
                self.calender_alert = True
            elif self.calender_alert:
                self.background = None
        except:
            pass

    def update_fan(self, param):
        pass

    def update_plants(self, problem):
        if problem["willhelm"] and problem["berndt"]:
            return True,"pump"
        elif problem["willhelm"]:
            return True,"can"
        elif problem["berndt"]:
            return True,"water_up"
        else:
            return False,""

    def update_luften(self, param):
        print(param)
        if param["wozi"] == "open":
            img = Image("icons/lueften.txt")
            self.smart_home_bg += img
        elif param["wozi"] == "close":
            img = Image("icons/ende_lueften.txt")
            self.smart_home_bg += img
        if param["esszi"] == "open":
            img = Image("icons/lueften.txt")
            img.shift_and_fill(0,3)
            self.smart_home_bg += img
        elif param["esszi"] == "close":
            img = Image("icons/ende_lueften.txt")
            img.shift_and_fill(0, 3)
            self.smart_home_bg += img

    def add_freeform_icon(self,icon_bytes):
        decodedArrays = json.loads(icon_bytes)
        self.freeform_icon = np.asarray(decodedArrays["icon"])
        self.update_freeform()
        #allows the display of 10x5 freeform icon

    def add_freeform_number(self,number):
        self.freeform_number = json.loads(number)["number"]
        self.update_freeform()

    def add_freeform_desc_unit(self,unit_bytes):
        # allows the display of 5x5 freeform unit
        decodedArrays = json.loads(unit_bytes)
        self.freeform_unit = np.asarray(decodedArrays["unit"])
        self.update_freeform()

    def clean_freeform(self):
        self.freeform_icon = None
        self.freeform_unit = None
        self.freeform_number = None
        self.update_freeform()

    def update_freeform(self):
        if self.smart_home_bg is None:
            self.smart_home_bg = Image()
        if self.freeform_icon is not None:
            complete_picture = np.zeros((28, 28), dtype=np.uint8)
            complete_picture[17:22, :10] = self.freeform_icon
            img = Image(data=complete_picture)
            self.smart_home_bg += img
        if self.freeform_number is not None:
            img = self.numgen_smarthome.get_image(self.freeform_number)
            img.shift_and_fill(17, 11)
            self.smart_home_bg += img
        if self.freeform_unit is not None:
            complete_picture = np.zeros((28, 28), dtype=np.uint8)
            complete_picture[17:22, 23:] = self.freeform_unit
            img = Image(data=complete_picture)
            self.smart_home_bg += img


if __name__ == "__main__":
    clock = Clock(design="digital")
    frame = "{\"notifications\":[\'shower\',\"tub\",\"flo\",\"kehrstin\"]," \
            "\"washer\":{\"status\":\"off\",\"remaining_time\":0},\"luften\":{\"wozi\":\"none\",\"esszi\":\"open\"},\"outdoor\":{\"temp\":21,\"hum\":65.0}," \
            "\"forecast\":{\"temp\":26,\"weather\":\"rainy\"},\"fan\":{\"Gustav\":\"unavailable\"," \
            "\"Venti\":\"unavailable\",\"Fritz\":\"unavailable\"},\"timer\":200,\"calender\":{\"name\":\"Linz :)\"," \
            "\"start_time\":\"2023-05-16 19:33:00\",\"end_time\":\"2023-05-15 00:00:00\"},\"traffic\":{\"bus\": " \
            "{\"departure 3\": \"unknown\" , \"departure 28\": \"unknown\"},\"car\": -1,\"bike\": -1},\"plants\":{\"berndt\":false,\"willhelm\":true}}"
    clock.add_freeform_number("{\"number\": 889}")
    clock.add_freeform_icon("{\"icon\": [[1, 0, 1, 0, 1,0, 1, 0, 1, 0],[1, 0, 1, 0, 1,0, 1, 0, 1, 0],[1, 0, 1, 0, 1,0, 1, 0, 1, 0],[1, 0, 1, 0, 1,0, 1, 0, 1, 0],[1, 0, 1, 0, 1,0, 1, 0, 1, 0]]}")
    clock.add_freeform_desc_unit("{\"unit\": [[1, 0, 1, 0, 1],[1, 0, 1, 0, 1],[1, 0, 1, 0, 1],[1, 0, 1, 0, 1],[1, 0, 1, 0, 1]]}")
    while True:
        #clock.update_smarthome(frame)
        clock.getframe()[0].show()
