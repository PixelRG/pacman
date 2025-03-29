from make_maze import *

def generate_new_maze():
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
    while maze.add_wall_obstacle(extend=True):
        pass




def maze_to_map():
    GAME_MAP = generate_new_maze()
    GAME_MAP = maze.maze_to_2d_array()
    rows = len(GAME_MAP)
    cols = len(GAME_MAP[0])

    # Create a new maze with symbols
    converted_maze = []
    for i in range(rows):
        new_row = []
        for j in range(cols):
            if GAME_MAP[i][j] == 1:
                new_row.append("X") # Wall
            else: 
                new_row.append("+")
        converted_maze.append(new_row)

    # To print the converted maze (for demonstration)
        with open("mazecontainer.txt", "w") as file:
            for row in converted_maze:
                #print("".join(row))
                file.write("".join(row)+"\n")

    
def add_power_pellets_to_corners():
    with open("mazecontainer.txt") as file:
        maze = [list(line.strip()) for line in file]

    height = len(maze)
    width = len(maze[0])

    corners = [(1,1), (1,width - 2), (height-2,1), (height-2, width - 2)]

    for y,x in corners:
        if 0 <= y <= height and 0 <= x < width:
            maze[y][x] = "P"


    modified_map = ["".join(line) for line in maze]
    
    with open('mazecontainer.txt', 'w') as f:
        f.write('\n'.join(modified_map))

