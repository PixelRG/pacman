import pygame
from constants import *
from MCPACMAN import Pacman
from nodesinmaze import NodeGroup
from make_maze import *
from make_maze_to_text import *
from pellets import PelletGroup
from ghosts import GhostGroup
from userInterface import *
import random


class GameEngine():
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode(SCREENSIZE,0,32)
        self.background = None
        self.clock = pygame.time.Clock()
        self.debug_font = pygame.font.SysFont("Arial",28)
        self.textbar = TextBar(SCREENSIZE[0])
        self.pause = Pause(True)
        self.level = 0
        self.lives = 5
        self.score = 0

    def nextLevel(self):
        self.level += 1
        self.textbar.update_level(self.level)
        self.pause.paused = True
        self.generateNewMaze()
        self.startGame()
        



    def startGame(self):
        self.setBackground()
       
        self.nodes = NodeGroup("mazecontainer.txt")
        self.pellets = PelletGroup("mazecontainer.txt")
        homekey = self.nodes.createHomeNodes(9,9)
        self.nodes.connectGhostHomeNodes(homekey, (15,8),UP)

        self.pacman = Pacman(self.nodes.getNodeFromTiles(15,14))
        self.ghosts = GhostGroup(self.nodes.getStartTempNode(),self.pacman)
        self.ghosts.setSpawnNode(self.nodes.getNodeFromTiles(15,9))
        self.ghosts.blinky.setStartNode(self.nodes.getNodeFromTiles(15,8))
        self.ghosts.inky.setStartNode(self.nodes.getNodeFromTiles(15,12))
        self.ghosts.clyde.setStartNode(self.nodes.getNodeFromTiles(12,12))
        self.ghosts.pinky.setStartNode(self.nodes.getNodeFromTiles(18,12))

        
    def setBackground(self):
        self.background = pygame.surface.Surface(SCREENSIZE).convert()
        self.background.fill(CHARCOAL)

    def update(self):
        dt = self.clock.tick(30) / 1000
        self.pellets.update(dt)
        if not self.pause.paused:
            self.pacman.update(dt)
            self.ghosts.update(dt)
            self.checkGhostEvents()
        self.checkEvents()
        afterPauseMethod = self.pause.update(dt)

        if afterPauseMethod != None:
            afterPauseMethod()
        if self.lives <= 0:
            print("you died")

        self.render()
    

    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.pause.setPause()
                    

    def showObjects(self):
        self.pacman.visible = True
        self.ghosts.show()

    def hideObjects(self):
        self.pacman.visible = False
        self.ghosts.hide()
 

    def checkGhostEvents(self):
        for ghost in self.ghosts:
            if self.pacman.collideCheck(ghost):
                if ghost.mode.current == FRIGHT:
                    self.textbar.update_score(ghost.points)
                    self.pacman.collideposition = self.pacman.position.copy()
                    self.pacman.collide_node = self.pacman.node
                    self.pacman.collide_target = self.pacman.target
                    self.pacman.collide_direction= self.pacman.direction
                    
                    ghost.startSpawn()

                
                    self.pause.setPause(pause = True,pauseTime = 0.5, func = self.showObjects)
                elif ghost.mode.current != SPAWN:
                    if self.pacman.alive:
                        self.lives = self.lives - 1
                        self.pacman.die()
                       
                        if self.lives <=0:
                            self.pause.setPause(pauseTime = 3)
                        self.resetLevel()

                    

    def render(self):
        
        self.screen.blit(self.background,(0,0))
     
        self.nodes.render(self.screen,OFFSET_X,OFFSET_Y)
        self.pellets.render(self.screen,OFFSET_X,OFFSET_Y)
        self.checkPellet()
        self.pacman.render(self.screen,OFFSET_X,OFFSET_Y)
        self.ghosts.render(self.screen,OFFSET_X,OFFSET_Y)
        self.textbar.draw(self.screen)
        self.renderDebugInfo(GHOST)
        
        if self.pause.paused:
            self.displayPauseMessage()
        pygame.display.update()

    def renderDebugInfo(self,object):
        y_offset = 600
        x_position = 10

        if object == GHOST:
            # Get ghost-specific info (for example, using 'pinky' as the ghost)
            ghost = self.ghosts.pinky  # You can choose any ghost or cycle through them if you like
            mode = ghost.mode.getCurrentMode()
            grid_x, grid_y = ghost.getGridPosition()
            

            remaining = 0
            if mode in [SCATTER, CHASE]:
                mainmode = ghost.mode.mainmode
                remaining = max(0, mainmode.limitingTime - mainmode.timer)
            elif mode == FRIGHT:
                remaining = max(0, ghost.mode.limitingTime - ghost.mode.timer)
            elif mode == SPAWN:
                remaining = "N/A"

            # Create text surfaces for ghost info
            name_text = f"{ghost.name}:"
            mode_text = f"Mode: {mode}"
            pos_text = f"Position: ({grid_x}, {grid_y})"
            timer_text = f"Timer: {remaining:.1f}s" if isinstance(remaining, float) else f"Timer: {remaining}"
            speed_text = f"Speed of pacman: {self.pacman.showSpeed()}"
            lives_text = f"Lives left: {self.lives}"
            points_text = f"Points collected: {self.pellets.number_of_eaten}"

            # Check if Pacman collides with the ghost
            collision_text = "Collision with Pacman: No"
            if self.pacman.collideCheck(ghost):
                collision_text = "Collision with Pacman: Yes"

            # Render text for ghost info
            name_surface = self.debug_font.render(name_text, True, ghost.colour)
            mode_surface = self.debug_font.render(mode_text, True, WHITE)
            pos_surface = self.debug_font.render(pos_text, True, WHITE)
            timer_surface = self.debug_font.render(timer_text, True, WHITE)
            collision_surface = self.debug_font.render(collision_text, True, WHITE)
            speed_surface = self.debug_font.render(speed_text,True, WHITE)
            lives_surface = self.debug_font.render(lives_text,True,WHITE)
            points_surface = self.debug_font.render(points_text,True,WHITE)

            # Display ghost info on the screen
            self.screen.blit(name_surface, (x_position, y_offset+100))
            self.screen.blit(mode_surface, (x_position, y_offset + 125))
            self.screen.blit(pos_surface, (x_position, y_offset + 150))
            self.screen.blit(timer_surface, (x_position, y_offset + 175))
            self.screen.blit(collision_surface, (x_position, y_offset + 200))
            #self.screen.blit(speed_surface,(x_position, y_offset +700))
            #self.screen.blit(lives_surface,(x_position,y_offset + 800))
            #self.screen.blit(points_surface, (x_position + 600, y_offset))

        else:
            # Pacman-specific info
            grid_x,grid_y = self.pacman.getGridPosition() # Get pacman's grid position
            #pacman_lives = self.pacman.lives  # If you track pacman lives, show it here

            pacman_pos_text = f"Pacman Position:{grid_x},{grid_y}"
            #pacman_lives_text = f"Lives: {pacman_lives}"

            # Render text for pacman info
            pacman_pos_surface = self.debug_font.render(pacman_pos_text, True, WHITE)
            # pacman_lives_surface = self.debug_font.render(pacman_lives_text, True, WHITE)

            # Display pacman info on the screen
            self.screen.blit(pacman_pos_surface, (x_position, y_offset+30))
            # self.screen.blit(pacman_lives_surface, (x_position, y_offset + 30))



    def checkPellet(self):
        pellet = self.pacman.eatPellets(self.pellets.pelletList)
        if pellet:
            self.score += pellet.points
            self.pellets.number_of_eaten += 1
            self.textbar.update_score(self.score)

            if pellet.name== POWERPELLET:
                self.ghosts.startFright()
            self.pellets.pelletList.remove(pellet)

        if self.pellets.isEmpty():
            self.hideObjects()
            self.nextLevel()

    def restartGame(self):
        self.lives = 5
        self.level = 0
        self.pause.paused = True
        self.startGame()

    def resetLevel(self):
        self.pause.paused = True
        self.pacman.reset()
        self.ghosts.reset()
      
        
    def generateNewMaze(self):
        
        # Create new random maze structure
        initial_layout = """
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
        ||||||||||||||||"""
        
        # Generate new maze
        maze = Maze(16, 24, initial_layout)
        while maze.add_wall_obstacle(extend=True):
            pass
        
        maze = maze.maze_to_2d_array()
        
        maze_to_map(maze)
        add_power_pellets_to_corners()
        
        # Convert to game format
       

    def displayPauseMessage(self):
    # Define the text message
        message = "Paused"
        
        # Render the message
        message_surface = self.debug_font.render(message, True, WHITE)
        
        # Calculate the position to center the message on the screen
        message_rect = message_surface.get_rect(center=(self.screen.get_width() // 2, 50))
        
        # Blit the message onto the screen
        self.screen.blit(message_surface, message_rect)


def run():
    
    game = GameEngine()
    game.generateNewMaze()
    game.startGame()
    while True:
        game.update()



run()



