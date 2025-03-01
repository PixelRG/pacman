import pygame
from pygame.locals import *
from templateForNodesAndObjects import Vector
from constants import *
from object import Object
class Pacman(Object):
    def __init__(self, node):
        self.name = PACMAN
        self.position = Vector(200, 400)
        self.directions = {STOP:Vector(), UP:Vector(0,-1), DOWN:Vector(0,1), LEFT:Vector(-1,0), 
    RIGHT:Vector(1,0)}
        self.direction = STOP
        self.setSpeed(100)
        self.radius = 10
        self.colour = YELLOW
        self.node = node
        self.setPosition()
        self.target = node
        self.collide_distance = 5
        self.visible = True

    def setPosition(self):
        self.position = self.node.position.copy()

    def update(self, dt):
        self.position += self.directions[self.direction]*self.speed*dt 
        direction = self.getValidKey()
        if self.overshotTarget():
            self.node = self.target
            self.target = self.getNewTarget(direction)
            if self.target is not self.node:
                self.direction = direction
            else:
                self.target = self.getNewTarget(self.direction)

            if self.target is self.node:
                self.direction = STOP
            
            self.setPosition()

        else:
            if self.oppositeDirection(direction):
                self.reverseDirection()

    
    
    
    def getValidKey(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_UP] or key_pressed[K_w]:
            return UP
        if key_pressed[K_DOWN] or key_pressed[K_s]:
            return DOWN
        if key_pressed[K_LEFT] or key_pressed[K_a]:
            return LEFT
        if key_pressed[K_RIGHT] or key_pressed[K_d]:
            return RIGHT
        return STOP
    
    


    
    def eatPellets(self,pelletList):
        for pellet in pelletList:
            if self.collideCheck(pellet):
                return pellet
        return None
    
    def collideGhost(self,ghost):
        return self.collideCheck(ghost)
    
    def collideCheck(self,other):
        distance_to_object = self.position - other.position
        distance_to_object_squared = distance_to_object.magnitudeSquared()
        distance_between_object_and_collidedistance = (other.radius + self.collide_distance)**2
        if distance_to_object_squared <= distance_between_object_and_collidedistance:
            return True
        
        return False

