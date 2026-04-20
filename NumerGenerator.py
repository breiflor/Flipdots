from Image import *
from Animation import *


import numpy as np

class NumberGenerator:

    def __init__(self,fontspath,distance=1):
        self.fonts = Animation(fontspath)
        self.distance = distance
        self.cache = {}

    def get_image(self,numbers,white=True):
        cache_key = (str(numbers), white)
        if cache_key in self.cache:
            return Image(data=np.copy(self.cache[cache_key].data))

        image = Image()
        for i,n in enumerate(str(numbers)) :
            image+= (self.fonts.get_entry(int(n))[0].shift_and_fill(0,i*(3+self.distance)))

        final_image = image if white else ~image
        self.cache[cache_key] = final_image

        return Image(data=np.copy(final_image.data))

if __name__ == "__main__":
    gen = NumberGenerator("numbers/numbers.json")
    gen.get_image(1287).show()


