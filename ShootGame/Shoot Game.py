import pygame
import random
import time

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BROWN = (127,51,0)
pygame.init()
screen_width = 900
screen_height = 500
screen = pygame.display.set_mode([screen_width, screen_height])
pygame.display.set_caption('Shoot Game')
global loclist, listtogen, listtocheck, shot, score
score = 0
shot = False
listtocheck = []
listtogen = []
loclist = []
loclist.append((290,150))
loclist.append((415,150))
loclist.append((540,150))
loclist.append((290,300))
loclist.append((540,300))
loclist.append((190,300))
loclist.append((630,300))
loclist.append((500,0))

class dude():
    not_shootingGraphic = pygame.image.load("Sprites/1.png")
    shootingGraphic = pygame.image.load("Sprites/2.png")
    deadGraphic = pygame.image.load("Sprites/circlespam.png")
    shotGraphic = pygame.image.load("Sprites/3.png")
    def createGraphics(self):
        self.graphics.append(dude.not_shootingGraphic)
        self.graphics.append(dude.shootingGraphic)
        self.graphics.append(dude.deadGraphic)
        self.graphics.append(dude.shotGraphic)
    def __init__(self,loc):
        self.graphics = []
        self.createGraphics()
        self.loc = loc
        ret = quickmaths(3000,20)
        self.time = pygame.time.get_ticks() + ret
        self.removetime = 0
        self.currentgraphic = 0
        self.dead = False
        self.width = 75
        self.height = 90

    def drawself(self):
        global done, shot
        if pygame.time.get_ticks() > self.time + 1000 and not self.dead:
            self.currentgraphic = 3
            target = self.graphics[self.currentgraphic]
            target = pygame.transform.scale(target, (self.width, self.height))
            screen.blit(target, self.loc)
            goFont = pygame.font.SysFont(None, 72)
            text = goFont.render("Game Over", True, BLACK, BROWN)
            textRect = text.get_rect()
            screen.blit(text, textRect)
            shot = True

        elif pygame.time.get_ticks() > self.time and not self.dead:
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
        target = pygame.transform.scale(target,(self.width,self.height))
        screen.blit(target, self.loc)
    def getshoot(self,x,y):
        loc = self.loc
        top = loc[1]
        left = loc[0]
        right = left + self.width
        bottom = top + self.height
        if x > left and x < right and y > top and y < bottom:
            self.currentgraphic = self.graphics[2]
            return True
        return False
def configsprites():
    background = pygame.image.load("Sprites/background.png")
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
    global shot
    font = pygame.font.SysFont(None, 48)
    scoretxt = "Score: " + str(score)
    text = font.render(scoretxt, True, BLACK, BROWN)
    textRect = text.get_rect()
    textRect.centery = 100
    screen.blit(text, textRect)
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
    if shot == True:
        global done
        time.sleep(5)
        done = True

def quickmaths(num,min):
    sub = min * score
    toret = num - sub
    if toret < 0:
        toret = 0
    return toret

done = False
while not done:
    configsprites()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for guy in listtogen:
                if guy.getshoot(pos[0],pos[1]):
                    guy.dead = True
                    guy.removetime = pygame.time.get_ticks() + 1000
                    score += 1
                    pass

pygame.quit()