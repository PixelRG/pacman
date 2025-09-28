
# region files
from templateForNodesAndObjects import Vector
import pygame
from constants import * 

# region Pause
class Pause():
    def __init__(self,paused = False):
        self.paused = paused
        self.timer = 0 
        self.pauseTime = None
        self.func = None


    def update(self,dt):
        if self.pauseTime != None:
            self.timer += dt
            if self.timer >= self.pauseTime:
                self.timer = 0 
                self.paused = False
                self.pauseTime = None
                return self.func
        return None
        
    def setPause(self,pause = None, pauseTime = None, func = None):
        self.timer = 0
        self.func = func
        self.pauseTime = pauseTime
        if pause != None:
            self.paused = pause
        else:
            self.paused = not self.paused


    def flip(self):
        self.paused = not self.paused



# region text
class Text():
    def __init__(self,text,colour,x,y,size, time = None, id = None, visible = True):
        self.id = id
        self.text = text
        self.colour = colour
        self.size = size
        self.visible = visible
        self.position = Vector(x,y)
        self.timer = 0
        self.lifespan = time
        self.label = None
        self.destroy = False
        self.setupFont("KarmaticArcade-6Yrp1.ttf")
        self.createLabel()

    def setupFont(self,fontpath):
        self.font = pygame.font.Font(fontpath,self.size)

    def createLabel(self):
        self.label = self.font.render(self.text,1,self.colour)


    def setText(self,newText):
        self.text = str(newText)

        self.createLabel()

    def update(self,dt):
        if self.lifespan != None:
            self.timer += dt
            if self.timer >= self.lifespan:
                self.timer = 0

                self.lifespan = None
                self.destroy = True

    def render(self,screen):
        if self.visible:
            x,y = self.position.asTuple()
            screen.blit(self.label,(x,y))

class TextBar:
    def __init__(self,screen_width):
        self.font = pygame.font.SysFont("arial",24)
        self.score = 0
        self.level = 1
        self.score_pos = (10,10)

        self.level_pos = (screen_width - 150, 10)

    def update_score(self, new_score):
        self.score = new_score
    
    def update_level(self,new_level):
        self.level = new_level

    def draw(self,screen):
        score_text = self.font.render(f"Score: {self.score}", True, PAC_YELLOW)
        level_text = self.font.render(f"Level: {self.level}", True, PAC_YELLOW)
        pygame.draw.rect(screen, CHARCOAL, (self.score_pos[0]-5, self.score_pos[1]-5, 200, 30))
        pygame.draw.rect(screen, CHARCOAL, (self.level_pos[0]-5, self.level_pos[1]-5, 200, 30))

        screen.blit(score_text,self.score_pos)
        screen.blit(level_text,self.level_pos)


# region: sprite

BASETILEWIDTH = 16
BASETILEHEIGHT = 16

class Spritesheet:
    def __init__(self):
        self.sheet = pygame.image.load("spritesheet.png").convert()
        transcolour = self.sheet.get_at((0,0))
        self.sheet.set_colourkey(transcolour) # make background transparent

    def scale_sheet(self):
        width = int(self.sheet.get_width() / BASETILEHEIGHT * TILEWIDTH)
        height = int(self.sheet.get_height() / BASETILEHEIGHT *TILEHEIGHT)

        self.sheet = pygame.transform.scale(self.sheet, (width,height))


    def get_sprite(self,grid_x,grid_y,width,height,rows,cols):
        x = grid_x * TILEWIDTH
        y = grid_y * TILEHEIGHT
        width = cols * TILEWIDTH
        height = rows * TILEHEIGHT
        return self.sheet.subsurface((x, y, width, height))
    
