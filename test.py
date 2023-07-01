import pygame as pg
import random
import sys
import cv2
import PIL.Image
import PIL.ImageTk

pg.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)                 #De tich hop sound tot hon cho pygame
pg.init()
#Set khung hinh
screen_width = 432
screen_height = 768
screen = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption("Test")
blockSize = 156
def grid():
    for i in range(0, screen_width, blockSize):
        for j in range(0, screen_height, blockSize):    
            rect = pg.Rect(i, j, blockSize, blockSize)
            pg.draw.rect(screen, (100,100,100), rect, 1)
while True:
    grid()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
    pg.display.update()