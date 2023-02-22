import json
import time
import random
import math
from Image import *

class Pong:

    def __init__(self):
        self.state = "run"
        self.ball = [8,10]
        self.p1 = [0,0]
        self.p2 = [27,0]
        self.p1_l = 10
        self.p2_l = 10
        self.min = 5
        self.speed = 0.4
        self.b_speed = [1,1]


    def getframe(self):
        if self.state == "run":
            #move ball
            self.ball[0] += self.b_speed[0]
            self.ball[1] += self.b_speed[1]
            if self.ball[0] > 27:
                self.ball[0] = 27
            if self.ball[0] < 0:
                self.ball[0] = 0
            if self.ball[1] > 27:
                self.ball[1] = 27
            if self.ball[1] < 0:
                self.ball[1] = 0
            #check for borders
            #up and down
            if self.ball[1] == 0 or self.ball[1] == 27:
                self.b_speed[1] = -self.b_speed[1]
            if self.ball[0] == 0 or self.ball[0] == 27:
                self.game_over(self.ball[0]==27)
            #check if paddels reached
            if self.ball[0] == 1:
                if self.ball[1] in range(self.p1[1],self.p1[1]+self.p1_l):
                    factor = (self.ball[1]-self.p1[1])/(self.p1_l/2)-1
                    abs_speeed = abs(self.b_speed[0])+abs(self.b_speed[1])
                    if self.b_speed[0] < 0:
                        self.b_speed[0] = - math.floor(self.b_speed[0] * abs(factor)-0.1)
                    else:
                        self.b_speed[0] = - math.ceil(self.b_speed[0] * abs(factor)+0.1)
                    if self.b_speed[1] < 0:
                        self.b_speed[1] -= abs_speeed-abs(self.b_speed[0])
                    if self.b_speed[1] > 0:
                        self.b_speed[1] += abs_speeed-abs(self.b_speed[0])
            if self.ball[0] == 26:
                if self.ball[1] in range(self.p2[1],self.p2[1]+self.p2_l):
                    factor = (self.ball[1]-self.p2[1])/(self.p2_l/2)-1
                    abs_speeed = abs(self.b_speed[0])+abs(self.b_speed[1])
                    if self.b_speed[0] < 0:
                        self.b_speed[0] = - math.floor(self.b_speed[0] * abs(factor)-0.1)
                    else:
                        self.b_speed[0] = - math.ceil(self.b_speed[0] * abs(factor)+0.1)
                    if self.b_speed[1] < 0:
                        self.b_speed[1] -= abs_speeed-abs(self.b_speed[0])
                    if self.b_speed[1] > 0:
                        self.b_speed[1] += abs_speeed-abs(self.b_speed[0])
            #generate image
            image = Image()
            image.toggleDot(self.ball[0],self.ball[1])
            for p in range(self.p1[1],self.p1[1]+self.p1_l):
                if p < 28:
                    image.toggleDot(0,p)
            for p in range(self.p2[1],self.p2[1]+self.p2_l):
                if p < 28:
                    image.toggleDot(27,p)

            return (image,self.speed)
        else:
            image = Image()
            image.insert_text("Game",(0,8),scale=0.6)
            image.insert_text("over",(1,15),scale=0.7)
            return (image,-1)

    def control(self,input):
        if input == "UP":
            if self.p1[1] != 0:
                self.p1[1]-=1
        elif input == "DOWN":
            if self.p1[1]+self.p1_l != 28:
                self.p1[1]+=1
        elif input == "LEFT":
            if self.p2[1] != 0:
                self.p2[1]-=1
        elif input == "RIGHT":
            if self.p2[1]+self.p2_l != 28:
                self.p2[1]+=1

    def game_over(self,right):
        if right:
            self.p2_l -= 1
            self.p1_l += 1
        else:
            self.p2_l += 1
            self.p1_l -= 1
        if self.p1_l < self.min or self.p2_l < self.min:
            self.state = "game_over"
        else:
            time.sleep(3)
            self.b_speed = [1,1]
            self.ball = [8,10]

if __name__ == "__main__":
    snake = Snake()
    while(1):
        snake.getframe()[0].show(1)
