import pygame
import numpy as np
from templateForNodesAndObjects import Vector
from constants import *


class Node():
    def __init__(self,x,y):
        self.position = Vector(x,y)
        self.neighbours = {UP:None, DOWN:None, LEFT:None, RIGHT:None, PORTAL:None}
        self.colour = SILVER


    def render(self,screen):
        for n in self.neighbours.keys():
            if self.neighbours[n] is not None: 
                line_start = self.position.asTuple()
                line_end = self.neighbours[n].position.asTuple() 
                pygame.draw.line(screen, WHITE, line_start, line_end, 4) # displays the connection between nodes          
                pygame.draw.circle(screen, self.colour, self.position.asInt(), 12) # draws the nodes

class NodeManager:
    def __init__(self, maze_layout):
        self.nodeTable = {} # maps (x,y) coordinates to Node objects
        # Symbols from maze file: "x" and "P" are nodes, "," are paths
        self.node_symbols = {"+", "P"} 
        self.path_symbols = {"."} 
        # Maze layout loaded as a 2D numpy array for grid traversao
        self.maze = self.load_maze(maze_layout) # saves the layout of the maze as an array
        self.instantiate_nodes() # Creates nodes from symbols in maze file
        self.build_graph() # connects nodes to form the graph
        self.gateway = None

    def load_maze(self, filename): 
        # converts text file "maze container" to an array
        with open(filename) as f:
            return np.array([list(line.strip()) for line in f]) 

    def instantiate_nodes(self): 
        # Instantiates nodes using PIXEL coordinates
        rows, cols = self.maze.shape
        for y in range(rows):
            for x in range(cols):
                if self.maze[y][x] in self.node_symbols:
                    # px,py represent pixel_x and pixel_coordinate
            
                    px, py = x * TILEWIDTH + OFFSET_X , y * TILEHEIGHT + OFFSET_Y

                    #new node is added into the table
                    self.nodeTable[(px, py)] = Node(px, py) 

    
    
    def join_nodes(self,node1,dir1,node2,dir2): # forms bidirectional connections
        #if statement validates if the directions are opposite
        if dir1 * -1 == dir2: 
            node1.neighbours[dir1] = node2
            node2.neighbours[dir2] = node1
        else:
            return None

    

    def connect_horizontal(self, data, x_offset=0, y_offset=0):
        rows, cols = data.shape
        for y in range(rows):
            prev = None
            for x in range(cols):
                # Calculate actual grid position with offsets
                grid_x = x
                grid_y = y
                
                current = self.get_node(grid_x, grid_y,x_offset,y_offset)
                if current:
                    if prev:
                        self.join_nodes(prev, RIGHT, current, LEFT)
                    prev = current
                else:
                    prev = None  # Break chain at walls

    def connect_vertical(self, data, x_offset=0, y_offset=0):
        
        rows, cols = data.shape
        for x in range(cols):
            prev = None
            for y in range(rows):
                # Calculate actual grid position with offsets
                
                grid_x,grid_y = x,y
                current = self.get_node(grid_x, grid_y,x_offset,y_offset)
                if current:
                    if prev:
                        self.join_nodes(prev, DOWN, current, UP)
                    prev = current
                else:
                    prev = None  # Break chain at walls

    def build_graph(self):
        self.connect_horizontal(self.maze, OFFSET_X,OFFSET_Y)
        self.connect_vertical(self.maze,OFFSET_X,OFFSET_Y)




    def get_node(self, x, y, offset_x =0 ,offset_y = 0): # retrieves the node
        # convert grid (x,y) to pixel coordinates to retrieve a Node object
        return self.nodeTable.get((x * TILEWIDTH + offset_x, y * TILEHEIGHT + offset_y))


    def getStartTempNode(self): # returns the first node(top corner node)
        nodeTable = list(self.nodeTable.values())
        return nodeTable[0]
    
    def render(self,screen):
         # iterates through the nodes to render them
        for node in self.nodeTable.values(): 
            node.render(screen)

    def render_one_node(self,node,colour,screen):
        node.colour = colour
        node.render(screen)

    def create_ghost_home(self, grid_x, grid_y):
        home_data = np.array([
            ['X','X','X','X','X','X','+','X','X','X','X','X'],
            ['X','X','X','X','X','X','+','X','X','X','X','X'],
            ['X','X','X','+','X','X','+','X','X','+','X','X'],
            ['X','X','X','+','+','+','+','+','+','+','X','X'],
            ['X','X','X','X','X','X','X','X','X','X','X','X']
        ])
        
        # Calculate pixel offsets based on grid position
        x_offset = grid_x * TILEWIDTH + OFFSET_X
        y_offset = grid_y * TILEHEIGHT + OFFSET_Y
        
        # Create nodes for ghost home
        for y in range(5):
            for x in range(12):
                if home_data[y][x] in self.node_symbols:
                    px = x * TILEWIDTH + x_offset
                    py = y * TILEHEIGHT + y_offset
                    self.nodeTable[(px, py)] = Node(px, py)
        
        # Connect nodes within ghost home
        self.connect_horizontal(home_data, x_offset, y_offset)
        self.connect_vertical(home_data, x_offset, y_offset)
        
        # Rretuns the centre grid position
        return (grid_x + 6, grid_y)
    def connect_home_exit(self, home_center, maze_pos, direction):
        """Simplified version of connectGhostHomeNodes"""
        # Convert grid positions to pixel coordinates
        
        # home_center = center of ghost home in grid coordinates
        # maze_pos = connecting point in main maze grid coordinates
        home_px = home_center[0] * TILEWIDTH + OFFSET_X
        home_py = home_center[1] * TILEHEIGHT + OFFSET_Y
        maze_px = maze_pos[0] * TILEWIDTH + OFFSET_X
        maze_py = maze_pos[1] * TILEHEIGHT + OFFSET_Y
        
        # Get node objects
        home_node = self.nodeTable.get((home_px, home_py))
        maze_node = self.nodeTable.get((maze_px, maze_py))

        # to validate home node has been made
        home_node.colour = WHITE

        
        # Create bidirectional connection
        if home_node and maze_node:
            self.join_nodes(home_node, direction, maze_node, direction * -1)