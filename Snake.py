import json
import time
import random
from Image import *

class Snake:

    def __init__(self):
        self.state = "run"
        self.lenght = 3
        self.score = 0
        self.speed = 1 #time between frames
        self.head = [14,14]
        self.body = [  [14, 14],
                [13, 14],
                [12, 14],
                [12, 13]
            ]
        self.direction = 'RIGHT'
        self.change_to = self.direction
        self.fruit = None
        self.generate_fruit(s)

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
                self.score += 10
                self.generate_fruit()
            else:
                self.body.pop()

            for block in self.body[1:]:
                if self.head[0] == block[0] and self.head[1] == block[1]:
                    self.game_over()

            image = Image()
            snake = self.body.copy()
            for entry in snake:
                image.toggleDot(entry[0],entry[1])
            image.toggleDot(self.fruit[0],self.fruit[1])
            return (image,self.speed)
        else:
             #return Gameover image TODO
            return (Image(),-1)

    def control(self,input):
        self.change_to = input

    def game_over(self):
        self.state == "game_over"

if __name__ == "__main__":
    snake = Snake()
    while(1):
        snake.getframe()[0].show(1)
