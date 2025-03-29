import pygame
from templateForNodesAndObjects import Vector
from nodesinmaze import *
from constants import *
import numpy as np


class Pellet():
    def __init__(self,row,column):
        self.name = PELLET
        self.position = Vector(column * TILEWIDTH, row * TILEWIDTH )
        self.colour = LIGHT_GREEN
        self.radius = int(4 * TILEWIDTH / 16)
        self.colliderADIUS = int(4* TILEWIDTH / 16)
        self.points = 10
        self.visible = True

    def render(self, screen, offset_x=0, offset_y=0):  # Add offset params
        if self.visible:
            # Apply offsets to position
            x = self.position.x + offset_x
            y = self.position.y + offset_y
            pygame.draw.circle(screen, self.colour, (int(x), int(y)), self.radius)

class Powerpellet(Pellet):
    def __init__(self,row,column):
        Pellet.__init__(self,row,column)
        self.name = POWERPELLET
        self.radius = int(8 * TILEWIDTH / 16)
        self.points = 50
        self.flashTime = 0.4
        self.timer = 0

    def update(self,dt):
        self.timer = self.timer + dt
        if self.timer >= self.flashTime:
            self.visible = not(self.visible)
            self.timer = 0





class PelletGroup():
    def __init__(self,pelletfile):
        self.pelletList = []
        self.powerpellets = []
        self.createPelletList(pelletfile)
        self.number_of_eaten = 0
    
    def update(self,dt):
        for powerpellet in self.powerpellets:
            powerpellet.update(dt)
    
    def createPelletList(self,pelletfile):
        data = self.readPelletfile(pelletfile)
        for row in range(data.shape[0]):
            for col in range(data.shape[1]):
                if data[row][col] in [".","+"]:
                    self.pelletList.append(Pellet(row,col))
                elif data[row][col] in ["P"]:
                    pp = Powerpellet(row,col)
                    self.pelletList.append(pp)
                    self.powerpellets.append(pp)

    def readPelletfile(self, textfile):
        with open(textfile, 'r') as f:
            data = [list(line.strip()) for line in f]  # Split lines into characters
        return np.array(data)  #  2D array

    def isEmpty(self):
        if len(self.pelletList) == 0:
            return True
        
        return False
    
    def render(self, screen, offset_x=0, offset_y=0):  # Add offset params
        for pellet in self.pelletList:
            pellet.render(screen, offset_x, offset_y)  # Pass offsets

