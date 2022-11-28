import numpy as np

class Image:

    def __init__(self):
        self.data = np.eye(28,dtype=int) # creates eigen matrix
        print(self.data)

    def setData(self,data):
        self.data = data

    def getPanels(self,id):
        panel = self.data[:,(0+id*7):(7+id*7)]
        panel_hex = bytearray()
        for row in panel :
            panel_hex.append(self.calculate_row(row))
        return panel_hex

    def calculate_row(self,row):
        val = np.matmul((row.reshape(1,7)),(np.array([1,2,4,8,16,32,64]).reshape(7,1)))
        return val[0][0].item()

    def visualize(self):
        pass

    def load_txt(self):
        pass

    def load_image(self):
        pass
    
    def save_txt(self):
        pass

if __name__ == "__main__":
    image = Image()
    print(image.getPanels(0))
