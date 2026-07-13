import time
import math
from Image import *

class Breakout:

    def __init__(self):
        self.state = "run"
        self.ball = [14, 14]
        self.paddle = 11 # x-coordinate of the left side of the paddle
        self.paddle_l = 6 # paddle length
        self.speed = 0.4
        self.b_speed = [1, -1] # ball moves right and up initially

        self.bricks = []
        for y in range(2, 10, 2):
            for x in range(2, 26, 3):
                self.bricks.append([x, y])
                self.bricks.append([x+1, y])

    def getframe(self):
        if self.state == "run":
            # Move ball
            self.ball[0] += self.b_speed[0]
            self.ball[1] += self.b_speed[1]

            # Constrain to grid
            if self.ball[0] > 27:
                self.ball[0] = 27
            if self.ball[0] < 0:
                self.ball[0] = 0
            if self.ball[1] > 27:
                self.ball[1] = 27
            if self.ball[1] < 0:
                self.ball[1] = 0

            # Wall collisions
            if self.ball[0] <= 0 or self.ball[0] >= 27:
                self.b_speed[0] = -self.b_speed[0]
                if self.ball[0] <= 0: self.ball[0] = 0
                if self.ball[0] >= 27: self.ball[0] = 27
            if self.ball[1] <= 0:
                self.b_speed[1] = -self.b_speed[1]
                self.ball[1] = 0

            # Paddle collision
            if self.ball[1] >= 26 and self.b_speed[1] > 0:
                if self.ball[0] in range(self.paddle, self.paddle + self.paddle_l):
                    # Base bounce logic on Pong.py paddle hit
                    factor = (self.ball[0] - self.paddle) / (self.paddle_l / 2) - 1
                    abs_speed = abs(self.b_speed[0]) + abs(self.b_speed[1])

                    if self.b_speed[0] < 0:
                        self.b_speed[0] = - math.floor(abs(self.b_speed[0]) * abs(factor) - 0.1)
                    else:
                        self.b_speed[0] = math.ceil(abs(self.b_speed[0]) * abs(factor) + 0.1)

                    if self.b_speed[0] == 0:
                        self.b_speed[0] = 1 if factor > 0 else -1 if factor < 0 else 0

                    # Fix speed y
                    self.b_speed[1] = -(abs_speed - abs(self.b_speed[0]))

                    # Ensure minimum y speed
                    if self.b_speed[1] >= 0:
                        self.b_speed[1] = -1

            if self.ball[1] >= 27:
                if self.b_speed[1] > 0:
                    self.game_over(win=False)

            # Brick collisions
            hit_brick = -1
            for i, brick in enumerate(self.bricks):
                if self.ball[0] == brick[0] and self.ball[1] == brick[1]:
                    hit_brick = i
                    break

            if hit_brick != -1:
                brick = self.bricks.pop(hit_brick)
                # Determine bounce direction. A simple implementation is to reverse y direction if hitting top/bottom, x if hitting side.
                # Since ball moves 1 step per frame, we just reverse y for simplicity for now.
                self.b_speed[1] = -self.b_speed[1]

            if len(self.bricks) == 0:
                self.game_over(win=True)

            # Generate image
            image = Image()
            image.toggleDot(self.ball[0], self.ball[1])
            for p in range(self.paddle, self.paddle + self.paddle_l):
                if p < 28:
                    image.toggleDot(p, 26)
            for brick in self.bricks:
                image.toggleDot(brick[0], brick[1])

            return (image, self.speed)
        else:
            image = Image()
            if self.win:
                image.insert_text("You", (0, 8), scale=0.6)
                image.insert_text("Win!", (1, 15), scale=0.7)
            else:
                image.insert_text("Game", (0, 8), scale=0.6)
                image.insert_text("over", (1, 15), scale=0.7)
            return (image, -1)

    def control(self, input):
        if input == "LEFT":
            if self.paddle > 0:
                self.paddle -= 1
        elif input == "RIGHT":
            if self.paddle + self.paddle_l < 28:
                self.paddle += 1

    def game_over(self, win):
        self.state = "game_over"
        self.win = win

if __name__ == "__main__":
    breakout = Breakout()
    while(1):
        breakout.getframe()[0].show(1)
