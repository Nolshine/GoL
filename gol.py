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
    for row in range(len(GRID)):
        for col in range(len(GRID[0])):
            updateCell(row,col)

def updateCell(row, col):
    #which neighbours do I have? am I a corner? an edge?
    leftEdge = (col == 0)
    rightEdge = (col == (len(GRID[row])-1))
    topEdge = (row == 0)
    bottomEdge = (row == (len(GRID)-1))
    #now I pick up on the rules of John Conway's GoL
    #am I alive?
    living = False
    if GRID[row][col] == 1:
        living = True
    #count my neighbours
    neighbours = 0
    for check_row in range(3):
        if check_row == 0 and topEdge:
            continue
        if check_row == 2 and bottomEdge:
            continue
        for check_col in range(3):
            if check_col == 0 and leftEdge:
                continue
            if check_col == 2 and rightEdge:
                continue
            checking_row = (row-1)+check_row
            checking_col = (col-1)+check_col
            if checking_row == row and checking_col == col:
                continue
            if GRID[checking_row][checking_col] == 1:
                neighbours += 1
    #determine which rules to use
    if living:
        #apply rules of live cells
        #1) Any live cell with fewer than two live neighbours dies,
        #   as if caused by under-population.
        if neighbours < 2:
            GRID[row][col] = 0
        #2) Any live cell with two or three live neighbours lives on
        #   to the next generation. (I don't need to check for this,
        #   as checking for the other living rules suffices.)
        #3) Any live cell with more than three live neighbours dies,
        #   as if by overcrowding.
        if neighbours > 3:
            GRID[row][col] = 0
    else:
        #apply rules of dead cells
        #4) Any dead cell with exactly three live neighbours becomes
        #   a live cell, as if by reproduction.
        if neighbours == 3:
            GRID[row][col] = 1

    
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
for row in range(32):
    GRID.append([])
    for col in range(32):
        GRID[row].append(randrange(2))

#START THE SIM
pygame.init()


SCREEN_SIZE = ((32*16),(32*16)) #size of window

screen = pygame.display.set_mode(SCREEN_SIZE, DOUBLEBUF)

clock = pygame.time.Clock()

while True:

    time_passed = clock.tick(50) #limits FPS to 50 and stores time.

    screen.fill((0,0,0)) #draw black background.

    if processEvents():
        break

    updateCells()

    renderGrid()
    pygame.display.update()


