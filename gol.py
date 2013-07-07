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

GOAL: get a screen up.
"""

import pygame
from pygame.locals import *


def processEvents():
    for event in pygame.event.get():
        cond1 = (event.type == QUIT)
        cond2 = ((event.type == KEYDOWN) and (event.key == K_ESCAPE))
        if cond1 or cond2:
            pygame.quit()
            print "This is too much. I quit!"
            return True
    return False

def updateCells():
    print "update cells."

GRID = []
for row in range(16):
    GRID.append([])
    for col in range(16):
        GRID[row].append(0)

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
    



