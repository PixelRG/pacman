import pygame
from constants import *
from MCPACMAN import Pacman
from nodesinmaze import NodeGroup
from make_maze_to_text import *
class GameEngine():
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode(SCREENSIZE,0,32)
        self.background = None
        self.clock = pygame.time.Clock()

    def startGame(self):
        self.setBackground()
       
        self.nodes = NodeGroup("mazecontainer.txt")
   
        self.pacman = Pacman(self.nodes.getStartTempNode())
        

    def setBackground(self):
        self.background = pygame.surface.Surface(SCREENSIZE).convert()
        self.background.fill((0,100,100))

    def update(self):
        dt = self.clock.tick(30) / 1000
        self.pacman.update(dt)
        self.checkEvents()
        self.render()

    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

    
    def render(self):
        
        self.screen.blit(self.background,(0,0))
     
        self.nodes.render(self.screen)
        self.pacman.render(self.screen)
        pygame.display.update()


def run():
    maze_to_map()
    game = GameEngine()
    game.startGame()
    while True:
        game.update()


run()