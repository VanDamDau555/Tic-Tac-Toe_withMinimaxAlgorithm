import pygame as pg
import random
import sys
import cv2
import PIL.Image

#pg.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)                 #De tich hop sound tot hon cho pygame
pg.init()
#Set screen frame
screen_width = 468
screen_height = 468
screen = pg.display.set_mode((screen_width, screen_height))
screen.fill((255, 255, 255))
pg.display.set_caption("Caro")

#The image are used for when you play
player_img = pg.image.load('D:\Anaconda\python1\CaroChess\X_turn.png')
bot_img = pg.image.load('D:\Anaconda\python1\CaroChess\O_turn.png')

clock = pg.time.Clock()  
font_Game = pg.font.SysFont('Time new roman', 40, bold=True)

blockSize = 156
grid = ["-", "-", "-", "-", "-", "-", "-", "-", "-"]
currentPlayer = 'X'
winner = None
gameRunning = True

#Demo without pygame
def display(a):
    for i in range(0, len(a), 3):
        print(a[i],'|', a[i+1],'|', a[i+2])
        print("------------")
    
def checkTie(a):
    global gameRunning
    if "-" not in a and winner == None:
        gameRunning = False    
        print("Tie")
        
def Player(a):
    Pchoose = int(input("Choose your cell - from 0 - 8: "))
    if(Pchoose >=0 and Pchoose <=8 and a[Pchoose] == '-' and a[Pchoose] != 'O'):
        a[Pchoose] = currentPlayer
        display(a)
    else:
        print("This cell has a already symbol")

def Bot(a):
    while currentPlayer == 'O':
        botPos = random.randint(0, 8)
        if(a[botPos] == "-" and a[botPos]!="X"):
            a[botPos] = currentPlayer
            display(a)
            switchPlayer()
    
def switchPlayer():
    global currentPlayer
    if currentPlayer == 'X':
        currentPlayer = 'O'
    else:
        currentPlayer = 'X'

def checkLine(a, x1, x2, x3):
    global winner
    if a[x1] == a[x2] == a[x3] and a[x1] != '-':
        winner = a[x1]
        return True    
    return False

def checkAll(a):
    #Dòng
    if (checkLine(a, 0, 1, 2) == True) or (checkLine(a, 3, 4, 5) == True) or (checkLine(a, 6, 7, 8) == True):
        return True
    #Cột
    if (checkLine(a, 0, 3, 6) == True) or (checkLine(a, 1, 4, 7) == True) or (checkLine(a, 2, 5, 8) == True):
        return True
    #Đường chéo
    if (checkLine(a, 0, 4, 8) == True) or (checkLine(a, 2, 4, 6) == True):
        return True
    return False

def checkWin(a):
    global gameRunning
    if(checkAll(a)):
        print("The winner is "+winner)
        gameRunning = False
#Try code with have Pygame
def display2():
    for i in range(0, screen_width, blockSize):
        for j in range(0, screen_height, blockSize):    
            rect = pg.Rect(i, j, blockSize, blockSize)
            pg.draw.rect(screen, (0, 0, 0), rect, 1)
    
def Player2(posX, posY):
    for i in range (0, screen_width, blockSize):
        for j in range (0, screen_height, blockSize):
            if (posX > i) and (posX < i + blockSize) and (posY > j) and (posY < j + blockSize):
                screen.blit(player_img, (i, j))
                break

def Bot2(posX, posY):
    for i in range (0, screen_width, blockSize):
        for j in range (0, screen_height, blockSize):
            if (posX > i) and (posX < i + blockSize) and (posY > j) and (posY < j + blockSize):
                screen.blit(bot_img, (i, j))
                break

while gameRunning:
    display2()
    Player(grid)
    checkWin(grid)
    checkTie(grid)
    switchPlayer()
    Bot(grid)
    checkWin(grid)
    checkTie(grid)
    for event in pg.event.get():
        (x, y) = pg.mouse.get_pos()
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

        if event.type == pg.MOUSEBUTTONDOWN:
            Player2(x, y)


    pg.display.update()
    #FPS = 90
    FPS = 45
    clock.tick(FPS)
    
