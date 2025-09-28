from constants import *
from random import randint
class MainMode():
    def __init__(self):
        self.timer = 0
        self.scatter()

    def scatter(self):
        self.mode = SCATTER
        self.limitingTime = randint(5,9) # SUBJECT TO CHANGE
        self.timer = 0

    def chase(self):
        self.mode = CHASE
        self.limitingTime = 20
        self.timer = 0


    def update(self,dt):
        self.timer += dt
        if self.timer >= self.limitingTime:
            if self.mode == SCATTER:
                self.chase()

            elif self.mode == CHASE:
                self.scatter()


class ModeController():
    def __init__(self,entity):
        self.timer = 0
        self.limitingTime = None
        self.mainmode = MainMode()
        self.current = self.mainmode.mode
        self.entity = entity
    def getCurrentMode(self):
        return self.current
    def update(self,dt):
        self.mainmode.update(dt)
        if self.current == FRIGHT:
            self.timer += dt
            if self.timer >= self.limitingTime:
                self.time = None
                self.entity.normalMode()
                self.current = self.mainmode.mode


    def setFrightMode(self):
        if self.current in [SCATTER,CHASE]:
            self.timer = 0
            self.limitingTime = 7
            self.current = FRIGHT
        elif self.current == FRIGHT:
            self.timer = 0

