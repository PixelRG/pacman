import pygame
from pygame.locals import *
from templateForNodesAndObjects import Vector
from constants import *
from sprite import Sprite

class Pacman(Sprite):
    def __init__(self, node):
        # inherits methods for movement and updating of nodes from sprite class
        Sprite.__init__(self,node)
        self.name = PACMAN
      
        self.setSpeed(90)
        self.colour = YELLOW
        self.collide_distance = int(5* TILEWIDTH / 16)
        self.direction =RIGHT # new change


    def update(self, dt):
        # updates position based on current position and speed
        self.position += self.directions[self.direction]*self.speed*dt 
        
        # Check for a valid keypress to change direction
        direction = self.getValidKey()

        # when pacman moves past its target, its target node updates
        # ensures continuous movement
        if self.overshot_target():
            
            self.current_node = self.target_node # updates its current node
            
            # gets a new target
            self.target_node = self.get_new_target_node(direction)
            
            # if target node is not the same current node,
            # updates direction
            if self.target_node != self.current_node:
                self.direction = direction
            else:
                self.target_node = self.get_new_target_node(self.direction)

            # this happens when pacman hits the edge or is at dead end
            if self.target_node == self.current_node:
                self.direction = STOP
            
            # updates position 
            self.reset_position()

        else:
            if self.is_opposite_direction(direction):
                self.reverse_movement()

    
    
    
    def getValidKey(self):
        # perform input key validation
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
        # verifies whether Pacman has eaten a pellet
        for pellet in pelletList:
            distance_to_pellet = self.position - pellet.position
            distance_to_pellet_squared = distance_to_pellet.magnitudeSquared()
            distance_between_pellet_and_collidedistance = (pellet.radius + self.collide_distance)**2

            
            if distance_to_pellet_squared <= distance_between_pellet_and_collidedistance:
                return pellet
        return None
    

    def check_ghost_collision(self,ghost):
        distance = self.position - ghost.position
        squared_distance = distance.magnitudeSquared()

        # collide_distance -> the minimum distance for a collision to happen
        collide_distance = (self.collide_distance+ghost.collide_distance)
        squared_collide_distance= collide_distance**2

        if squared_distance <= squared_collide_distance:
            return True # collision has happened
        
        return False