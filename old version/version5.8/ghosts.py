# import pygame
# from constants import *
# from templateForNodesAndObjects import Vector
# from newmodes import BehaviourManager
# from random import randint
# from sprite import Sprite
# import heapq
# class Ghost(Sprite):
#     def __init__(self, node, pacman=None):
#         super().__init__(node)
#         self.name = GHOST
#         self.colour = CYAN
#         self.directionMethod = self.goalDirection
#         self.setSpeed(100)
#         self.points = 200
#         self.navigation_goal = Vector(9, 15)  # Default scatter target
#         self.pacman = pacman
#         self.behaviour = BehaviourManager(self)

#     def getGridPosition(self):
#         return (self.position.x // TILEWIDTH, self.position.y // TILEHEIGHT)
    
#     def update(self, dt):
#         self.behaviour.update(dt)
#         current_behaviour = self.behaviour.get_current_behaviour()
        
#         if current_behaviour == SCATTER:
#             self.scatter()
#         elif current_behaviour == CHASE:
#             self.chase()
        
#         super().update(dt)

#     def scatter(self):
#         self.navigation_goal = Vector()  # (0,0)

#     def chase(self):
#         if self.pacman is not None:
#             self.navigation_goal = self.pacman.position.copy()

#     def start_fright(self):
#         self.behaviour.set_fright_mode()
#         if self.behaviour.get_current_behaviour() == FRIGHT:
#             self.setSpeed(30)
#             self.directionMethod = self.choose_random_direction

#     def restore_normal_behaviour(self):
#         self.setSpeed(100)
#         self.directionMethod = self.goalDirection

#     def goalDirection(self, directions):
#         # Calculate direction that moves closest to goal
#         distances = []
#         for direction in directions:
#             vec = self.current_node.position + self.directions[direction]*TILEWIDTH
#             distances.append((vec - self.navigation_goal).magnitudeSquared())
#         return directions[distances.index(min(distances))]


import pygame
from constants import *
from templateForNodesAndObjects import Vector

from newmodes import BehaviourManager
from random import randint
from sprite import Sprite
import heapq

class PriorityQueue: # initialise the queue object
    def __init__(self):
        self.elements = [] # list to hold queue elements
        self.entry_counter = 0 # it's a counter that maintain order of elements
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, item, priority): # Adds item to the priority queue with priority
        heapq.heappush(self.elements, (priority,self.entry_counter,item))
        self.entry_counter += 1

    def get(self): # Retrives item with lowest priority
        return heapq.heappop(self.elements)[2]
                           

class Ghost(Sprite):
    def __init__(self, start_node, scatter_node,nodeTable, respawn_node, pacman=None):
        super().__init__(start_node)
        self.name = GHOST
        self.colour = CYAN
        self.directionMethod = self.goalDirection
        self.setSpeed(90)
        self.points = 200

        self.respawn_node = respawn_node  # location where ghost respawns
        self.scatter_node = scatter_node
        self.start_node = start_node
        self.navigation_goal = self.scatter_node.position.copy() # this needs to be vector
        
        if self.scatter_node and self.start_node and self.navigation_goal:
            print("Got the nodes")

        self.collide_distance = int(5* TILEWIDTH / 16)
        self.pacman = pacman
        self.behaviour = BehaviourManager(self)
        self.current_path = []
        self.path_update_interval = 0.5
        self.path_update_timer = 0
        self.fright_colour = BLUE
        self.default_colour = CYAN
      
        self.nodes = nodeTable
        
        print(scatter_node.position.asTuple())

    def getGridPosition(self):
        return (self.position.x // TILEWIDTH, self.position.y // TILEHEIGHT)
    
    

    def update(self, dt):
        self.behaviour.update(dt)
        current_behaviour = self.behaviour.get_current_behaviour()
        
        self.path_update_timer += dt
        if self.path_update_timer >= self.path_update_interval:
            self.path_update_timer = 0
            if current_behaviour == SCATTER:
                self.scatter()
            elif current_behaviour == CHASE:
                self.chase()
        
        if current_behaviour == FRIGHT:
            if self.behaviour.frightened_duration - self.behaviour.timer < 3:
                if int((self.behaviour.frightened_duration - self.behaviour.timer) * 5) % 2 == 0:
                    self.colour = WHITE
                else:
                    self.colour = self.fright_colour
        
        super().update(dt)

    def scatter(self):
        self.navigation_goal = self.scatter_node.position.copy()

    def chase(self):
        if self.pacman is not None:
            self.navigation_goal = self.pacman.position.copy()


    def start_respawning(self):
        if self.behaviour.get_current_behaviour() == FRIGHT:
            self.behaviour.activate_respawn_mode()
            self.setSpeed(150)
            self.navigation_goal = self.respawn_node.position.copy()
            self.directionMethod = self.goalDirection

    def accessDirections(self):
        # Add any special direction restrictions here if needed
        return [UP, DOWN, LEFT, RIGHT]

    def manhattanDistance(self, pos1, pos2):
        return abs(pos1.x - pos2.x) + abs(pos1.y - pos2.y)

    def aStarSearch(self, start, goal):
        frontier = PriorityQueue()
        frontier.put(start, 0)
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0
        self.current_path = []

        while not frontier.empty():
            current = frontier.get()

            if current == goal:
                break

            for direction in self.accessDirections():
                next_node = current.neighbours[direction]
                if next_node is None:
                    continue

                new_cost = cost_so_far[current] + 1
                if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                    cost_so_far[next_node] = new_cost
                    priority = new_cost + self.manhattanDistance(next_node.position, goal.position)
                    frontier.put(next_node, priority)
                    came_from[next_node] = current

        # Reconstruct path
        current = goal
        while current != start:
            if current not in came_from:
                return []
            self.current_path.insert(0, current)
            current = came_from[current]
            
        return self.current_path

    def goalDirection(self, directions):
        # Try A* pathfinding first
        target = None
        if self.behaviour.get_current_behaviour() == SCATTER:
            target = self.scatter_node
        elif self.behaviour.get_current_behaviour() == RESPAWN:
            target = self.respawn_node
        

        else:
            target = self.pacman.current_node

        if self.navigation_goal:
            target = self.find_nearest_node(self.navigation_goal)
            if target and self.current_node:
                path = self.aStarSearch(self.current_node, target)
                
                if path:
                    next_node = path[0]
                    vec = next_node.position - self.current_node.position
                    # print("A star code running")
                    return self.vectorToDirection(vec)
                

        # If A star fails, fallback to greedy search using Manhattan distance
        distances = []
        for direction in directions:
    
            current_vec = self.current_node.position + self.directions[direction] * TILEWIDTH
            # Compare vectors directly
            distances.append((current_vec - self.navigation_goal).magnitudeSquared())
            # print("Greedy first algorithm is being used")
        if distances:
            return directions[distances.index(min(distances))]
        return STOP # this is when Pacman and ghost are at the same position

    def vectorToDirection(self, vector):
        if vector.x > 0:
            return RIGHT
        if vector.x < 0:
            return LEFT
        if vector.y > 0:
            return DOWN
        return UP

    def start_fright(self):
        self.behaviour.set_fright_mode()
        if self.behaviour.get_current_behaviour() == FRIGHT:
            self.setSpeed(30)
            self.directionMethod = self.choose_random_direction
            self.colour = self.fright_colour

    def restore_normal_behaviour(self):
        self.setSpeed(90)
        self.directionMethod = self.goalDirection
        self.colour = self.default_colour

    def find_nearest_node(self, position): #NEWLY ADDED
        # Helper method to find nearest node to a position
        min_distance = float("inf") # set to infinity
        nearest_node = None
        for node in self.nodes.values():  # Assuming access to node list
            distance = (node.position - position).magnitudeSquared()
            if distance < min_distance:
                min_distance = distance
                nearest_node = node
        return nearest_node

    def reset(self):
        super().reset()
        self.position = self.start_node.position.copy()
        print("node copied")
        self.points = 200
        self.directionMethod = self.goalDirection

    def draw_target_indicator(self,screen):
        if self.navigation_goal:
            indicator_colour = BLACK
            target_pos = (int(self.navigation_goal.x), int(self.navigation_goal.y))

            pygame.draw.circle(screen,indicator_colour,target_pos,radius = 5)

    def render(self,screen):
        super().render(screen)
        self.draw_target_indicator(screen)
# region GHOSTS

class Blinky(Ghost):
    def __init__(self,start_node,scatter_node,nodeTable,respawn_node, pacman = None):
        super().__init__(start_node,scatter_node,nodeTable,respawn_node, pacman)
        self.name = BLINKY
        self.colour = RED
        self.default_colour = RED
        
        #self.visible = True

class Pinky(Ghost):
    def __init__(self, start_node, scatter_node, nodeTable,spawn_node, pacman=None):
        super().__init__(start_node, scatter_node, nodeTable,spawn_node,pacman)
        self.name = PINKY
        self.colour = PINK
        self.default_colour = PINK
        #self.visible = True

    def chase(self):
        # Target 4 tiles ahead of Pacman's direction
        if self.pacman and self.pacman.direction != STOP:
            target_offset = self.pacman.directions[self.pacman.direction] * TILEWIDTH * 4
            target_pos = self.pacman.position + target_offset
            self.navigation_goal = self.find_nearest_node(target_pos).position.copy()


class Inky(Ghost):
    def __init__(self, start_node, scatter_node, nodeTable,respawn_node, pacman=None,blinky = None):
        super().__init__(start_node, scatter_node, nodeTable, respawn_node, pacman)
        self.name = INKY
        self.colour = TEAL
        self.default_colour = TEAL
        self.blinky = blinky

    def chase(self):
        if self.pacman and self.blinky:
            # calculate inky target position
            # its target -> the tile that is 2 tiles ahead of Pacman
            pacman_dir = self.pacman.directions[self.pacman.direction]
            pivot = self.pacman.position + pacman_dir * TILEWIDTH * 2

            # calculate the vector from blinky to pivot
            blinky_to_pivot = pivot - self.blinky.position

            target_pos = self.blinky.position + blinky_to_pivot * 2

            target_node = self.find_nearest_node(target_pos)

            if target_node:
                self.navigation_goal = target_node.position.copy()


class Clyde(Ghost):
    def __init__(self, start_node, scatter_node, nodeTable,respawn_node, pacman=None):
        super().__init__(start_node, scatter_node, nodeTable, respawn_node, pacman)
        self.name = CLYDE
        self.colour = ORANGE
        self.default_colour = ORANGE
        

    def chase(self):
        distance = self.position - self.pacman.position
        distance_squared = distance.magnitudeSquared()

        threshold = (8 * TILEWIDTH)**2

        if distance_squared > threshold:
            self.navigation_goal = self.pacman.position.copy() # remedial action
            print("clyde will chase pacman")

        else:
            self.navigation_goal = self.scatter_node.position.copy()
            print("clyde will not chase Pacman")


class GhostManager():
    def __init__(self,pacman,nodes):
        self.pacman = pacman
        self.nodes = nodes
        self.initialise_ghosts()

    def initialise_ghosts(self):

        starting_node = self.nodes.get_node(15,12)

        spawn_node = self.nodes.get_node(15,13) # remedial action fix, i made spawn_node an attribute for all
        self.blinky = Blinky(starting_node,self.get_scatter_node(BLINKY),self.nodes.nodeTable,spawn_node,self.pacman)
        self.pinky = Pinky(starting_node,self.get_scatter_node(PINKY),self.nodes.nodeTable,spawn_node,self.pacman)
        self.inky = Inky(starting_node,self.get_scatter_node(INKY),self.nodes.nodeTable,spawn_node,self.pacman,self.blinky)
        self.clyde = Clyde(starting_node,self.get_scatter_node(CLYDE), self.nodes.nodeTable, spawn_node,self.pacman)
        self.ghosts = [self.blinky,self.inky,self.pinky,self.clyde]

    def get_scatter_node(self,corner):
        # these variables represent the corners of the maze
        top_left = self.nodes.get_node(1, 5)                  # top left
        top_right = self.nodes.get_node(COLS-2, 5)            # top right
        bottom_left = self.nodes.get_node(1, ROWS+2)          # bottom left corner
        bottom_right = self.nodes.get_node(COLS-2, ROWS+2)    # bottom right corner

        # contains the locations that each ghost has to patrol
        scatter_nodes = {BLINKY:top_left,
                         INKY:top_right,
                         CLYDE:bottom_left,
                         PINKY:bottom_right}

        if corner in scatter_nodes:
            return scatter_nodes[corner]
        


        
    def update(self,dt):
        for ghost in self.ghosts:
            ghost.update(dt)

    def render(self,screen):
        for ghost in self.ghosts:
            ghost.render(screen)

    def retrieve_ghost_list(self):
        return self.ghosts # returns all ghosts
    
    def start_fright(self): 
        for ghost in self.ghosts:
            ghost.start_fright()

    def reset(self): # resets all ghost states
        for ghost in self.ghosts:
            ghost.reset()
        



