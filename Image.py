import numpy as np
import cv2
import pathlib

class Image:

    def __init__(self,imagepath=None,data=np.eye(28,dtype=int)):
        self.data=data  # creates eigen matrix as default image
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

    def getData(self):
        return np.copy(self.data)

    def getPanel(self,id):
        panel = self.data[:,(0+id*7):(7+id*7)]
        panel_hex = bytearray()
        for row in reversed(panel) :
            panel_hex.append(self.calculate_row(row))
        return panel_hex

    def calculate_row(self,row):
        val = np.matmul((row.reshape(1,7)),(np.array([64,32,16,8,4,2,1]).reshape(7,1)))
        return val[0][0].item()

    def show(self,original=False,scale_to_px=500):
        img  = np.zeros((28,28))
        img = img+self.data
        if(not original):
            img = cv2.resize(img,(scale_to_px, scale_to_px), interpolation = cv2.INTER_AREA)
        cv2.imshow("Image - scaled to "+str(scale_to_px)+" px", img)
        cv2.waitKey(0)
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
        elif(suf == ".txt"):
            self.save_txt(imagepath)
        else:
            print("Wrong Type saving Image Data to "+ imagepath +" (only .png and .txt supported)")

if __name__ == "__main__":
    image = Image("image.png")
    image.show()
    image1 = Image("image.txt")
    (image-image1).show()



