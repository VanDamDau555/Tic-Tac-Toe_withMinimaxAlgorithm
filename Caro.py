import pygame as pg
import random
import sys
import cv2
import PIL.Image
import math

pg.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)                 #De tich hop sound tot hon cho pygame
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
#The sound are used
hit_sound = pg.mixer.Sound('D:\Anaconda\python1\FlappyBird\Sound_FB\FB_sfx_hit.wav')
clock = pg.time.Clock()  
font_Game = pg.font.SysFont('Time new roman', 40, bold=True)

blockSize = 156
grid = ["-", "-", "-", "-", "-", "-", "-", "-", "-"]
#Set up score for minimax algorithm
scores = {'X':-10, 
          'O':10, 
          'T':0    }
currentPlayer = 'X'
winner = None
active = True
gameRunning = True

#Demo without pygame
def display(a):
    for i in range(0, len(a), 3):
        print(a[i],'|', a[i+1],'|', a[i+2])
        print("------------")
        
    
def checkTie(a):
    global active
    global winner
    if "-" not in a and winner == None:
        winner = 'T'
        active = False    
        #print("Tie")       Delete when use pygame to don't check Terminal
        return True
    return False
        
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

#Can use for case have pygame    
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
    global active
    if(checkAll(a)):
        #print("The winner is "+winner)         Delete when use pygame to don't check Terminal
        active = False
        return True
    return False

def checkWinFuture():
    #Vertical
    count = 0
    winFuture = None
    for i in range(0, 3):
        if grid[i*3] == grid[i*3+1] == grid[i*3+2] and grid[i*3]!="-":
            winFuture = grid[i*3]
    
    #Horizon
    for i in range(0, 3):
        if grid[i] == grid[i+3] == grid[i+6] and grid[i]!="-":
            winFuture = grid[i]
    
    #Diagonal
    if grid[0] == grid[4] == grid[8] and grid[0] != "-":
        winFuture = grid[0]
    
    if grid[2] == grid[4] == grid[6] and grid[2] != "-":
        winFuture = grid[6]

    for i in range(0, 9):
        if grid[i] == "-":
            count = count+1

    if winFuture == None and count == 0:
        return 'T'
    else:
        return winFuture
#Try code with have Pygame
def display2():
    for i in range(0, screen_width, blockSize):
        for j in range(0, screen_height, blockSize):    
            rect = pg.Rect(i, j, blockSize, blockSize)
            pg.draw.rect(screen, (0, 0, 0), rect, 1)
    
def Player2(posX, posY):
    while currentPlayer == 'X':        
        grid[(posX//blockSize)+((posY//blockSize)*3)] = currentPlayer
        for i in range (0, screen_width, blockSize):
            for j in range (0, screen_height, blockSize):
                if (posX > i) and (posX < i + blockSize) and (posY > j) and (posY < j + blockSize):
                    # +2 to don't overprint with grid in display2 
                    screen.blit(player_img, (i+2, j+2))
                    hit_sound.play()
                    switchPlayer()
                

def Bot2():
    while currentPlayer == 'O':
        botPos = random.randint(0, 8)
        posY = botPos // (len(grid)/3)
        posX = botPos - posY*3
        #Print when i check error with position of Bot
        #print(posX, posY)
        if(grid[botPos] == "-" and grid[botPos]!="X"):
            grid[botPos] = currentPlayer
            print(botPos)
            # +2 to don't overprint with grid in display2
            screen.blit(bot_img, (posX*blockSize+2, posY*blockSize+2))
            switchPlayer()


def Bot3_with_Minimax():
    while currentPlayer == 'O' and active:
        bestScore = -100 
        pos = 0       
        for i in range(0, len(grid)):
            if grid[i] == "-":
                grid[i] = currentPlayer                
                score = Minimax(grid, 0, False)
                grid[i] = "-"                
                if(score > bestScore):
                    bestScore = score
                    pos = i
                print(bestScore, i)    
        grid[pos] = 'O'
        posY = pos // (len(grid)/3)
        posX = pos - posY*3
        print(pos)
        screen.blit(bot_img, (posX*blockSize+2, posY*blockSize+2))
        switchPlayer()



def Minimax(grid, depth, isMinimax):
    result = checkWinFuture()
    #result2 = tie    
    if result != None:
        return scores[result]

    if isMinimax:
        bestScore = -100
        for i in range(0, len(grid)):
            if grid[i] == "-":
                grid[i] = 'O'
                score = Minimax(grid, depth+1, False)
                grid[i] = "-"
                bestScore = max(score, bestScore)
        return bestScore
    elif isMinimax == False:        
        bestScore = 100
        for i in range(0, len(grid)):
            if (grid[i] == "-"):
                grid[i] = 'X'
                score = Minimax(grid, depth+1, True)
                grid[i] = "-"
                bestScore = min(score, bestScore)
        
        return bestScore
  


def EndGame(gameRun):
    if gameRun == False:
        #Retry always display at any case
        myFont = pg.font.SysFont('Comic Sans MS', 32)
        retry_display = myFont.render("Click R to retry the game",True, (100, 174, 48))
        retry_rect = retry_display.get_rect(center = (screen_width/2, screen_height/2))
        screen.blit(retry_display, retry_rect)
    #Case Tie    
    if checkTie(grid) == True and gameRun == False:     
        tie_display = font_Game.render(winner, True, (0, 255, 0))
        tie_rect = tie_display.get_rect(center = (screen_width/2, 120))
        screen.blit(tie_display, tie_rect)
    #Case have win
    elif checkWin(grid) == True and gameRun == False:    
        winner_display = font_Game.render("The winner is "+winner, True, (0, 255, 0))
        winner_rect = winner_display.get_rect(center = (screen_width/2, 120))
        screen.blit(winner_display, winner_rect)
    else:
        display2()

while gameRunning:
    if winner==None and active == True:
        #print(Minimax(grid, 0, True))
        EndGame(gameRun=True)
        
        Bot3_with_Minimax()
        #display(grid)
        # Player(grid)
        checkWin(grid)
        checkTie(grid)
        # switchPlayer()
        # Bot(grid)
        # checkWin(grid)
        # checkTie(grid)

    elif active == False:
        EndGame(gameRun=False)

    for event in pg.event.get():
        (x, y) = pg.mouse.get_pos()
        #print(x, y)
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

        if event.type == pg.MOUSEBUTTONDOWN and active == True:
            if(grid[(x//blockSize)+((y//blockSize)*3)] == "-" and grid[(x//blockSize)+((y//blockSize)*3)]!="O"):
                Player2(x, y)
        
        #Use R to retry
        if event.type == pg.KEYDOWN:    
            if event.key == pg.K_r and active == False:
                screen.fill((255, 255, 255))
                winner = None
                grid = ["-", "-", "-", "-", "-", "-", "-", "-", "-"]
                active = True
                display2()
                #print(1)
    pg.display.update()
    #FPS = 90
    FPS = 10
    clock.tick(FPS)
    
