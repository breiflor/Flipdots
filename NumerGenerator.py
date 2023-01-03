from Image import *
from Animation import *


class NumberGenerator:

    def __init__(self,fontspath):
        self.fonts = Animation(fontspath)

    def get_image(self,numbers,white=True):
        image = Image()
        for i,n in enumerate(str(numbers)) :
            image+= (self.fonts.get_entry(int(n))[0].shift_and_fill(0,i*4))
        if(white):
            return image
        else:
            return  ~image

if __name__ == "__main__":
    gen = NumberGenerator("numbers/numbers.json")
    gen.get_image(1287).show()


