import pygame
from constants import *
from MCPACMAN import Pacman
from nodesinmaze import NodeGroup
from make_maze_to_text import *
from pellets import PelletGroup
from ghosts import Ghost


class GameEngine():
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode(SCREENSIZE,0,32)
        self.background = None
        self.clock = pygame.time.Clock()

    def startGame(self):
        self.setBackground()
       
        self.nodes = NodeGroup("mazecontainer.txt")
        self.pellets = PelletGroup("mazecontainer.txt")
        self.ghost = Ghost(self.nodes.getStartTempNode())
        self.pacman = Pacman(self.nodes.getStartTempNode())
    
        

    def setBackground(self):
        self.background = pygame.surface.Surface(SCREENSIZE).convert()
        self.background.fill((0,0,0))

    def update(self):
        dt = self.clock.tick(30) / 1000
        self.pellets.update(dt)
        self.pacman.update(dt)
        self.ghost.update(dt)
        self.checkEvents()
        self.render()
    

    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

    
    def render(self):
        
        self.screen.blit(self.background,(0,0))
     
        self.nodes.render(self.screen)
        self.pellets.render(self.screen)
        self.checkPellet()
        self.pacman.render(self.screen)
        self.ghost.render(self.screen)
        pygame.display.update()

    def checkPellet(self):
        pellet = self.pacman.eatPellets(self.pellets.pelletList)
        if pellet:
            self.pellets.number_of_eaten += 1
            self.pellets.pelletList.remove(pellet)


def run():
    maze_to_map()
    add_power_pellets_to_corners()
    game = GameEngine()
    game.startGame()
    while True:
        game.update()


run()