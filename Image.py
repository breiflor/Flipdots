import numpy as np
import cv2
import pathlib
import json


class NumpyArrayEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

class Image:

    def __init__(self,imagepath=None,data=np.zeros((28,28),dtype=int)):
        self.data = np.copy(data)  # creates eigen matrix as default image
        if (imagepath is not None):
            self.load(imagepath) # checks if text or picture representation and inits class

    def __add__(self, other):
        return Image(data=np.around((self.data+other.getData()+0.2)/2).astype(int))

    def __sub__(self, other):
        return Image(data=np.around((self.data-other.getData()).astype(int)))

    def __iadd__(self, other):
        self.data=np.around((self.data+other.getData()+0.2)/2).astype(int)
        return self

    def __invert__(self):
        self.data = ((-1)*(self.data-1).astype(int))
        return self

    def setData(self,data):
        self.data = data

    def insert_text(self,text,location=(0,9),scale= 0.8):
        cv2.putText(self.data, text=text, org=location,
                    fontFace= cv2.FONT_HERSHEY_PLAIN, fontScale=scale, color=(1,1,1),
                    thickness=1)
        return self

    def toggleDot(self,x,y):
        if self.data[x][y] > 0:
            self.data[x][y] = 0
        else:
            self.data[x][y] = 1

    def shift_and_fill(self,x=0,y=0,fill=0):
        res = np.empty_like(self.data)
        if x > 0:
            res[:x] = fill
            res[x:] = self.data[:-x]
        elif x < 0:
            res[x:] = fill
            res[:x] = self.data[-x:]
        else:
            res = self.data
        self.data = res #maybe copy here
        for index,r in enumerate(res):
            row = np.empty_like(r)
            if y > 0:
                row[:y] = fill
                row[y:] = r[:-y]
            elif y < 0:
                row[y:] = fill
                row[:y] = r[-y:]
            else:
                row = r
            self.data[index] = row
        #this method shifts an image and fills the remaining spots with the specifed value
        self.data = res #maybe a copy is needed here
        return self

    def getData(self):
        return np.copy(self.data)

    def getPanel(self,id):
        panel = self.data[:,(0+id*7):(7+id*7)]
        panel_hex = bytearray()
        for row in reversed(panel) :
            panel_hex.append(self.calculate_row(row))
        return panel_hex

    def calculate_row(self,row):
        val = np.matmul((row.reshape(1,7)),(np.array([1,2,4,8,16,32,64]).reshape(7,1)))
        return val[0][0].item()

    def show(self,original=False,scale_to_px=500,time = 0):
        img  = np.zeros((28,28))
        img = img+self.data
        if(not original):
            img = cv2.resize(img,(scale_to_px, scale_to_px), interpolation = cv2.INTER_AREA)
        cv2.imshow("Image - scaled to "+str(scale_to_px)+" px", img)
        cv2.waitKey(int(time))
        cv2.destroyAllWindows()

    def load_txt(self, filepath="image.txt"):
        self.data = np.genfromtxt(filepath, delimiter=' ', dtype=int, encoding ='UTF-8')

    def save_txt(self, filepath="image.txt"):
        np.savetxt(filepath, self.data, fmt="%s")

    def save_image(self, filepath="image.png"):
        img = np.zeros((28,28))
        img = img+self.data*254
        cv2.imwrite(filepath, img)

    def load_image(self, filepath="image.png"):
        self.data = (cv2.imread(filepath, 0) / 254).astype(int)

    def to_string(self):
        numpyData = {"image": self.data}
        return json.dumps(numpyData, cls=NumpyArrayEncoder)

    def from_string(self,payload):
        decodedArrays = json.loads(payload)
        self.data = np.asarray(decodedArrays["image"])
        pass

    def load(self, imagepath):
        suf = pathlib.Path(imagepath).suffix
        if(suf == ".png"):
            self.load_image(imagepath)
        elif(suf == ".txt"):
            self.load_txt(imagepath)
        else:
            print("Wrong Type loading Image Data from "+ imagepath +" (only .png and .txt supported)")

    def save(self, imagepath):
        suf = pathlib.Path(imagepath).suffix
        if(suf == ".png"):
            self.save_image(imagepath)
            return pathlib.Path(imagepath).name
        elif(suf == ".txt"):
            self.save_txt(imagepath)
            return pathlib.Path(imagepath).name
        else:
            print("Wrong Type saving Image Data to "+ imagepath +" (only .png and .txt supported)")

    def from_frame(self,frame,min=100,max=200,size=400,camera=True):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if camera:
            img = gray[int((480-size)/2):int((480-size)/2+size),int((840-size)/2):int((640-size)/2+size)]
        else:
            img = gray[int((500-size)/2):int((500-size)/2+size),int((500-size)/2):int((500-size)/2+size)]
        img = cv2.resize(img,(56, 56), interpolation = cv2.INTER_AREA)
        img = cv2.GaussianBlur(img, (3,3), 0)
        img = cv2.Canny(image=img, threshold1=min, threshold2=max,)
        img = cv2.resize(img,(28, 28), interpolation = cv2.INTER_AREA)
        for x,row in enumerate(img):
            for y,element in enumerate(row):
                if(element == 0):
                    self.data[x][y] = int(0)
                else:
                    self.data[x][y] = int(1)

class Textgen:

    def __init__(self,text,x=0,y=9,shift=1,scale = 0.8,factor =6.5,background=None,speed=1):
        self.text = text
        self.scale = scale
        self.x = x
        self.y = y
        self.shift = shift
        self.factor = factor #describes how much x space a font needs
        self.background = background
        self.speed = speed

    def get_image(self):
        img = Image()
        img.insert_text(self.text,(self.x,self.y),scale=self.scale)
        self.x -= self.shift
        if 0 > self.text.__len__()*self.scale*self.factor +self.x :
            self.x = 0
        if self.background is not None:
            img+=self.background
        return img

    def get_text(self):
        text = self.text[self.current_frame*self.size:self.current_frame*self.size+(self.size)]+self.end
        #self.current_frame = (self.current_frame+1) % self.frames
        return text

    def getframe(self):
        return (self.get_image(),self.speed)

if __name__ == "__main__":
    txt = Textgen("youre not special",scale=0.6)
    while True:
        txt.get_image().show()



