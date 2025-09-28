import pygame
from constants import *
from MCPACMAN import Pacman
from nodesinmaze import NodeGroup
from make_maze_to_text import *
from pellets import PelletGroup
from ghosts import GhostGroup
import random


class GameEngine():
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode(SCREENSIZE,0,32)
        self.background = None
        self.clock = pygame.time.Clock()
        self.debug_font = pygame.font.SysFont("Arial",24)

    def startGame(self):
        self.setBackground()
       
        self.nodes = NodeGroup("mazecontainer.txt")
        self.pellets = PelletGroup("mazecontainer.txt")
        homekey = self.nodes.createHomeNodes(9,9)
        self.nodes.connectGhostHomeNodes(homekey, (15,8),UP)
        # self.nodes.connectGhostHomeNodes(homekey,(10,8),UP)
        
        self.pacman = Pacman(self.nodes.getStartTempNode())
        self.ghosts = GhostGroup(self.nodes.getStartTempNode(),self.pacman)
        self.ghosts.setSpawnNode(self.nodes.getNodeFromTiles(15,9))
        

    def setBackground(self):
        self.background = pygame.surface.Surface(SCREENSIZE).convert()
        self.background.fill((0,0,0))

    def update(self):
        dt = self.clock.tick(30) / 1000
        self.pellets.update(dt)
        self.pacman.update(dt)
        
        self.ghosts.update(dt)
        self.checkGhostCollision()
        self.checkEvents()
        self.render()
    

    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

    def checkGhostCollision(self):
        for ghost in self.ghosts:
            if self.pacman.collideCheck(ghost):
                if ghost.mode.current == FRIGHT:
                    ghost.startSpawn()



    def render(self):
        
        self.screen.blit(self.background,(0,0))
     
        self.nodes.render(self.screen,OFFSET_X,OFFSET_Y)
        self.pellets.render(self.screen,OFFSET_X,OFFSET_Y)
        self.checkPellet()
        self.pacman.render(self.screen,OFFSET_X,OFFSET_Y)
        self.ghosts.render(self.screen,OFFSET_X,OFFSET_Y)
        self.renderDebugInfo()
        pygame.display.update()

    def renderDebugInfo(self):
        y_offset = 10
        ghost_index = 0
        
    
            # Get ghost-specific info
        mode = self.ghosts.blinky.mode.getCurrentMode()
        grid_x, grid_y = self.ghosts.blinky.getGridPosition()

        column = ghost_index // 2  # 0 for first column, 1 for second
        row = ghost_index % 2     # 0 or 1 for row in column
        
        x_position = 10 + (400 * column)
        y_offset = y_offset + (row * 120)  # 120px between ghosts in same column
            
        
        # Calculate remaining time
        remaining = 0
        if mode in [SCATTER, CHASE]:
            mainmode = self.ghosts.blinky.mode.mainmode
            remaining = max(0, mainmode.limitingTime - mainmode.timer)
        elif mode == FRIGHT:
            remaining = max(0, self.ghosts.blinky.mode.limitingTime - self.ghosts.blinky.mode.timer)
        elif mode == SPAWN:
            remaining = "N/A"

        # Create text surfaces
        name_text = f"{self.ghosts.blinky.name}:"
        mode_text = f"Mode: {mode}"
        pos_text = f"Position: ({grid_x}, {grid_y})"
        timer_text = f"Timer: {remaining:.1f}s" if isinstance(remaining, float) else f"Timer: {remaining}"

        #Check if Pacman collides with the ghost
        collision_text = "Collision with Ghost: No"
        if self.pacman.collideCheck(self.ghosts.blinky):
            collision_text = "Collision with Ghost: Yes"

        # Render text
        name_surface = self.debug_font.render(name_text, True, self.ghosts.blinky.colour)
        mode_surface = self.debug_font.render(mode_text, True, WHITE)
        pos_surface = self.debug_font.render(pos_text, True, WHITE)
        timer_surface = self.debug_font.render(timer_text, True, WHITE)
        collision_surface = self.debug_font.render(collision_text,True,WHITE)

        # Position texts
        x_position = 10   # Create two columns
        y_offset = y_offset
        
        self.screen.blit(name_surface, (x_position, y_offset))
        self.screen.blit(mode_surface, (x_position, y_offset + 30))
        self.screen.blit(pos_surface, (x_position, y_offset + 60))
        self.screen.blit(timer_surface, (x_position, y_offset + 90))
        self.screen.blit(collision_surface, (10, y_offset + 120))
        


    def checkPellet(self):
        pellet = self.pacman.eatPellets(self.pellets.pelletList)
        if pellet:
            self.pellets.number_of_eaten += 1
            self.pellets.pelletList.remove(pellet)

            if pellet.name== POWERPELLET:
                self.ghosts.startFright()

    # def renderDebugInfo(self):

    #     mode = self.ghost.mode.getCurrentMode()
    #     grid_x, grid_y = self.ghost.getGridPosition()
        
    #     remaining = 0
    #     if mode in [SCATTER, CHASE]:
    #         mainmode = self.ghost.mode.mainmode
    #         remaining = max(0, mainmode.limitingTime - mainmode.timer)
    #     elif mode == FRIGHT:
    #         remaining = max(0, self.ghost.mode.limitingTime - self.ghost.mode.timer)

    #     # Check if Pacman collides with the ghost
    #     collision_text = "Collision with Ghost: No"
    #     if self.pacman.collideCheck(self.ghost):
    #         collision_text = "Collision with Ghost: Yes"

    #     mode_text = f"Ghost Mode: {mode}"
    #     pos_text = f"Position: ({grid_x}, {grid_y})"
    #     timer_text = f"Time left: {remaining: .1f}s"

    #     #fps_text = f"FPS: {self.clock.get_fps():1.f}"
    #     mode_surface = self.debug_font.render(mode_text, True, WHITE)
    #     pos_surface = self.debug_font.render(pos_text, True, WHITE)
    #     timer_surface = self.debug_font.render(timer_text,True,WHITE)
    #     collision_surface = self.debug_font.render(collision_text, True, WHITE)

    #     # Display text
    #     y_offset = 10
    #     self.screen.blit(mode_surface, (10, y_offset))
    #     self.screen.blit(pos_surface, (10, y_offset + 30))
    #     self.screen.blit(timer_surface,(10,y_offset+60))
    #     self.screen.blit(collision_surface, (10, y_offset + 90)) 
def run():
    maze_to_map()
    add_power_pellets_to_corners()
    game = GameEngine()
    game.startGame()
    while True:
        game.update()



run()
