from constants import *

class MainMode():
    def __init__(self):
        self.timer = 0
        self.scatter()

    def scatter(self):
        self.mode = SCATTER
        self.time = 7 # SUBJECT TO CHANGE
        self.timer = 0

    def chase(self):
        self.mode = CHASE
        self.time = 20
        self.timer = 0


    def update(self,dt):
        self.timer += dt
        if self.timer >= self.time:
            if self.mode == SCATTER:
                self.chase()

            elif self.mode == CHASE:
                self.scatter()


class ModeController():
    def __init__(self,entity):
        self.timer = 0
        self.time = None
        self.mainmode = MainMode()
        self.current = self.mainmode.mode
        self.entity = entity

    def update(self,dt):
        self.mainmode.update(dt)
        self.current = self.mainmode.mode