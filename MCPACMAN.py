import pygame
from pygame.locals import *
from templateForNodesAndObjects import Vector
from constants import *
class Pacman(object):
    def __init__(self, node):
        self.name = PACMAN
        self.position = Vector(200, 400)
        self.directions = {STOP:Vector(), UP:Vector(0,-1), DOWN:Vector(0,1), LEFT:Vector(-1,0), 
    RIGHT:Vector(1,0)}
        self.direction = STOP
        self.speed = 90
        self.radius = 10
        self.colour = YELLOW
        self.node = node
        self.setPosition()
        self.target = node
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

    def overshotTarget(self):
        if self.target is not None:
            vec1 = self.target.position -self.node.position
            vec2 = self.position -self.node.position
            node2Target = vec1.magnitudeSquared()
            node2Self = vec2.magnitudeSquared()
            return node2Self >= node2Target
        return False
    def validDirection(self, direction):
        if direction is not STOP:
            if self.node.neighbours[direction] is not None:
                return True
        return False
    def getNewTarget(self, direction):
        if self.validDirection(direction):
            return self.node.neighbours[direction]
        return self.node
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
    
    def reverseDirection(self):
        self.direction = self.direction * -1
        before = self.node 
        self.node = self.target
        self.target = before

    def oppositeDirection(self,direction):
        if direction != STOP:
            if direction == (self.direction * -1):
                return True
            
        return False


    def render(self, screen):
        p = self.position.asInt()
        pygame.draw.circle(screen, self.colour, p, self.radius)