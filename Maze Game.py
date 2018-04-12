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
pygame.display.set_caption('Maze Game')
walls = pygame.sprite.Group()
weals = pygame.sprite.Group()
woes = pygame.sprite.Group()
passable_blocks = pygame.sprite.Group()
impassable_blocks = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()
wealsneeded = 0

def extractFromFile(line,f,toInt = 1):
    file = open(f, "r")
    lines = file.readlines()
    export = line - 1
    num = lines[export]
    len = num.__len__()
    num = num[0:len - 1]
    if toInt == 1:
        num = int(num)
    file.close()
    return num

class Player(pygame.sprite.Sprite):
    global screen_height, screen_width
    wealPoints = 10
    woePoints = -100
    tiles = []
    maze = []
    debug = True
    blockWidth = 0
    blockHeight = 0

    def __init__(self, maze, color, width, height):
        super().__init__()
        self.maze = maze[0]
        self.tiles = maze[1]
        rows = len(self.maze[0])
        cols = len(self.maze)
        self.blockWidth = screen_width / cols
        self.blockHeight = screen_height / rows
        self.blockHeight = 20
        self.blockWidth = 20
        self.image = pygame.Surface([self.blockWidth, self.blockHeight])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self._col = 1
        self._row = 1
        self.weals = 0
        self.woes = 0
        self.moves = 0
        self.score = 0
        self.rect.x = self.blockWidth * 2
        self.rect.y = self.blockHeight
        self.movingDown = True

    def _move(self, dCol, dRow):
        self.moves += 1
        newCol = self._col + dCol
        newRow = self._row + dRow
        destination = self.maze[newCol][newRow]
        if not destination == self.tiles['wall']:
            self.rect.x += dCol * self.blockWidth
            self.rect.y += dRow * self.blockHeight
            self.maze[self._col][self._row] = self.tiles['blank']
            self._col = newCol
            self._row = newRow
            self.maze[self._col][self._row] = self.tiles['player']
            if destination == self.tiles['weal']:
                self.weals += 1
            if destination == self.tiles['woe']:
                self.woes += 1
                # self.sayMaze()

    def moveUp(self):
        self._move(0, -1)

    def moveDown(self):
        self._move(0, 1)

    def moveRight(self):
        self._move(1, 0)

    def moveLeft(self):
        self._move(-1, 0)

    def dSay(self, message):
        if self.debug:
            print(message)

    def calculateScore(self):
        score = self.wealPoints * self.weals + self.woePoints * self.woes - self.moves
        return score

    def basicAI(self):
        if not self.maze[self._col + 1][self._row] == self.tiles['wall']:
            self.moveRight()
            print("moving right")
        elif not self.maze[self._col][self._row + 1] == self.tiles['wall'] and self.movingDown:
            return self.moveDown()

        if self.maze[self._col][self._row + 1] == self.tiles['wall']:
            self.movingDown = False
        elif not self.maze[self._col][self._row - 1] == self.tiles['wall'] and not self.movingDown:
            return self.moveUp()
        elif self.maze[self._col][self._row - 1] == self.tiles['wall']:
            self.movingDown = True

    def sayMaze(self):
        rows = len(self.maze[0])
        cols = len(self.maze)

        for row in range(rows):
            newRow = []
            message = ''
            for col in range(cols):
                newRow.append(self.maze[col][row])
            for c in newRow:
                message += c
                message += ' '
            self.dSay(message)
        self.dSay("")


class Block(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()


def create_maze():
    tiles = {'wall': 'X',
             'weal': '+',
             'woe': '-',
             'blank': ' ',
             'player': 'P'}

    # maze config

    config = createRandomMapConfig()
    rows = config[0]
    cols = config[1]
    openSpaces = config[2]
    numWeals = config[3]
    numWoes = config[4]

    maze = createWalls(cols, rows, openSpaces, tiles)
    if not maze == 'invalid':
        maze = fillOtherCrap(numWeals, numWoes, maze, tiles)

    return maze, tiles


def createRandomMapConfig():
    rows = random.randint(15, 20)
    cols = random.randint(25, 30)
    openSpaces = random.randint(2, rows - 1)
    numWeals = int(abs(random.gauss(0, rows * cols * .1)))
    numWoes = int(abs(random.gauss(0, rows * cols * .1)))
    if numWoes > numWeals * 1.2:
        numWoes = numWeals * 1.2
    return rows, cols, openSpaces, numWeals, numWoes

def configtext():
    timer =  int(pygame.time.get_ticks() / 1000)
    seconds = timer % 60
    minutes = int(timer / 60)
    if seconds < 10:
        sdisplay = ":0" + str(seconds)
    else:
        sdisplay = ":" + str(seconds)
    timerdisplay = str(minutes) + sdisplay
    basicFont = pygame.font.SysFont(None, 48)

    text = basicFont.render(timerdisplay, True, BLACK, WHITE)
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx + 300
    textRect.centery = screen.get_rect().centery + 50
    screen.blit(text, textRect)
    pygame.display.update()


def createWalls(cols, rows, openSpaces, tiles):
    if openSpaces < rows:
        maze = []
        i = 2
        if cols % 2 == 0:
            i = 1
        for col in range(cols + i):
            maze.append([])
            for row in range(rows + 2):
                if row == 0:
                    maze[col].append(tiles['wall'])
                if row == rows + 1:
                    maze[col].append(tiles['wall'])
                else:
                    if col % 2 == 0:
                        maze[col].append(tiles['wall'])
                    else:
                        maze[col].append(tiles['blank'])
        for col in range(cols):

            if col % 2 == 0 and col > 0:
                openSpacesThisCol = openSpaces
                while openSpacesThisCol > 0:
                    r = random.randint(1, rows - 1)
                    if maze[col][r] == tiles['wall']:
                        openSpacesThisCol -= 1
                        maze[col][r] = tiles['blank']

    else:
        print("Unacceptable wall parameters")
        return "invalid"
    return maze


def fillOtherCrap(numWeals, numWoes, maze, tiles):
    rows = len(maze[0])
    cols = len(maze)
    m.wealprint = 0
    m.weals = numWeals
    m.woes = numWoes

    if (numWeals + numWoes) > .5 * rows * cols:
        print("Unacceptable maze parameters in fillOtherCrap")
        return 'invalid'
    while numWeals > 0:
        c, r = random.randint(0, cols - 1), random.randint(0, rows - 1)
        if maze[c][r] == tiles['blank']:
            maze[c][r] = tiles['weal']
            numWeals -= 1
    while numWoes > 0:
        c, r = random.randint(0, cols - 1), random.randint(0, rows - 1)
        if maze[c][r] == tiles['blank']:
            maze[c][r] = tiles['woe']
            numWoes -= 1
    return maze

class measurements:
    def __init__(self,bW,bH):
        self.blockWidth = bW
        self.blockHeight = bH
        self.weals = 0
        self.woes = 0
        self.wealprint = 0
        self.room = 0

m = measurements(0,0)
def showScore():
    basicFont = pygame.font.SysFont(None, 48)
    smallFont = pygame.font.SysFont(None, 30)
    scoretxt = "Score: " + str(score)
    text = basicFont.render(scoretxt, True, BLACK, WHITE)
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx + 300
    textRect.centery = screen.get_rect().centery - 170
    screen.blit(text, textRect)
    wealsneeded = int(m.weals * 85 / 100)
    if m.wealprint >= wealsneeded:
        makeNewMazeAndStuff()
    wealtxt = "Tiles: " + str(m.wealprint) + "/" + str(wealsneeded)
    text = basicFont.render(wealtxt, True, BLACK, WHITE)
    textRect.centerx = screen.get_rect().centerx + 300
    textRect.centery = screen.get_rect().centery - 120
    screen.blit(text, textRect)
    movesmax = int(wealsneeded * 6)
    if  movesmax < 250:
        movesmax = int(wealsneeded * 12)
        if movesmax > 250:
            movesmax = 250
        if movesmax < 60:
            movesmax = 60
    if player.moves > movesmax:
        player.moves = movesmax
    movetxt = "Moves: " + str(player.moves) + "/" + str(movesmax)
    text = smallFont.render(movetxt, True, BLACK, WHITE)
    textRect.centerx = screen.get_rect().centerx + 300
    textRect.centery = screen.get_rect().centery + 170
    screen.blit(text, textRect)
    roomtxt = "Room: " + str(m.room)
    text = basicFont.render(roomtxt, True, BLACK, WHITE)
    textRect.centerx = screen.get_rect().centerx + 300
    textRect.centery = screen.get_rect().centery - 70
    screen.blit(text, textRect)
    text = basicFont.render("Time Played", True, BLACK, WHITE)
    textRect.centerx = screen.get_rect().centerx + 300
    textRect.centery = screen.get_rect().centery
    screen.blit(text, textRect)
    configtext()
    if player.moves >= movesmax:
        gameover()
    else:
        pygame.display.update()

def createSpritesFromMazeList(player):
    maze = player.maze
    rows = len(maze[0])
    cols = len(maze)
    blockWidth = 20
    blockHeight = 20
    m.blockWidth = blockWidth
    m.blockHeight = blockHeight
    currentCol = 0

    for col in maze:
        currentCol += 1
        currentRow = -1
        for row in col:
            currentRow += 1
            # This represents a block
            if row == 'X':
                block = Block(BLACK, blockWidth, blockHeight)
                block.rect.x = currentCol * blockWidth
                block.rect.y = currentRow * blockHeight
                walls.add(block)
            if row == '+':
                block = Block(GREEN, blockWidth, blockHeight)
                block.rect.x = currentCol * blockWidth
                block.rect.y = currentRow * blockHeight
                weals.add(block)
            if row == '-':
                block = Block(RED, blockWidth, blockHeight)
                block.rect.x = currentCol * blockWidth
                block.rect.y = currentRow * blockHeight
                woes.add(block)

            all_sprites_list.add(block)

def makeNewMazeAndStuff():
    all_sprites_list.empty()
    walls.empty()
    weals.empty()
    woes.empty()
    passable_blocks.empty()
    impassable_blocks.empty()
    m.wealprint = 0
    global player
    global score
    try:
        if score == 0:
            pass
    except:
        score = 0
    maze = create_maze()
    score += (m.room * 1000)
    m.room += 1
    player = Player(maze, BLUE, m.blockWidth, m.blockHeight)
    player.maze[1][1] = 'P'
    player.moves = 0
    createSpritesFromMazeList(player)
    all_sprites_list.add(player)

def gameover():
    screen.fill(WHITE)
    goFont = pygame.font.SysFont(None, 72)
    goFontM = pygame.font.SysFont(None, 48)
    goFontS = pygame.font.SysFont(None, 30)
    text = goFont.render("GAME OVER", True, RED, WHITE)
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx - 25
    textRect.centery = screen.get_rect().centery
    screen.blit(text, textRect)
    text = goFontS.render("You ran out of moves!", True, RED, WHITE)
    textRect.centerx = screen.get_rect().centerx + 12
    textRect.centery = screen.get_rect().centery + 50
    screen.blit(text, textRect)
    highscore = extractFromFile(1,"MazeGameHighscore")
    if score > highscore:
        highscore = score
        hstxt = "New Highscore!"
    else:
        hstxt = "Highscore: " + str(highscore)
    file = open("MazeGameHighscore", "w")
    file.write(str(highscore))
    file.write("\n")
    file.write("N/A")
    file.close()
    stxt = "Your Score: " + str(score)
    text = goFontM.render(stxt, True, RED, WHITE)
    textRect.centerx = screen.get_rect().centerx
    textRect.centery = screen.get_rect().centery - 100
    screen.blit(text, textRect)
    text = goFontM.render(hstxt, True, RED, WHITE)
    textRect.centerx = screen.get_rect().centerx
    textRect.centery = screen.get_rect().centery - 50
    screen.blit(text, textRect)
    pygame.display.update()
    time.sleep(5)
    pygame.quit()

clock = pygame.time.Clock()


makeNewMazeAndStuff()
score = 0
done = False

# -------- Main Program Loop -----------
while not done:
    try:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    player.moveLeft()
                if event.key == pygame.K_d:
                    player.moveRight()
                if event.key == pygame.K_s:
                    player.moveDown()
                if event.key == pygame.K_w:
                     player.moveUp()
        screen.fill(WHITE)

        weal_hit_list = pygame.sprite.spritecollide(player, weals, True)
        woe_hit_list = pygame.sprite.spritecollide(player, woes, True)

        for weal in weal_hit_list:
            score += 200
            m.wealprint += 1

        for woe in woe_hit_list:
            score -= 100
            player.moves += 25

        if score < 0:
            score = 0
    except:
        pass

    try:
        all_sprites_list.draw(screen)
        showScore()

        pygame.display.flip()
    except:
        pass

pygame.quit()