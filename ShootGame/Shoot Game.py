import pygame
import random
import time

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
pygame.init()
screen_width = 900
screen_height = 500
screen = pygame.display.set_mode([screen_width, screen_height])
pygame.display.set_caption('Shoot Game')
global loclist, listtogen, listtocheck
listtocheck = []
listtogen = []
loclist = []
loclist.append((300,180))
loclist.append((425,180))
loclist.append((550,180))
loclist.append((300,330))
loclist.append((550,330))
loclist.append((220,350))
loclist.append((630,350))
loclist.append((500,15))

class dude():
    not_shootingGraphic = pygame.image.load("Sprites/1.png")
    shootingGraphic = pygame.image.load("Sprites/2.png")
    deadGraphic = pygame.image.load("Sprites/circlespam.png")
    def createGraphics(self):
        self.graphics.append(dude.not_shootingGraphic)
        self.graphics.append(dude.shootingGraphic)
        self.graphics.append(dude.deadGraphic)
    def __init__(self,loc):
        self.graphics = []
        self.createGraphics()
        self.loc = loc
        self.time = pygame.time.get_ticks() + 3000
        self.removetime = 0
        self.currentgraphic = 0
        self.dead = False
    def drawself(self):
        if pygame.time.get_ticks() > self.time and not self.dead:
            self.currentgraphic = 1
        elif not self.dead:
            self.currentgraphic = 0
        else:
            self.currentgraphic = 2
            if self.removetime < pygame.time.get_ticks():
                global loclist, listtogen, listtocheck
                listtogen.remove(self)
                listtocheck.remove(self.loc)
        target = self.graphics[self.currentgraphic]
        screen.blit(target, self.loc)
    def getshoot(self,x,y):
        loc = self.loc
        top = loc[1]
        left = loc[0]
        right = left + 300
        bottom = top + 300
        if x > left and x < right and y > top and y < bottom:
            self.currentgraphic = self.graphics[2]
            return True
        return False
def configsprites():
    background = pygame.image.load("Sprites/black.png")
    imgRect = background.get_rect()
    imgRect.centerx = screen.get_rect().centerx
    imgRect.centery = screen.get_rect().centery
    screen.blit(background,imgRect)

    if random.randint(1,100) == 1:
        print("ye")
        global loclist, listtocheck
        loc = loclist[random.randint(0,7)]
        print(loc)
        if not listtocheck.__contains__(loc):
            listtocheck.append(loc)
            listtogen.append(dude(loc))
    for guy in listtogen:
        guy.drawself()
    area = pygame.image.load("Sprites/area.png")
    imgRect = area.get_rect()
    imgRect.centerx = screen.get_rect().centerx
    imgRect.centery = screen.get_rect().centery
    screen.blit(area, imgRect)
    global cursor
    cursor = pygame.image.load("Sprites/crosshair.png")
    Mouse_x, Mouse_y = pygame.mouse.get_pos()
    loc = (Mouse_x - 21,Mouse_y - 21)
    screen.blit(cursor,loc)
    pygame.display.update()

done = False
while not done:
    configsprites()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            print("hello")
            pos = pygame.mouse.get_pos()
            for guy in listtogen:
                if guy.getshoot(pos[0],pos[1]):
                    guy.dead = True
                    guy.removetime = pygame.time.get_ticks() + 1000
                    pass

pygame.quit()