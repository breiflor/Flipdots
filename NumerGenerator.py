from Image import *
from Animation import *


class NumberGenerator:

    def __init__(self,fontspath,distance=1):
        self.fonts = Animation(fontspath)
        self.distance = distance

    def get_image(self,numbers,white=True):
        image = Image()
        for i,n in enumerate(str(numbers)) :
            image+= (self.fonts.get_entry(int(n))[0].shift_and_fill(0,i*(3+self.distance)))
        if(white):
            return image
        else:
            return  ~image

if __name__ == "__main__":
    gen = NumberGenerator("numbers/numbers.json")
    gen.get_image(1287).show()


