# this template will be inherited for pacman and gohsts
from templateForNodesAndObjects import Vector
from constants import *
import pygame
from random import randint



class Sprite:
    def __init__(self, node):
            self.name = None
            # Vector directions mapped to certain directions
            # Stores the directions that the ghost or Pacman go to
            self.directions = {STOP:Vector(), UP:Vector(0,-1), DOWN:Vector(0,1), LEFT:Vector(-1,0), 
        RIGHT:Vector(1,0)}
            
            # movement properties
            self.direction = STOP
            self.setSpeed(100)

            self.directionMethod = self.choose_random_direction # the ghost will move randomly
            self.radius = 10 # visual size
            self.colour = WHITE

            # attributes store node positions
            self.current_node = node # current occupied node
            self.reset_position() # align position with current node
            self.target_node = node # next node moving towards
            self.navigation_goal = None # target position for pathfinding

            # gameplay properties
            self.collide_distance = 5
            self.visible = True


    def setSpeed(self, speed):
        # converts tile based speed to pixel movement rate
        self.speed = speed * TILEWIDTH / 16


    def reset_position(self):
        # updates position
        self.position = self.current_node.position.copy()

    def update(self, dt):
        # move in current direction 
        self.position += self.directions[self.direction]*self.speed*dt 
        
        if self.overshot_target():
            # if sprite is at target node -> get new direction
            self.current_node = self.target_node
            directions = self.get_available_directions()
            direction = self.directionMethod(directions) # Use AI strategy
            self.target_node = self.get_new_target_node(direction)

            # Only change direction if valid path exists
            if self.target_node is not self.current_node:
                self.direction = direction
            else: # No valid path -> continue moving with current direction
                self.target_node = self.get_new_target_node(self.direction)

            self.reset_position() 

        

    def overshot_target(self):
        if self.target_node is not None:
            vec_to_target = self.target_node.position -self.current_node.position
            vec_to_self = self.position -self.current_node.position
            current_node2target_node = vec_to_target.magnitudeSquared()
            current_node2Self = vec_to_self.magnitudeSquared()
            return current_node2Self >= current_node2target_node
        return False
    
    def is_direction_valid(self, direction):
        # checks if direction leads to a node
        if direction is not STOP:
            if self.current_node.neighbours[direction] is not None:
                return True
        return False
    

    def get_available_directions(self):
        # it gets directions
        # by deafult the ghost object cannot go backwards unless it's at dead end
        directions = [] # stores all valid directions
        for key in [UP,DOWN,LEFT,RIGHT]:
            if self.is_direction_valid(key):
                if key != self.direction *-1:
                    # prevents reversing 
                    directions.append(key)

        if len(directions) == 0:
            # when directions is empty, ghost is at a dead end
            # this situation will need reversing
            directions.append(self.direction * -1)
        return directions
    
    def choose_random_direction(self,directions):
        # makes ghosts go random
        return directions[randint(0,len(directions)-1)]
    
    def get_new_target_node(self, direction):
        # gets next node in specified direction if it is valid
        if self.is_direction_valid(direction):
            return self.current_node.neighbours[direction]
        return self.current_node
    
    def reverse_movement(self):
        # allows for immediate 180 turn
        self.direction = self.direction * -1
        before = self.current_node 
        self.current_node = self.target_node
        self.target_node = before

    def is_opposite_direction(self,direction):
        # checks if the direction is revse of current movenet
        if direction != STOP:
            if direction == (self.direction * -1):
                return True
            
        return False


    def render(self, screen,offset_x = 0, offset_y = 0):
        if self.visible:
            pos = (self.position.x + offset_x, self.position.y + offset_y)
            pygame.draw.circle(screen, self.colour, (int(pos[0]), int(pos[1])), self.radius)
