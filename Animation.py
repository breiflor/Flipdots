import pathlib
from Image import *
import json
import copy

class Animation:

    def __init__(self,path=None,loop=False):
        self.path = path

        self.image_list = []
        self.loop = loop
        self.current_index = 0
        if (path is not None):
            self.load(path)
        pass

    def __add__(self, other):
        self.image_list += other.get_list()

    def get_list(self):
        return self.image_list

    def merge(self):
        #FUTURE - idea
        pass

    def init(self,loop=False):
        self.loop = loop
        self.current_index = 0

    def animate_image(self,image,speed=1,vertical=False,loop=True,name="generic_animation"):
        self.loop = loop
        self.path = name
        if not vertical:
            for i in range(28):
                im = copy.deepcopy(image)
                im.shift_and_fill(0,i)
                self.image_list.append((copy.deepcopy(im), speed))
        else:
            for i in range(28):
                im = copy.deepcopy(image)
                im.shift_and_fill(i,0)
                self.image_list.append((copy.deepcopy(im), speed))

    def load(self,path):
        if (pathlib.Path(path).is_file()):
            file = path
        else:
            file = path+"/fd_animation_manifest.json"
        with open(file,"r") as json_file:
            self.parse_storage_list(json.load(json_file),str(pathlib.Path(file).parent))

    def store(self,path):
        if (pathlib.Path(path).is_file()):
            file = path
            dir = str(pathlib.Path(file).parent)+"/"
        else:
            dir = path
            file = path+"/fd_animation_manifest.json"
            pathlib.Path(path).mkdir(parents=True, exist_ok=True)
        storage_list = self.create_storage_list(dir)
        with open(file,"w") as json_file:
            json.dump(storage_list, json_file)

    def create_storage_list(self,path):
        storage_list = []
        for id,entry in enumerate(self.image_list):
            storage_list.append({"Filepath": entry[0].save(path+"/"+str(id)+".txt"), "Screentime" : entry[1] })
        return storage_list

    def parse_storage_list(self,list,dir):
        self.image_list = []
        self.init()
        for entry in list:
            self.image_list.append((Image(dir+"/"+entry["Filepath"]),entry["Screentime"]))

    def get_entry(self,id=0):
        return copy.deepcopy(self.image_list[id])

    def delete_entry(self,id):
        del self.image_list[id]

    def insert_entry(self,entry,after_id):
        self.image_list.insert(after_id,entry)

    def set_entry(self,entry,id):
        self.image_list[id] = entry

    def to_string(self):
        #if we want to send an Animation in completly serialized format
        storage_list = []
        for id,entry in enumerate(self.image_list):
            storage_list.append({"Frame": entry[0].to_string(), "Screentime" : entry[1] })
        return json.dumps(storage_list)

    def from_string(self,package):
        #if string is recieved in json format
        self.image_list = []
        self.init()
        list = json.loads(package)
        for entry in list:
            image = Image()
            image.from_string(entry["Frame"])
            self.image_list.append((image,entry["Screentime"]))


    def insert(self,image,duration=1):#duration is interpreted as seconds
        self.image_list.append((image,duration))

    def getframe(self):
        touple = self.image_list[self.current_index]
        if(len(self.image_list)) > (self.current_index+1):
            self.current_index += 1
            return touple
        else:
            if self.loop :
                self.current_index = 0
                return touple
            else:
                ret = (touple[0],-1) #indicates that the Animation has ended
                return ret




if __name__ == "__main__":
    animation = Animation()
    animation.insert(Image("logo.txt"),10)
    animation.insert(Image("test.png"),5)
    image,time = animation.getframe()
    print(time)
    image.show()
    image,time = animation.getframe()
    print(time)
    image.show()
    animation.store("default_animation")
    animation.load("default_animation")
    image,time = animation.getframe()
    print(time)
    image.show()
    image,time = animation.getframe()
    print(time)
    image.show()
    ana = Animation()
    ana.from_string(animation.to_string())
    image,time = ana.getframe()
    print(time)
    image.show()
