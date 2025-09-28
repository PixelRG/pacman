import pygame
from templateForNodesAndObjects import Vector
from nodesinmaze import *
from constants import *
import numpy as np



# def add_power_pellets_to_corners():
#     with open("pellettestfile.txt") as file:
#         maze = [list(line.strip()) for line in file]

#     height = len(maze)
#     width = len(maze[0])

#     corners = [(1,1), (1,width - 2), (height-2,1), (height-2, width - 2)]

#     for y,x in corners:
#         if 0 <= y <= height and 0 <= x < width:
#             maze[y][x] = "P"


#     modified_map = ["".join(line) for line in maze]
    
#     with open('pellettestfile.txt', 'w') as f:
#         f.write('\n'.join(modified_map))



# add_power_pellets_to_corners()


class Pellet():
    def __init__(self,row,column):
        self.name = PELLET
        self.position = Vector(column * TILEWIDTH, row * TILEWIDTH )
        self.colour = WHITE
        self.radius = int(4 * TILEWIDTH / 16)
        self.colliderADIUS = int(4* TILEWIDTH / 16)
        self.points = 10
        self.visible = True

    def render(self,screen):
        if self.visible:
            position = self.position.asInt()

            pygame.draw.circle(screen, self.colour,position,self.radius)



class Powerpellet(Pellet):
    def __init__(self,row,column):
        Pellet.__init__(self,row,column)
        self.name = POWERPELLET
        self.radius = int(8 * TILEWIDTH / 16)
        self.points = 50
        self.flashTime = 0.2
        self.timer = 0

    def update(self,dt):
        self.timer = self.timer + dt
        if self.timer >= self.flashTime:
            self.visble = not(self.visible)
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
                    self.pelletList.append(Powerpellet(row,col))
                    self.powerpellets.append(Powerpellet(row,col))

    def readPelletfile(self, textfile):
        with open(textfile, 'r') as f:
            data = [list(line.strip()) for line in f]  # Split lines into characters
        return np.array(data)  #  2D array

    def isEmpty(self):
        if len(self.pelletList) == 0:
            return True
        
        return False
    
    def render(self,screen):
        for pellet in self.pelletList:
            pellet.render(screen)

