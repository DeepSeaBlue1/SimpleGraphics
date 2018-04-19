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
pygame.display.set_caption('Reaction Game')
global score, timeleft
score = -1
timeleft = 3

def dostuff():
    screen.fill(WHITE)
    basicFont = pygame.font.SysFont(None, 500)
    smallFont = pygame.font.SysFont(None, 30)
    global letter
    txt = letter
    text = basicFont.render(txt, True, BLACK, WHITE)
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx
    textRect.centery = screen.get_rect().centery + 100
    screen.blit(text, textRect)
    txt = "Score: " + str(score)
    text = smallFont.render(txt, True, BLACK, WHITE)
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx
    textRect.centery = screen.get_rect().centery - 100
    screen.blit(text, textRect)
    configtext()
    pygame.display.update()

def getrdmletter():
    global score, timeleft
    score += 1
    timeleft += random.randint(0,1)
    global letter
    letter = extractFromFile(random.randint(1,26))


def extractFromFile(line,toInt = 0):
    file = open("Letters", "r")
    lines = file.readlines()
    export = line - 1
    num = lines[export]
    len = num.__len__()
    num = num[0:len - 1]
    if toInt == 1:
        num = int(num)
    file.close()
    return num

def checkletter(input):
    global letter
    if input == letter:
        getrdmletter()
    else:
        gameover()

def configtext():
    global timeleft
    timer =  timeleft - int(pygame.time.get_ticks() / 1000)
    if timer == 0:
        gameover()
    else:
        timerdisplay = "Time Left: " + str(timer)
        basicFont = pygame.font.SysFont(None, 30)
        txt = basicFont.render(timerdisplay, True, BLACK, WHITE)
        textRect = txt.get_rect()
        textRect.centerx = screen.get_rect().centerx
        textRect.centery = screen.get_rect().centery - 200
        screen.blit(txt, textRect)
        pygame.display.update()

def gameover():
    screen.fill(WHITE)
    basicFont = pygame.font.SysFont(None, 60)
    smallFont = pygame.font.SysFont(None, 30)
    txt = "Score: " + str(score)
    text = smallFont.render(txt, True, RED, WHITE)
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx
    textRect.centery = screen.get_rect().centery - 100
    screen.blit(text, textRect)
    txt = "Game Over!"
    text = basicFont.render(txt, True, RED, WHITE)
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx
    textRect.centery = screen.get_rect().centery
    screen.blit(text, textRect)
    pygame.display.update()
    time.sleep(5)
    pygame.quit()

getrdmletter()
done = False
while not done:
    try:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                key = "None"
                if event.key == pygame.K_a:
                    key = "A"
                if event.key == pygame.K_d:
                    key = "D"
                if event.key == pygame.K_s:
                    key = "S"
                if event.key == pygame.K_w:
                    key = "W"
                if event.key == pygame.K_q:
                    key = "Q"
                if event.key == pygame.K_e:
                    key = "E"
                if event.key == pygame.K_r:
                    key = "R"
                if event.key == pygame.K_t:
                    key = "T"
                if event.key == pygame.K_y:
                    key = "Y"
                if event.key == pygame.K_u:
                    key = "U"
                if event.key == pygame.K_i:
                    key = "I"
                if event.key == pygame.K_o:
                    key = "O"
                if event.key == pygame.K_p:
                    key = "P"
                if event.key == pygame.K_g:
                    key = "G"
                if event.key == pygame.K_f:
                    key = "F"
                if event.key == pygame.K_h:
                    key = "H"
                if event.key == pygame.K_j:
                    key = "J"
                if event.key == pygame.K_k:
                    key = "K"
                if event.key == pygame.K_l:
                    key = "L"
                if event.key == pygame.K_z:
                    key = "Z"
                if event.key == pygame.K_x:
                    key = "X"
                if event.key == pygame.K_c:
                    key = "C"
                if event.key == pygame.K_v:
                    key = "V"
                if event.key == pygame.K_b:
                    key = "B"
                if event.key == pygame.K_n:
                    key = "N"
                if event.key == pygame.K_m:
                    key = "M"
                checkletter(key)
        dostuff()
    except:
        pass


pygame.quit()