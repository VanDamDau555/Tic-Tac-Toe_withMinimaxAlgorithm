import pygame as pg
import random
import sys
import cv2
import numpy as np
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
blockSize = 156
blockSize2 = 46
#grid = ["-", "-", "-", "-", "-", "-", "-", "-", "-"]
grid2 = []

#The image are used for when you play
player_img = pg.image.load('D:\Anaconda\CODE\Main_Python\CaroChess\X_turn.png')             #Design for Tik tac toe
player_img2 = pg.transform.scale(player_img, (blockSize2-2, blockSize2-2))                                      #Transform for caro
bot_img = pg.image.load('D:\Anaconda\CODE\Main_Python\CaroChess\O_turn.png')                #Similar
bot_img2 = pg.transform.scale(bot_img, (blockSize2-2, blockSize2-2))                           #Similar
#The sound are used
hit_sound = pg.mixer.Sound('D:\Anaconda\CODE\Main_Python\FB_Bird\Sound_FB\FB_sfx_hit.wav')
clock = pg.time.Clock()  
font_Game = pg.font.SysFont('Time new roman', 40, bold=True)


for i in range(0, int(screen_width/blockSize2)):
    block=[]
    for j in range(0, int(screen_height/blockSize2)):
        block.append("-")
    grid2.append(block)
grid2 = np.array(grid2)
#Set up score for minimax algorithm
scores = {'X':-10, 
          'O':10, 
          'T':0    }
currentPlayer = 'X'
winner = None
active = True
gameRunning = True
# def __init__(height, width, blockSize):
#     pass

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

#Condition Win for Tik Tac Toe
# def checkLine(a, x1, x2, x3):
#     global winner
#     if a[x1] == a[x2] == a[x3] and a[x1] != '-':
#         winner = a[x1]
#         return True    
#     return False

# def checkAll(a):
#     #Dòng
#     if (checkLine(a, 0, 1, 2) == True) or (checkLine(a, 3, 4, 5) == True) or (checkLine(a, 6, 7, 8) == True):
#         return True
#     #Cột
#     if (checkLine(a, 0, 3, 6) == True) or (checkLine(a, 1, 4, 7) == True) or (checkLine(a, 2, 5, 8) == True):
#         return True
#     #Đường chéo
#     if (checkLine(a, 0, 4, 8) == True) or (checkLine(a, 2, 4, 6) == True):
#         return True
#     return False

# def checkWin(a):
#     global active
#     if(checkAll(a)):
#         #print("The winner is "+winner)         Delete when use pygame to don't check Terminal
#         active = False
#         return True
#     return False

# def checkWinFuture():
#     #Vertical
#     count = 0
#     winFuture = None
#     for i in range(0, 3):
#         if grid[i*3] == grid[i*3+1] == grid[i*3+2] and grid[i*3]!="-":
#             winFuture = grid[i*3]
    
#     #Horizon
#     for i in range(0, 3):
#         if grid[i] == grid[i+3] == grid[i+6] and grid[i]!="-":
#             winFuture = grid[i]
    
#     #Diagonal
#     if grid[0] == grid[4] == grid[8] and grid[0] != "-":
#         winFuture = grid[0]
    
#     if grid[2] == grid[4] == grid[6] and grid[2] != "-":
#         winFuture = grid[6]

#     for i in range(0, 9):
#         if grid[i] == "-":
#             count = count+1

#     if winFuture == None and count == 0:
#         return 'T'
#     else:
#         return winFuture
    
#Condition Win with Caro
def checkLine2(a, coord1, coord2, coord3, coord4, coord5):
    #Give 5 coord for check
    global winner
    if a[coord1[0]][coord1[1]] == a[coord2[0]][coord2[1]] == a[coord3[0]][coord3[1]] == a[coord4[0]][coord4[1]] == a[coord5[0]][coord5[1]]  and a[coord1[0]][coord1[1]] != '-':
        winner = a[coord1[0]][coord1[1]]
        return True    
    return False

def checkAll2(a):
    #Cột
    for i in range(0, a.shape[0]-4):
        for j in range(0, a.shape[1]):            
            if (checkLine2(a, (i, j), (i+1, j), (i+2, j), (i+3, j), (i+4, j)) == True):
                return True
    #Dòng
    for i in range(0, a.shape[0]):
        for j in range(0, a.shape[1]-4):            
            if (checkLine2(a, (i, j), (i, j+1), (i, j+2), (i, j+3), (i, j+4)) == True):
                return True
    #Đường chéo
    for i in range(0, a.shape[0]-4):
        for j in range(0, a.shape[1]-4):            
            if (checkLine2(a, (i, j), (i+1, j+1), (i+2, j+2), (i+3, j+3), (i+4, j+4)) == True):
                return True
    for i in range(0+4, a.shape[0]):
        for j in range(0, a.shape[1]-4):            
            if (checkLine2(a, (i, j), (i-1, j+1), (i-2, j+2), (i-3, j+3), (i-4, j+4)) == True):
                return True
    return False

def checkWin2(a):
    global active
    if(checkAll2(a) == True):
        #print("The winner is "+winner)         Delete when use pygame to don't check Terminal
        active = False
        return True
    return False

#Try code with have Pygame
# def display2():
    for i in range(0, screen_width, blockSize):
        for j in range(0, screen_height, blockSize):    
            rect = pg.Rect(i, j, blockSize, blockSize)
            pg.draw.rect(screen, (0, 0, 0), rect, 1)

#Update to new screen
def display3():
    numberBlock = screen_height/blockSize2
    for i in range(0, int(numberBlock)):
        for j in range(0, int(numberBlock)):
            rect = pg.Rect(i*blockSize2, j*blockSize2, blockSize2, blockSize2)
            pg.draw.rect(screen, (0, 0, 0), rect, 1)
    # print(numberBlock)

# def Player2(posX, posY):
#     while currentPlayer == 'X':        
#         grid[(posX//blockSize)+((posY//blockSize)*3)] = currentPlayer
#         for i in range (0, screen_width, blockSize):
#             for j in range (0, screen_height, blockSize):
#                 if (posX > i) and (posX < i + blockSize) and (posY > j) and (posY < j + blockSize):
#                     # +2 to don't overprint with grid in display2 
#                     screen.blit(player_img, (i+2, j+2))
#                     #hit_sound.play()
#                     switchPlayer()

#Try with new blockSize
def Player3(posX, posY):
    while currentPlayer == 'X':        
        grid2[int(posY/blockSize2)][int(posX/blockSize2)] = currentPlayer
        for i in range (0, screen_width, blockSize2):
            for j in range (0, screen_height, blockSize2):
                if (posX > i) and (posX < i + blockSize2) and (posY > j) and (posY < j + blockSize2):    
                    screen.blit(player_img2, (i+2, j+2))
                    #hit_sound.play()
                    switchPlayer()          
    checkWin2(grid2)

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


# def Bot3_with_Minimax():
#     while currentPlayer == 'O' and active:
#         bestScore = -100 
#         pos = 0       
#         for i in range(0, len(grid)):
#             if grid[i] == "-":
#                 grid[i] = currentPlayer                
#                 score = Minimax(grid, 0, False)
#                 grid[i] = "-"                
#                 if(score > bestScore):
#                     bestScore = score
#                     pos = i
#                 #print(bestScore, i)    
#         grid[pos] = 'O'
#         posY = pos // (len(grid)/3)
#         posX = pos - posY*3
#         #print(pos)
#         screen.blit(bot_img, (posX*blockSize+2, posY*blockSize+2))
#         checkWin2(grid2)
#         switchPlayer()
#     checkWin(grid)

#Try with new blockSize
def Bot3_with_Minimax2():
    while currentPlayer == 'O' and active:
        bestScore = float('-inf') 
        pos = (0, 0)  
        for i in range(0, grid2.shape[0]):
            for j in range(0, grid2.shape[1]):
                if grid2[i][j] == "-":
                    grid2[i][j] = currentPlayer                
                    score = Minimax2(grid2, 0, False)
                    #print(score)
                    grid2[i][j] = "-"                
                    if(score > bestScore):
                        bestScore = score
                        pos = (i, j)
                    print(score, (i, j))   
        grid2[pos[0]][pos[1]] = 'O'
        print(pos)
        screen.blit(bot_img2, (pos[1]*blockSize2+2, pos[0]*blockSize2+2))
        switchPlayer()
    checkWin2(grid2)

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
                score = Minimax(grid, depth-1, False)
                grid[i] = "-"
                bestScore = max(score, bestScore)
                #alpha_beta is added
                if bestScore>score:
                    break
        return bestScore
    elif isMinimax == False:        
        bestScore = 100
        for i in range(0, len(grid)):
            if (grid[i] == "-"):
                grid[i] = 'X'
                score = Minimax(grid, depth-1, True)
                grid[i] = "-"
                bestScore = min(score, bestScore)
                if bestScore>=score:
                    break
        return bestScore


def evaluate(a):
    score = 0
    #Check rows for 3, 4, 5
    for i in range(0, a.shape[0]):
        for j in range(0, a.shape[1]-4):
            pt_row = a[i, j:j+4]
            if np.all(pt_row == 'X'): score += -1200000
            if np.all(pt_row == 'O'): score += 1000000
            if np.sum(pt_row == 'X') == 4:
                if np.sum(pt_row == '-') == 1: score += -120000
                else: score += -12000
            if np.sum(pt_row == 'O') == 4:
                if np.sum(pt_row == '-') == 1: score += 100000
                else: score += 10000
            if np.sum(pt_row == 'X') == 3:
                if np.sum(pt_row == '-') == 2: score += -12000
                elif np.sum(pt_row == '-') == 1: score += -1200
                else: score += -120
            if np.sum(pt_row == 'O') == 3:
                if np.sum(pt_row == '-') == 2: score += 10000
                elif np.sum(pt_row == '-') == 1: score += 1000
                else: score += 100
            if np.sum(pt_row == 'X') == 2:
                if np.sum(pt_row == '-') == 3: score += -1200
                elif np.sum(pt_row == '-') == 2: score += -120
                else: score += -12
            if np.sum(pt_row == 'O') == 2:
                if np.sum(pt_row == '-') == 3: score += 1000
                elif np.sum(pt_row == '-') == 2: score += 100
                else: score += 10
            if np.sum(pt_row == 'X') == 1:
                if np.sum(pt_row == '-') == 4: score += -12
                else: score += -2
            if np.sum(pt_row == 'O') == 1:
                if np.sum(pt_row == '-') == 4: score += 10
                else: score += 1

    #Check column for 3, 4, 5
    for i in range(0, a.shape[0]-4):
        for j in range(0, a.shape[1]):
            pt_col = a[i:i+4, j]
            if np.all(pt_col == 'X'): score += -1200000
            if np.all(pt_col == 'O'): score += 1000000
            if np.sum(pt_col == 'X') == 4:
                if np.sum(pt_col == '-') == 1: score += -120000
                else: score += -12000
            if np.sum(pt_col == 'O') == 4:
                if np.sum(pt_col == '-') == 1: score += 100000
                else: score += 10000
            if np.sum(pt_col == 'X') == 3:
                if np.sum(pt_col == '-') == 2: score += -12000
                elif np.sum(pt_col == '-') == 1: score += -1200
                else: score += -120
            if np.sum(pt_col == 'O') == 3:
                if np.sum(pt_col == '-') == 2: score += 1000
                elif np.sum(pt_col == '-') == 1: score += 100
                else: score += 100
            if np.sum(pt_col == 'X') == 2:
                if np.sum(pt_col == '-') == 3: score += -1200
                elif np.sum(pt_col == '-') == 2: score += -120
                else: score += -12
            if np.sum(pt_col == 'O') == 2:
                if np.sum(pt_col == '-') == 3: score += 1000
                elif np.sum(pt_col == '-') == 2: score += 100
                else: score += 10
            if np.sum(pt_col == 'X') == 1:
                if np.sum(pt_col == '-') == 4: score += -12
                else: score += -2
            if np.sum(pt_col == 'O') == 1:
                if np.sum(pt_col == '-') == 4: score += 10
                else: score += 1

    #Check diagonal for 3, 4, 5
    for i in range(0, a.shape[0]-4):
        for j in range(0, a.shape[1]-4):
            pt_dia1 = np.diag(a[i:i+4, j:j+4])
            if np.all(pt_dia1 == 'X'): score += -1200000
            if np.all(pt_dia1 == 'O'): score += 1000000
            if np.sum(pt_dia1 == 'X') == 4:
                if np.sum(pt_dia1 == '-') == 1: score += -120000
                else: score += -12000
            if np.sum(pt_dia1 == 'O') == 4:
                if np.sum(pt_dia1 == '-') == 1: score += 100000
                else: score += 10000
            if np.sum(pt_dia1 == 'X') == 3:
                if np.sum(pt_dia1 == '-') == 2: score += -12000
                elif np.sum(pt_dia1 == '-') == 1: score += -1200
                else: score += -120
            if np.sum(pt_dia1 == 'O') == 3:
                if np.sum(pt_dia1 == '-') == 2: score += 10000
                elif np.sum(pt_dia1 == '-') == 2: score += 1000
                else: score += 100
            if np.sum(pt_dia1 == 'X') == 2:
                if np.sum(pt_dia1 == '-') == 3: score += -1200
                elif np.sum(pt_dia1 == '-') == 2: score += -120
                else: score += -12
            if np.sum(pt_dia1 == 'O') == 2:
                if np.sum(pt_dia1 == '-') == 3: score += 1000
                elif np.sum(pt_dia1 == '-') == 2: score += 100
                else: score += 10
            if np.sum(pt_dia1 == 'X') == 1:
                if np.sum(pt_dia1 == '-') == 4: score += -12
                else: score += -2
            if np.sum(pt_dia1 == 'O') == 1:
                if np.sum(pt_dia1 == '-') == 4: score += 10
                else: score += 1

    for i in range(4, a.shape[0]):
        for j in range(0, a.shape[1]-4):
            pt_dia2 = np.diag(a[i:i-4, j:j+4])
            if np.all(pt_dia2 == 'X'): score += -1200000
            if np.all(pt_dia2 == 'O'): score += 1000000
            if np.sum(pt_dia2 == 'X') == 4:
                if np.sum(pt_dia2 == '-') == 1: score += -120000
                else: score += -12000
            if np.sum(pt_dia2 == 'O') == 4:
                if np.sum(pt_dia2 == '-') == 1: score += 100000
                else: score += 10000
            if np.sum(pt_dia2 == 'X') == 3:
                if np.sum(pt_dia2 == '-') == 2: score += -12000
                elif np.sum(pt_dia2 == '-') == 1: score += -1200
                else: score += -120
            if np.sum(pt_dia2 == 'O') == 3:
                if np.sum(pt_dia2 == '-') == 2: score += 10000
                elif np.sum(pt_dia2 == '-') == 1: score += 1000
                else: score += 100
            if np.sum(pt_dia2 == 'X') == 2:
                if np.sum(pt_dia2 == '-') == 3: score += -1200
                elif np.sum(pt_dia2 == '-') == 2: score += -120
                else: score += -12
            if np.sum(pt_dia2 == 'O') == 2:
                if np.sum(pt_dia2 == '-') == 3: score += 1000
                elif np.sum(pt_dia2 == '-') == 2: score += 100
                else: score += 10
            if np.sum(pt_dia2 == 'X') == 1:
                if np.sum(pt_dia2 == '-') == 4: score += -12
                else: score += -2
            if np.sum(pt_dia2 == 'O') == 1:
                if np.sum(pt_dia2 == '-') == 4: score += 10
                else: score += 1

    return score
#New minimax algorithm for Caro (2D)
def Minimax2(a, depth, isMinimax):
    score = evaluate(a)
    #result2 = tie    
    if depth == 4 or score!= None:
        return score
    
    if isMinimax:
        bestScore = float('-inf')
        for i in range(0, a.shape[0]):
            for j in range(0, a.shape[1]):
                if a[i][j] == "-":
                    a[i][j] = 'O'
                    score = Minimax2(a, depth+1, False)
                    a[i][j] = "-"
                    bestScore = max(score, bestScore)
                    #alpha_beta is added
                    if bestScore>=score:
                        break
        return bestScore
    elif isMinimax == False:        
        bestScore = float('inf')
        for i in range(0, a.shape[0]):
            for j in range(0, a.shape[1]):
                if (a[i][j] == "-"):
                    a[i][j] = 'X'
                    score = Minimax2(a, depth+1, True)
                    a[i][j] = "-"
                    bestScore = min(score, bestScore)
                    if bestScore>=score:
                        break
        return bestScore    

def EndGame(gameRun):
    if gameRun == False:
        #Retry always display at any case
        myFont = pg.font.SysFont('Comic Sans MS', 32)
        retry_display = myFont.render("Click R to retry the game",True, (100, 174, 48))
        retry_rect = retry_display.get_rect(center = (screen_width/2, screen_height/2))
        screen.blit(retry_display, retry_rect)
    #Case Tie    
    if checkTie(grid2) == True and gameRun == False:     
        tie_display = font_Game.render("Don't any player win!", True, (0, 255, 0))
        tie_rect = tie_display.get_rect(center = (screen_width/2, 120))
        screen.blit(tie_display, tie_rect)
    #Case have win
    elif checkWin2(grid2) == True and gameRun == False:    
        winner_display = font_Game.render("The winner is "+winner+"!", True, (122, 74, 48))
        winner_rect = winner_display.get_rect(center = (screen_width/2, 120))
        screen.blit(winner_display, winner_rect)
    else:
        display3()

while gameRunning:
    display3()
    for event in pg.event.get():
        (x, y) = pg.mouse.get_pos()
        #print(x, y)
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

        if event.type == pg.MOUSEBUTTONDOWN and active == True:
            if(grid2[y//blockSize2][x//blockSize2] == "-" and grid2[y//blockSize2][x//blockSize2]!="O"):
                #Player2(x, y)
                Player3(x,y)
                #print(grid2)
        
        #Use R to retry
        if event.type == pg.KEYDOWN:    
            if event.key == pg.K_r:
                screen.fill((255, 255, 255))
                winner = None
                #grid = ["-", "-", "-", "-", "-", "-", "-", "-", "-"]
                grid2 = []
                for i in range(0, int(screen_width/blockSize2)):
                    block=[]
                    for j in range(0, int(screen_height/blockSize2)):
                        block.append("-")
                    grid2.append(block)
                grid2 = np.array(grid2)
                active = True
                display3()
                currentPlayer = 'X'
                #print(1)
    if active == False:
        EndGame(gameRun=False)

    if winner==None and active == True:
        EndGame(gameRun=True)
        
        Bot3_with_Minimax2()
        #display(grid)
        # Player(grid)
        
        #print(grid2)

    pg.display.update()
    FPS = 90
    #FPS = 60
    clock.tick(FPS)
    
