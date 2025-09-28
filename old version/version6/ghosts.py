import pygame
from templateForNodesAndObjects import Vector
from constants import *
from object import Object
from modes import ModeController
from random import randint
class Ghost(Object):
    def __init__(self,node,pacman = None, blinky = None):
        Object.__init__(self,node)
        self.name = GHOST
        self.colour = CYAN
        self.directionMethod = self.goalDirection
        self.setSpeed(100)
        self.points = 200
        self.goal = Vector()
        self.pacman = pacman
        self.mode = ModeController(self)
        self.homeNode = node
        self.blinky = blinky

        
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
    

    # Spawn phase
    def spawn(self):
        self.goal = self.spawnNode.position

    def setSpawnNode(self, node):
        self.spawnNode = node

    def startSpawn(self):
        self.mode.setSpawnMode()
        if self.mode.current == SPAWN:
            self.setSpeed(150)
            self.directionMethod = self.goalDirection
            self.spawn()


class Blinky(Ghost):
    def __init__(self,node,pacman = None, blinky = None):
        Ghost.__init__(self,node,pacman, blinky)
        self.name = BLINKY
        self.colour = RED
        self.visible = True

class Pinky(Ghost):
    def __init__(self,node, pacman = None, blinky = None):
        Ghost.__init__(self,node,pacman,blinky)
        self.name = PINKY
        self.colour = PINK
        self.visible = True

    def scatter(self):
        self.goal = Vector(TILEWIDTH*COLS,0)

    def chase(self):
        self.goal = self.pacman.position + self.pacman.directions[self.pacman.direction] * TILEWIDTH *4

class Inky(Ghost):
    def __init__(self, node, pacman = None, blinky = None):
        Ghost.__init__(self,node,pacman,blinky)
        self.name =INKY
        self.colour = TEAL
        self.visible = True

    def scatter(self):
        self.goal = Vector(TILEWIDTH*COLS, TILEWIDTH * ROWS)

    def chase(self):
        vec1 = self.pacman.position + self.pacman.directions[self.pacman.direction] * 2 * TILEWIDTH

        vec2 = (vec1 - self.blinky.position) * 2

        self.goal = self.blinky.position + vec2


class Clyde(Ghost):
    def __init__(self, node, pacman = None, blinky = None):
        Ghost.__init__(self,node,pacman,blinky)
        self.name = CLYDE
        self.colour = ORANGE
        self.visible = True

    def scatter(self):
        self.goal = Vector(0,TILEWIDTH*ROWS)

    def chase(self):
        distance_to_pacman = self.pacman.position - self.position
        distance_squared = distance_to_pacman.magnitudeSquared()

        if distance_squared <= (TILEWIDTH * 8) **2:
            self.scatter()

        else:
            self.goal = self.pacman.position + self.pacman.directions[self.pacman.direction] * TILEWIDTH * 4



class GhostGroup():
    def __init__(self,node,pacman):
        self.blinky = Blinky(node,pacman)
        self.pinky = Pinky(node,pacman)
        self.inky = Inky(node,pacman,self.blinky)
        self.clyde = Clyde(node,pacman)
        self.ghosts = [self.blinky,self.pinky,self.inky,self.clyde]

    def __iter__(self):
        return iter(self.ghosts)
    

    def update(self,dt):
        for ghost in self.ghosts:
            ghost.update(dt)

    def startFright(self):
        for ghost in self.ghosts:
            ghost.startFright()
        self.resetPoints()

    def setSpawnNode(self, node):
        for ghost in self.ghosts:
            ghost.setSpawnNode(node)

    def updatePoints(self):
        for ghost in self.ghosts:
            ghost.points = ghost.points * 2

    def resetPoints(self):
        for ghost in self.ghosts:
            ghost.points = 200

    def reset(self):
        for ghost in self.ghosts:
            ghost.reset()

    def hide(self):
        for ghost in self.ghosts:
            ghost.visible = False

    def show(self):
        for ghost in self.ghosts:
            ghost.visible = True

    def render(self,screen,offset_x,offset_y):
        for ghost in self.ghosts:
            ghost.render(screen,offset_x,offset_y)





        
