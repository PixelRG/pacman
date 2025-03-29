import pygame
from constants import *
from MCPACMAN import Pacman
from nodesinmaze import NodeManager
from make_maze_to_text import *
from pellets import PelletGroup
from ghosts import *
from pause import PauseManager
import random

class GameEngine():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREENSIZE,0,32)
        self.background = None
        self.clock = pygame.time.Clock()
        self.debug_font = pygame.font.SysFont("Arial",24)
        self.score = 0 
        self.high_score = self.load_high_score()
        self.pause_manager = PauseManager()
        self.score_multiplier = 1

    def startGame(self):
        self.setBackground()
        self.setup_graph() # initialises the nodes
        self.initialise_pellets()
        self.createGhostHome()
        
        self.initialise_Pacman()
        self.initialise_ghost()

# initialises the classes 
    def setup_graph(self):
        self.nodes = NodeManager("mazecontainer.txt")

    
    def createGhostHome(self): # creates ghost home
        self.gateway = self.nodes.create_ghost_home(9, 9)
        self.nodes.connect_home_exit(self.gateway, (15, 8), UP)


    def initialise_Pacman(self):
        # position of pacman is 0,0
        position_node = self.get_node(15,14)
        self.pacman = Pacman(position_node)

    def initialise_ghost(self):
        self.ghost_manager = GhostManager(self.pacman,self.nodes)
        self.ghosts = self.ghost_manager.retrieve_ghost_list()

        spawn_node = self.nodes.get_node(15,13)
        # Ghost starts at the exit node above the ghost home (grid position 15,8)
        
        
     
        # used to validate if the start node the ghost is at is valid

    def initialise_pellets(self):
        self.pellets = PelletGroup("mazecontainer.txt")

    # retrives nodes (automatically includes the offsets)
    def get_node(self,x,y):
        return self.nodes.get_node(x,y,OFFSET_X,OFFSET_Y)
    
    def retrieve_node_table(self): # retrieves all nodes 
        return self.nodes.nodeTable.values()
    

# sets background
    def setBackground(self):
        self.background = pygame.surface.Surface(SCREENSIZE).convert()
        self.background.fill(CHARCOAL) # black background

    def reset_maze_and_pellets(self):
        maze_to_map()
        add_power_pellets_to_corners()
        self.startGame()

    def update(self):
        # updates pacman,ghosts, pellets state
        # rechecks if user pressed X
        # update the screen
        dt = self.clock.tick(30) / 1000
        self.check_user_events()
        if not self.pause_manager.is_paused():
            
            self.pellets.update(dt)
            self.pacman.update(dt)
            self.ghost_manager.update(dt)
            self.check_ghost_collision()
            self.check_pellet()
        self.render()
    


    def check_user_events(self):
        # this exits
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.save_high_score() 
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.pause_manager.toggle()  # Toggle pause with spacebar

    def check_pellet(self):
        eaten_pellet = self.pacman.eatPellets(self.pellets.pelletList)
        if eaten_pellet: # if it is true
            self.pellets.number_of_eaten += 1
            
            self.pellets.pelletList.remove(eaten_pellet)
            if not self.pellets.pelletList: # happens whenall pellets are eaten
                self.reset_maze_and_pellets()
                return
        # added change
            if eaten_pellet.name== POWERPELLET:
                self.ghost_manager.start_fright() # remedial action done
                self.ghost_multiplier = 1  # Reset multiplier for new frightened period

            self.update_current_score(eaten_pellet.points)
            print(f"{eaten_pellet.points} pellet points have been added")
            
    def check_ghost_collision(self):
        for ghost in self.ghosts:
            if self.pacman.check_ghost_collision(ghost):
                
                if ghost.behaviour.get_current_behaviour() == FRIGHT:
                    # Pacman eats ghost
                    ghost.start_respawning()
                    points_awarded = ghost.points * self.ghost_multiplier
                    self.update_current_score(points_awarded)
                    
                    print(f"{points_awarded} GHOST POINTS have been added")
                    self.ghost_multiplier *= 2
                    print(f"all remaining ghosts are worth {self.ghost_multiplier * ghost.points}")

                    
                elif ghost.behaviour.get_current_behaviour() in [SCATTER, CHASE]:
                        # Pacman dies
                        print("Pacman died!")
                        # Add game reset logic here

                
    # display methpds
    def display_nodes(self):
        self.nodes.render(self.screen)

    def display_pellets(self):
        self.pellets.render(self.screen,OFFSET_X,OFFSET_Y)

    def display_pacman(self):
        self.pacman.render(self.screen)

    def display_ghost(self):
        self.ghost_manager.render(self.screen)
  


    def render(self):
    
        self.screen.blit(self.background,(0,0))
        self.display_nodes()
        self.display_pellets()
        self.display_pacman()
        self.display_ghost()
        self.renderDebugInfo()
        self.display_score()
        if self.pause_manager.is_paused():
            self.display_pause_message()
        pygame.display.update()
    
    def display_score(self):
        score_text = f"Score: {self.score}"
        high_score_text = f"High Score: {self.high_score}"

        y_offset = 0  # Adjust based on existing text
        self.screen.blit(self.debug_font.render(score_text, True, PAC_YELLOW), (600, y_offset))
        self.screen.blit(self.debug_font.render(high_score_text, True, PAC_YELLOW), (600, y_offset + 30))

    def display_pause_message(self):
        message = "Paused. PRESS SPACEBAR"
        message_surface = self.debug_font.render(message, True, (255, 255, 255))
        message_rect = message_surface.get_rect(center=(self.screen.get_width() // 2, 50))
        self.screen.blit(message_surface, message_rect)

    def renderDebugInfo(self):
        
        self.ghost = self.ghosts[0] # shows blinky's stats
        mode = self.ghost.behaviour.get_current_behaviour()
        grid_x, grid_y = self.ghost.getGridPosition()
        
        remaining = 0
        # Get remaining time based on current mode
        if mode == FRIGHT:
            remaining = max(0, self.ghost.behaviour.frightened_duration - self.ghost.behaviour.timer)
        else:
            remaining = max(0, self.ghost.behaviour.behaviour_types.duration - self.ghost.behaviour.behaviour_types.timer)

        # Create text surfaces
        mode_text = f"Ghost Mode: {mode}"
        pos_text = f"Position: ({grid_x}, {grid_y})"
        timer_text = f"Time left: {remaining:.1f}s"
        fps_text = f"FPS: {self.clock.get_fps():.1f}"

        # Render text
        y_offset = 10
        self.screen.blit(self.debug_font.render(mode_text, True, WHITE), (10, y_offset))
        self.screen.blit(self.debug_font.render(pos_text, True, WHITE), (10, y_offset + 30))
        self.screen.blit(self.debug_font.render(timer_text, True, WHITE), (10, y_offset + 60))
        self.screen.blit(self.debug_font.render(fps_text, True, WHITE), (10, y_offset + 90))

    def highlight_node(self,node):
        self.nodes.render_one_node(node,WHITE,self.screen)

    def load_high_score(self):
        try:
            with open("highestscore.txt", "r") as file:
                return int(file.read())
        except (FileNotFoundError, ValueError):
       
            with open("highestscore.txt", "w") as file:
                file.write("0")
        return 0
        
    def save_high_score(self):
        with open("highestscore.txt","w") as file:
            file.write(str(self.high_score))

    def update_current_score(self,points):
        self.score += points
        self.high_score = max(self.score, self.high_score)
    
def run():
    maze_to_map()
    add_power_pellets_to_corners()
    game = GameEngine()
    game.startGame()
    while True:
        game.update()





run()
