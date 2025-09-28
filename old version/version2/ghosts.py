import pygame
from templateForNodesAndObjects import Vector
from constants import *
from object import Object

class Ghost(Object):
    def __init__(self,node):
        Object.__init__(self,node)
        self.name = GHOST
        self.colour = CYAN

        self.setSpeed(50)
        self.points = 200