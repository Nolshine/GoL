"""
Simulating John Conway's Game of Life

Step 1) Display a grid. I had neglected to remember until now
that to display a grid you need to display borders. But I've already
thought of a possible solution.
    1a) First, you workout if the cell is  living or dead.
    1b) then you draw a filled square that's white if the cell's dead,
        or black if it's living.
    1c) then you draw a square smaller by 2px*2px that's filled with
        the opposite color to the one you drew before, smack in the
        centre of the other square.

(But of course, first we must make a screen appear, make it fit the grid)


Let's think about the grid. I want to get to the stage where I'm
simulating rules fairly quickly, and I think I want to do it on... hm
i guess a fairly small, finite and bound space. I don't have a choice
regarding bound, I don't know how to make things scroll or w/e.
Finite because I do not yet want to warp stuff, although I will after I'm done
reaching the first GoL.

A 16*16 cells grid will do for now, and i need to fit them in a window,
so I'll make them 16px*16px big. Of course the sqares themselves will
only be 14*14 but i need to include the border.

GOAL: get a screen up. *done*
GOAL: render tilegrid. Shouldn't be too difficult, as I am
      separating rendering from processing.
"""

import pygame
from pygame.locals import *

from random import randrange


def processEvents():
    for event in pygame.event.get():
        cond1 = (event.type == QUIT)
        cond2 = ((event.type == KEYDOWN) and (event.key == K_ESCAPE))
        if cond1 or cond2:
            pygame.quit()
            print "This is too much. I quit!"
            return True
        if event.type == MOUSEBUTTONDOWN:
            pressed = pygame.mouse.get_pressed()
            if pressed[0] == 1:
                pos = pygame.mouse.get_pos()
                col = pos[0]/16
                row = pos[1]/16
                if GRID[row][col] == 0:
                    GRID[row][col] = 1
                else:
                    GRID[row][col] = 0
                
    return False

def updateCells():
    print "update cells."

def renderGrid():
    #let's see if I can access GRID from here.
    for row in range(len(GRID)):
        for col in range(len(GRID[0])):
            renderTile(row,col)

def renderTile(row,col):
    tile = pygame.Rect((col*16),(row*16),16,16)
    inner = pygame.Rect(((col*16)+1), ((row*16)+1), 14, 14)
    if GRID[row][col] == 1:
        pygame.draw.rect(screen, (0,0,0), tile)
        pygame.draw.rect(screen, (255,255,255), inner)
    else:
        pygame.draw.rect(screen, (255,255,255), tile)
        pygame.draw.rect(screen, (0,0,0), inner)

GRID = []
for row in range(16):
    GRID.append([])
    for col in range(16):
        GRID[row].append(randrange(2))

#START THE SIM
pygame.init()

SCREEN_SIZE = ((16*16),(16*16)) #size of window
SPEED = 100 #speed, in ms, of simulation

screen = pygame.display.set_mode(SCREEN_SIZE, DOUBLEBUF)

clock = pygame.time.Clock()

update_timer = 0

while True:

    time_passed = clock.tick(50) #limits FPS to 50 and stores time.
    update_timer += time_passed

    screen.fill((0,0,0)) #draw black background.

    if processEvents():
        break

    if update_timer >= SPEED:
        update_timer = 0
        updateCells()

    renderGrid()
    pygame.display.update()


