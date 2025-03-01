# this template will be inherited for pacman and gohsts
from templateForNodesAndObjects import Vector
from constants import *
import pygame
from random import randint
class Object:
    def __init__(self, node):
            self.name = None
            self.directions = {STOP:Vector(), UP:Vector(0,-1), DOWN:Vector(0,1), LEFT:Vector(-1,0), 
        RIGHT:Vector(1,0)}
            self.direction = STOP
            self.setSpeed(100)
            self.directionMethod = self.randomDirection
            self.radius = 10
            self.colour = WHITE
            self.node = node
            self.setPosition()
            self.target = node
            self.collide_distance = 5
            self.visible = True
            self.goal = None


    def setSpeed(self, speed):
        self.speed = speed * TILEWIDTH / 16
    def setPosition(self):
        self.position = self.node.position.copy()

    def update(self, dt):
        self.position += self.directions[self.direction]*self.speed*dt 
        
        if self.overshotTarget():
            self.node = self.target
            directions = self.validDirections()
            direction = self.directionMethod(directions)
            self.target = self.getNewTarget(direction)
            if self.target is not self.node:
                self.direction = direction
            else:
                self.target = self.getNewTarget(self.direction)

            
            self.setPosition()

        

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
    

    def validDirections(self):
        directions = []
        for key in [UP,DOWN,LEFT,RIGHT]:
            if self.validDirection(key):
                if key != self.direction *-1:
                    directions.append(key)

        if len(directions) == 0:
            directions.append(self.direction * -1)
        return directions
    
    def randomDirection(self,directions):
        return directions[randint(0,len(directions)-1)]
    
    def getNewTarget(self, direction):
        if self.validDirection(direction):
            return self.node.neighbours[direction]
        return self.node
    
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


    def render(self, screen,offset_x = 0, offset_y = 0):
        if self.visible:
            pos = (self.position.x + offset_x, self.position.y + offset_y)
            pygame.draw.circle(screen, self.colour, (int(pos[0]), int(pos[1])), self.radius)
