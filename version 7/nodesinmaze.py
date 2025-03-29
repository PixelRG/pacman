import pygame
import numpy as np
from templateForNodesAndObjects import Vector
from constants import *


class Node():
    def __init__(self,x,y):
        self.position = Vector(x,y)
        self.neighbours = {UP:None, DOWN:None, LEFT:None, RIGHT:None, PORTAL:None}
        self.access = {UP: [PACMAN,BLINKY,INKY,PINKY,CLYDE],
                       DOWN: [PACMAN,BLINKY,INKY,PINKY,CLYDE],
                       LEFT: [PACMAN,BLINKY,INKY,PINKY,CLYDE],
                       RIGHT: [PACMAN,BLINKY,INKY,PINKY,CLYDE]}
        

    
    def __hash__(self):
        return hash(self.position)
  

    def render(self,screen,offset_x = 0, offset_y = 0,homekey = None):
        node_colour = SILVER  # Default color (RED for normal node)
        if homekey and self.position.asTuple() == homekey:  # Compare positions
            node_colour = BLUE  # Color for homekey node (use any color you want)
        offset_pos = self.position + Vector(offset_x,offset_y)
        for n in self.neighbours.keys():
            if self.neighbours[n] is not None:
                line_start = offset_pos.asTuple()
                line_end = (self.neighbours[n].position+ Vector(offset_x,offset_y)).asTuple()
                pygame.draw.line(screen, WHITE, line_start, line_end, 4)                
                pygame.draw.circle(screen, node_colour, offset_pos.asInt(), 12)

    def denyAccess(self,direction,object):
        if object.name in self.access[direction]:
            self.access[direction].remove(object.name)

    def allowAccess(self,direction, object):
        if object.name not in self.access[direction]:
            self.access[direction].append(object.name)
   

class NodeGroup():
    def __init__(self,level):
        self.level = level
        self.nodesTable = {}
        self.node_symbol = ["+","P"]
        self.path_Symbol = ["."]
        data = self.readMazeFile(level)
        self.createNodeTable(data)
        self.connectHorizontally(data)
        self.connectVertically(data)
        self.homekey = None

        
    """
    - self.nodesTable is a dictionary (better way of accessing data rather than using an array)
        It uses the coordinate of each node
        coordinate: node object
    
    """
  
    def readMazeFile(self,textfile): # this produces a 2d array using the text file that is imported from the file test_run
        with open(textfile, 'r') as f:
            data = [list(line.strip()) for line in f]  # Split lines into characters
        return np.array(data)  #  2D array


    """ This is for createNodeTable
    - data.shape returns a tuple that shows the number of rows and the number
    of columns
    - data.shape[0] returns the number of rows
    - row represents y coordinate
    - col represents x coordinate


    """
    def createNodeTable(self,data,xoffset=0,yoffset=0):
        for row in list(range(data.shape[0])): # goes through y coordinate of a cell
            for col in list(range(data.shape[1])): # goes through x coordinate
                if data[row][col] in self.node_symbol:
                    x,y = self.constructKey(col + xoffset, row + yoffset)
                    self.nodesTable[(x,y)] = Node(x,y)


    """
    connect horizontally forms a connection between horizontal nodes
    - every node has a dictionary in built thanks to the class that contains LEFT,RIGHT,UP, DOWN
        - we can set the RIGHT or LEFT of a node to be equal to the adjacent node

    - the function iterates through each node horizontally
        if the current node is a wall, the functions discontinues the connection.
        it makes a new one when it finds a node
    """

    def connectHorizontally(self,data,xoffset = 0,yoffset=0):
        for row in range(data.shape[0]):
            key = None
            for col in range(data.shape[1]):
                if data[row][col] in self.node_symbol:
                    if key is None: 
                        key = self.constructKey(col + xoffset, row+yoffset)
                    else: # when key contains a tuple
                        otherkey = self.constructKey(col + xoffset, row + yoffset)
                        self.nodesTable[key].neighbours[RIGHT] = self.nodesTable[otherkey] # 
                        self.nodesTable[otherkey].neighbours[LEFT] = self.nodesTable[key] # 
                        key = otherkey # sets the key to now be the adjacent key that was used
                elif data[row][col] not in self.path_Symbol: # if the current node is a wall, the code ends the horizontal connection being formed
                    key = None  

   # transpose swaps the columns and rows       
    def connectVertically(self, data, xoffset=0, yoffset=0):
        dataT = data.transpose() 
        for col in range(dataT.shape[0]):
            key = None
            for row in range(dataT.shape[1]):
                if dataT[col][row] in self.node_symbol:
                    if key is None:
                        key = self.constructKey(col+xoffset, row+yoffset)
                    else:
                        otherkey = self.constructKey(col+xoffset, row+yoffset)
                        self.nodesTable[key].neighbours[DOWN] = self.nodesTable[otherkey]
                        self.nodesTable[otherkey].neighbours[UP] = self.nodesTable[key]
                        key = otherkey
                elif dataT[col][row] not in self.path_Symbol:
                    key = None
        
    def constructKey(self, x, y):
        return x * TILEWIDTH, y * TILEHEIGHT
    
    def getNodeFromTiles(self,x,y):
        key = self.constructKey(x,y)
        return self.nodesTable.get(key)
    def getStartTempNode(self):
        nodes = list(self.nodesTable.values())
        return nodes[0]
    
    def render(self,screen,offset_x = 0, offset_y = 0):
        for node in self.nodesTable.values():
            node.render(screen,offset_x,offset_y, homekey=self.homekey)

        

    def findPortalNodes(self,vertical_range = 10): # this needs to be checked out
        nodes = list(self.nodesTable.values())
        
        all_y = [node.position.y for node in nodes]
        mid_y = (min(all_y) + max(all_y)) // 2
        candidates = []
        for node in nodes:
            if (mid_y - vertical_range <= node.position.y <= mid_y+vertical_range):
                if node.position[1]:
                    candidates.append(node)

        if len(candidates) >= 2:
            return candidates[0]

    def setupPortalPair(self, pair1, pair2):
        key1 = self.constructKey(*pair1)
        key2 = self.constructKey(*pair2)
        if key1 in self.nodesTable.keys() and key2 in self.nodesTable.keys():
            self.nodesTable[key1].neighbors[PORTAL] = self.nodesTable[key2]
            self.nodesTable[key2].neighbors[PORTAL] = self.nodesTable[key1]
    
    def createHomeNodes(self,xoffset,yoffset):# 11 columns wide (index 0-10)
        ghosthomedata = np.array([
            ['X', 'X', 'X', 'X', 'X', 'X', '+', 'X', 'X', 'X', 'X', 'X'],  # Row 0
            ['X', 'X', 'X', 'X', 'X', 'X', '.', 'X', 'X', 'X', 'X', 'X'],  # Row 1
            ['X', 'X', 'X', '+', 'X', 'X', '.', 'X', 'X', '+', 'X', 'X'],  # Row 2 (center)
            ['X', 'X', 'X', '+', '.', '.', '+', '.', '.', '+', 'X', 'X'],  # Row 3
            ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']   # Row 4
        ], dtype="<U1") 
    
        self.createNodeTable(ghosthomedata,xoffset,yoffset)
        self.connectHorizontally(ghosthomedata,xoffset,yoffset)
        self.connectVertically(ghosthomedata,xoffset,yoffset)
        self.homekey = self.constructKey(xoffset+6,yoffset)
        return self.homekey

    def connectGhostHomeNodes(self,homekey,otherKey,direction):
        key = self.constructKey(*otherKey)
        self.nodesTable[homekey].neighbours[direction] = self.nodesTable[key]
        self.nodesTable[key].neighbours[direction*-1] = self.nodesTable[homekey]


   

    def allowHomeAccess(self,object):
        self.nodesTable[self.homekey].allowAccess(DOWN,object)

    def denyHomeAccess(self,object):
        self.nodesTable[self.homekey].denyAccess(DOWN,object)

    
    