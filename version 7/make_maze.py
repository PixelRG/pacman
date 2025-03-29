
# in this program, we will need into input data that gives a starting strcture of the maze.
# the input data must have:
#   -all of its edges must be covered by waals
# the reason why having this data will make it simpler for make a maze that is always guaranteed to mmaking no gaps in the edges
# each position of a maze will be referred to as TILE


import random
import sys
class Maze:
    def __init__(self,width, height, map_layout):
        self.width, self.height = width, height
        self.map_layout = self.format_map_to_str(map_layout)
        self.available_positions = [] # this carries a list of all valid positions for adding walls. Each position is stored as a tuple format, as it stores coordinates
        self.connections = {}# This dictionary keeps a notes of the positions between each connected tile
                            # This will improve the algroithm performance

    """""
    format_map_to_str
    The maze will be represented as a single line inside a 1d array. This is far more easier than trying to convert
    it into a 2d array""
    """""
    # maze map converter
    def format_map_to_str(self,layout):
        map_list = [] # this will give the map of tiles in the form of a 1d array 
        for line in layout.splitlines():
            stripped_line = line.strip() # this removes any whitespaces in back or front
            for c in stripped_line:
                map_list.append(c)

        return map_list
    
    def maze_to_string(self):
        """Returns the maze as a string."""
        
        return "\n".join("".join(self.map_layout[y * self.width: (y + 1) * self.width]) for y in range(self.height))

    """""
    As the maze is represented as a single string, we need a way to each tile using indexing. However, the parameters
    we will use will be (x,y) coordinates so we need a converter from coordinates to an index 
    """""
    def xy_to_index_converter(self,x,y):
        index = x + (y*self.width)
        return index

    # This function will return  the content in the index (wall or a .)
    def get_tile(self,x,y):
        if self.valid(x,y):
            return self.map_layout[self.xy_to_index_converter(x,y)]
        else:
            return None

    # This checks if the coordinate of the walls being placed are inside the maze
    def valid(self,x,y):
        if 0<= x <= self.width and 0<= y <= self.height:
            return True
        

    # This function ensures there is room to add a 2x2 blocks
    # We add 4 rather than 2 so we can have empty space between blocks and hence create paths
    def can_new_block_fit(self,x,y):
        for y_position in range(y,y+4):
            for x_position in range(x,x+4):
                if self.get_tile(x_position,y_position) != ".":
                    return False
        return True
    

    # wall adding algorithms
    def set_tile(self,x,y,tile):
        if self.valid(x,y):
            self.map_layout[self.xy_to_index_converter(x,y)] = tile
        
    def add_wall_block(self,x,y):
        for dx in range(2): # remember these loops start at 0
            for dy in range(2):
                self.set_tile(x+1+dx, y+1+dy, "|")



    # dictionary updating
    def add_wallconnection(self,x,y,dx,dy):
        coordinate = (x,y)
        for step in range(1,3):
            adjacent_coordinate = (x+ (dx*step), y+(dy*step))
            if adjacent_coordinate in self.available_positions:
                self.connections.setdefault(adjacent_coordinate,[]).append(coordinate)

    # this looks through the tiles nearby and updates the dictionary by adding the position of the wall
    def update_wallconnections(self):
        for y in range(self.height):
            for x in range(self.width):
                if (x,y) in self.available_positions:
                    for dx,dy in [(-1,0),(1,0),(0,-1),(-1,-1)]:
                        for vertical in range(4):
                            if self.get_tile(x+4*dx,y + vertical*dy) == "|": 
                                self.add_wallconnection(x,y,dx,dy)
                                break


    # available position updating
    def update_available_positions(self):
        self.available_positions = []
        for y in range(self.height):
            for x in range(self.width):
                if self.can_new_block_fit(x,y):
                    self.available_positions.append((x,y))

    # this is used to update the list and dictionary
    def update(self):
        self.update_available_positions()
        self.update_wallconnections()

    # this function aims to keep a record of the positions of the tiles that were accessed by keeping them in visited list
    # the function accesses the dictionary connections because it has to only put walls that are adjacent to existing walls
    # it only adds walls when at least one of the adjacent positions that were determined by the two for loops is a wall
    # the purpose of wall count is to ensure only 4 walls are added
    def expand_wall(self,x,y):
        # This expands walls using a recursive technique
        visited = []
        def expand(x, y):
            if (x,y) in visited:
                return 0
            visited.append((x,y))
            wallcount = 0
            if (x,y) in self.connections:
                for x0,y0 in self.connections[(x,y)]:
                    if not all(self.get_tile(x + dx, y + dy) == '|' for dx in range(2) for dy in range(2)):
                        self.add_wall_block(x0, y0)
                        wallcount += 1

                    wallcount += expand(x0,y0)
            return wallcount

        return expand(x,y)


    def add_wall_obstacle(self, extend=False):
        """Adds a wall obstacle at a random position and expands the walls."""
        self.update()
        if not self.available_positions:
            return False

        x, y = random.choice(self.available_positions)
        self.add_wall_block(x, y)
        count = self.expand_wall(x, y)

        if extend:
            directions = [(0, -1), (0, 1), (1, 0), (-1, 0)]
            dx, dy = random.choice(directions)
            max_blocks =  4 + (4 if random.random() <= 0.35 else 0)
            for step in range(max_blocks):
                x0, y0 = x + dx * step, y + dy * step
                if (x0, y0) not in self.available_positions:
                    break
                if not all(self.get_tile(x0 + i, y0 + j) == '|' for i in range(2) for j in range(2)):
                    self.add_wall_block(x0, y0)
                    count += 1 + self.expand_wall(x0, y0)
                if step >= 4 and random.random() <= 0.35 :
                    dx, dy = -dy, dx

        return True

    def maze_to_2d_array(self):
        grid = []
        maze = self.maze_to_string()
        for line in maze.splitlines():
            word = line[:16] + line[:16][::-1]
            row = []
            for char in word:
                if char == "|":
                    char = 1
                else:
                    char = 0
                row.append(char)
            grid.append(row)
        return grid

maze = Maze(16,  24,  """
    ||||||||||||||||
    |...............
    |...............
    |...............
    |...............
    |...............
    |...............
    |...............
    |...............
    |.........||||||
    |.........||||||
    |.........||||||
    |.........||||||
    |.........||||||
    |...............
    |...............
    |...............
    |...............
    |...............
    |...............
    |...............
    |...............
    |...............
    ||||||||||||||||""")

# Generate the maze with obstacles
while maze.add_wall_obstacle(extend=True):
    pass

# with open("mazecontainer.txt", "w") as file:
#     for line in maze.maze_to_string().splitlines():
#         newline = line[:16] + line[:16][::-1]
#         file.write(newline + "\n")




            
        

    

   
