import pygame
from templateForNodesAndObjects import Vector
from nodesinmaze import * 
from constants import *
from object import Object
from modes import ModeController
from random import randint
import heapq

class PriorityQueue:
    def __init__(self):
        self.elements = []
        self.entry_counter = 0
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority,self.entry_counter,item))
        self.entry_counter += 1

    def get(self):
        return heapq.heappop(self.elements)[2]
                           

class Ghost(Object):
    def __init__(self,node,pacman = None, blinky = None):
        Object.__init__(self,node)
        self.name = GHOST
        self.directionMethod = self.goalDirection
        self.setSpeed(100)
        self.points = 200
        self.goal = Vector()
        self.pacman = pacman
        self.mode = ModeController(self)
        self.homeNode = node
        self.blinky = blinky
        self.current_path = []
        self.path_update_interval = 0.5  # the route gets updated by 0.5s
        self.path_update_timer = 0 # the start timer
        self.fright_colour = BLUE


    def accessDirections(self): # used for checking of nearby nodes in aStarAlgorithm
        if self.mode.current == SPAWN:
            return [UP] # Ghosts can only go up when returning home
        return [UP,DOWN,LEFT,RIGHT]
    
    def manhattenDistance(self,pos1,pos2): # used for estimating the distance to the goal direction
        return abs(pos1.x - pos2.x) + abs(pos1.y-pos2.y)
    
    def aStarSearch(self,start,goal):
        frontier = PriorityQueue()
        frontier.put(start,0) # adds the node that the ghost is on
        came_from = {} # dict object that stores the predeccesor node for each node

        cost_so_far = {} # dict object that stores the culmulative cost for each node
                        # the cost is the number of steps taken

        came_from[start] = None # start node is set to none in the dict
        cost_so_far[start] = 0 # cost of start is 0
        self.current_path = [] # the path being made

        while not frontier.empty():
            current = frontier.get() # it gets the node with the lowest priority ie cost

            if current not in cost_so_far:
                continue
            if current == goal:
                break
            
            for direction in self.accessDirections():
                next_node = current.neighbours[direction] # it explores every valid neighbouring node
                if next_node == None:
                    continue

                new_cost = cost_so_far[current] + 1 # the cost to is incremented by 1 because we are storing cost of next node

                if next_node not in cost_so_far or new_cost < cost_so_far[next_node]: #checks if the next node is been added to cost dict
                    priority = new_cost + self.manhattenDistance(next_node.position, goal.position) # it estimates the total distance to the goal
                    frontier.put(next_node,priority) # the next node is put into the queue
                    came_from[next_node] = current # the next node references to the current node in the came from dict

        current = goal
        while current != start:
            if current not in came_from:
                return []
            self.current_path.insert(0,current)
            current = came_from[current]
        return self.current_path
    

    def showSpeed(self):
        return self.speed
        
    def update(self,dt):
        self.mode.update(dt)
        self.path_update_timer += dt
        if self.path_update_timer >= self.path_update_interval:
            self.path_update_timer = 0
            if self.mode.current == SCATTER:
                self.scatter()
            elif self.mode.current == CHASE:
                self.chase()

        if self.mode.current == FRIGHT:
            if self.mode.limitingTime - self.mode.timer < 3:
                if int((self.mode.limitingTime - self.mode.timer) * 5) % 2 == 0:
                    self.colour = WHITE
                else:
                    self.colour = self.fright_colour

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
            self.colour = self.fright_colour
    def normalMode(self):
        self.setSpeed(100)
        self.directionMethod = self.goalDirection
        self.colour = self.defaultcolour  # Reset to original colour

    def goalDirection(self,directions):
        if self.pacman and self.node:
            path = self.aStarSearch(self.node,self.pacman.node)

        if path:
            next_node = path[0]
            vec = next_node.position - self.node.position
            return self.vectorToDirection(vec) # this is called to decide the direction the ghost has to go to reach the next node
        
        if self.mode.current == SPAWN:
            if self.mode and self.homeNode:
                path = self.aStarSearch(self.node,self.spawnNode)

                if path:
                    next_node = path[0]
                    vec = next_node.position - self.node.position
                    return self.vectorToDirection(vec) # this is called to decide the direction the ghost has to go to reach the next node
                
            
        distances = []
        for direction in directions:
            vec = self.node.position + self.directions[direction]*TILEWIDTH - self.goal
            distances.append(vec.magnitudeSquared())
        return directions[distances.index(min(distances))]
    
    def vectorToDirection(self,vector):
        if vector.x > 0: 
            return RIGHT
        if vector.x < 0:
            return LEFT
        
        if vector.y > 0:
            return DOWN
        return UP
    
    def reset(self):
        Object.reset(self)
        self.points = 200
        self.directionMethod = self.goalDirection

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
            self.colour = self.defaultcolour
            self.spawn()
            self.path_update_timer = self.path_update_interval

    def render(self, screen, offset_x=0, offset_y=0):
        super().render(screen, offset_x, offset_y)
        SHOW_PATH = True
        if SHOW_PATH:  # Add a constant SHOW_PATH = True/False
            for node in self.current_path:
                pos = node.position + Vector(offset_x, offset_y)
                pygame.draw.circle(screen, YELLOW, (int(pos.x), int(pos.y)), 4)

class Blinky(Ghost):
    def __init__(self,node,pacman = None, blinky = None):
        Ghost.__init__(self,node,pacman, blinky)
        self.name = BLINKY
        self.defaultcolour = RED
        self.colour = self.defaultcolour
        self.visible = True


class Pinky(Ghost):
    def __init__(self,node, pacman = None, blinky = None):
        Ghost.__init__(self,node,pacman,blinky)
        self.name = PINKY
        self.defaultcolour = PINK
        self.colour = self.defaultcolour
        self.visible = True

    def scatter(self):
        self.goal = Vector(TILEWIDTH*COLS,0)

    def chase(self):
        self.goal = self.pacman.position + self.pacman.directions[self.pacman.direction] * TILEWIDTH *4


class Inky(Ghost):
    def __init__(self, node, pacman = None, blinky = None):
        Ghost.__init__(self,node,pacman,blinky)
        self.name =INKY
        self.defaultcolour = TEAL
        self.colour = self.defaultcolour
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
        self.defaultcolour = ORANGE
        self.colour = self.defaultcolour
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





        
