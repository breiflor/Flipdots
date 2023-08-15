import json
import time
import random
from NumerGenerator import *
from Image import *

class Snake:

    def __init__(self):
        self.state = "run"
        self.lenght = 3
        self.score = 0
        self.speed = 0.5 #time between frames
        self.max_speed = 0.3
        self.head = [14,14]
        self.body = [  [14, 14],
                [13, 14],
                [12, 14],
                [12, 13]
            ]
        self.direction = 'RIGHT'
        self.change_to = self.direction
        self.fruit = None
        self.generate_fruit()
        self.name = "AAA"
        self.nam_at = 0
        self.highscore = {42 :"TES",43 :"TES",44 :"TES",442 :"FLO"}
        self.numgen = NumberGenerator("numbers/numbers.json")

    def generate_fruit(self):
        self.fruit = [random.randrange(1, 27, 1),
                      random.randrange(1, 27, 1)]
        for block in self.body[1:]:
            if self.fruit[0] == block[0] and self.fruit[1] == block[1]:
                self.generate_fruit()

    def getframe(self):
        if self.state == "run":
            if self.change_to == 'UP' and self.direction != 'DOWN':
                self.direction = 'UP'
            if self.change_to == 'DOWN' and self.direction != 'UP':
                self.direction = 'DOWN'
            if self.change_to == 'LEFT' and self.direction != 'RIGHT':
                self.direction = 'LEFT'
            if self.change_to == 'RIGHT' and self.direction != 'LEFT':
                self.direction = 'RIGHT'

                # Moving the snake
            if self.direction == 'UP':
                self.head[1] -= 1
            if self.direction == 'DOWN':
                self.head[1] += 1
            if self.direction == 'LEFT':
                self.head[0] -= 1
            if self.direction == 'RIGHT':
                self.head[0] += 1

            # let the snake pass the edges
            self.head[0]=self.head[0]%28
            self.head[1] = self.head[1] % 28

            self.body.insert(0, list(self.head))
            if self.head[0] == self.fruit[0] and self.head[1] == self.fruit[1]:
                self.score += 1
                if self.speed > self.max_speed:
                    self.speed -= self.speed*0.1
                self.generate_fruit()
            else:
                self.body.pop()

            for block in self.body[1:]:
                if self.head[0] == block[0] and self.head[1] == block[1]:
                    self.game_over()

            image = Image()
            snake = self.body.copy()
            for entry in snake:
                image.toggleDot(entry[1],entry[0])
            image.toggleDot(self.fruit[1],self.fruit[0])
            return (image,self.speed)
        elif self.state == "game_over":
             #return Gameover image TODO
            if self.change_to == 'UP' :
                name = list(self.name)
                name[self.nam_at] = chr(ord(self.name[self.nam_at])-1)
                self.name = "".join(name) 
            if self.change_to == 'DOWN':
                name = list(self.name)
                name[self.nam_at] = chr(ord(self.name[self.nam_at])+1)
                self.name = "".join(name) 
            if self.change_to == 'LEFT' :
                if self.nam_at > 0:
                    self.nam_at -= 1
            if self.change_to == 'RIGHT' :
                if self.nam_at < 2:
                    self.nam_at += 1
                else :
                    self.save_highcore()
            self.change_to = 'NONE' 
            image = Image()
            image.insert_text("Score",(0,7),scale=0.6)
            image.insert_text(self.name,(1,15),scale=0.7)
            image.insert_text("_",(self.nam_at*7+1,18),scale=0.7)
            image += self.numgen.get_image(self.score).shift_and_fill(20,2)
            return (image,0.5) # TODO check update speed
        elif self.state == "highscore":
            image = Image()
            for i in range(0,4):
                if len(self.highscore) > 0:
                    score, name = self.highscore.popitem()
                    image += self.numgen.get_image(score).shift_and_fill(i*7+1,17)
                    image.insert_text(name,(0,i*7+5),scale=0.5)

            return (image,-1)



    def save_highcore(self):
        self.highscore = json.load(open("snake_highscore.json",))
        self.highscore[self.score] = self.name
        new_dict = {}
        for ele,nam  in self.highscore.items():
            new_dict[int(ele)] = nam
        self.highscore = dict(sorted(new_dict.items()))
        json.dump(self.highscore,open("snake_highscore.json","wt"))
        self.state = "highscore"


    def control(self,input):
        self.change_to = input

    def game_over(self):
        self.state = "game_over"
        self.change_to = 'NONE'
        self.nam_at = 0

if __name__ == "__main__":
    snake = Snake()
    snake.state = "game_over"

    while(1):
        snake.getframe()[0].show()
