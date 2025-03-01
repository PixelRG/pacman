import pygame
from templateForNodesAndObjects import Vector
from constants import *
from object import Object
from modes import ModeController
from random import randint
class Ghost(Object):
    def __init__(self,node,pacman = None):
        Object.__init__(self,node)
        self.name = GHOST
        self.colour = CYAN
        self.directionMethod = self.goalDirection
        self.setSpeed(100)
        self.points = 200
        self.goal = Vector(9,15)
        self.pacman = pacman
        self.mode = ModeController(self)

    def getGridPosition(self):
        return (self.position.x // TILEWIDTH, self.position.y // TILEHEIGHT)
    
    def update(self,dt):
        self.mode.update(dt)
        if self.mode.current == SCATTER:
            self.scatter()
        elif self.mode.current == CHASE:
            self.chase()
        Object.update(self,dt)

    def scatter(self):
        self.goal = Vector() # this position is (0,0)

    def chase(self):
        self.goal = self.pacman.position


    def startFright(self):
        self.mode.setFrightMode()
        if self.mode.current == FRIGHT:
            self.setSpeed(30)
            self.directionMethod = self.randomDirection

    def normalMode(self):
        self.setSpeed(100)
        self.directionMethod = self.goalDirection

    def goalDirection(self,directions):
        distances = []
        for direction in directions:
            length = self.node.position + self.directions[direction] * TILEWIDTH - self.goal
            distances.append(length.magnitudeSquared())

        index_for_smallest_length = distances.index(min(distances))

        return directions[index_for_smallest_length]
    




    
