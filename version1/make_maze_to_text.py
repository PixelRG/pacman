from make_maze import *

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
                # Check adjacent passages of each cell/tile
                passages = []
                # these conditions check the connections with the cell
                # if statements check the adjacent cells to the selected cell
                # Check up
                if i > 0 and GAME_MAP[i-1][j] == 0:
                    passages.append('up')
                # Check down
                if i < rows - 1 and GAME_MAP[i+1][j] == 0:
                    passages.append('down')
                # Check left
                if j > 0 and GAME_MAP[i][j-1] == 0:
                    passages.append('left')
                # Check right
                if j < cols - 1 and GAME_MAP[i][j+1] == 0:
                    passages.append('right')
                
                count = len(passages) 
                if count != 2: 
                    new_row.append("+")
                else:
                    # Check if directions are opposite
                    dir_set = {passages[0], passages[1]}
                    if dir_set in [{'up', 'down'}, {'left', 'right'}]:
                        new_row.append(".")
                    else:
                        new_row.append("+")
        converted_maze.append(new_row)

    # To print the converted maze (for demonstration)
        with open("mazecontainer.txt", "w") as file:
            for row in converted_maze:
                #print("".join(row))
                file.write("".join(row)+"\n")


