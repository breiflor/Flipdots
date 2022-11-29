import numpy as np
import cv2

class Image:

    def __init__(self,imagepath=None):
        self.data = np.eye(28,dtype=int) # creates eigen matrix
        print(self.data)

    def setData(self,data):
        self.data = data

    def getPanels(self,id):
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

    def load_txt(self):
        pass

    def load_image(self):
        pass
    
    def save_txt(self):
        pass

if __name__ == "__main__":
    image = Image()
    print(image.getPanels(0))
    image.show()
