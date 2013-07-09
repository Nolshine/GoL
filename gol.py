import pygame
from pygame.locals import *

from random import randrange

#globals:
PAUSED = False

TILE_SIZE = 16 #...squared. that's the tile size in px

GRID_SIZE = 32 #...squared. square size of grid, in tiles.

SCREEN_SIZE = ((GRID_SIZE*TILE_SIZE),(GRID_SIZE*TILE_SIZE)) #size of window

SPEED = 40 #time between updates in ms

GRID = []
for row in range(GRID_SIZE):
    GRID.append([])
    for col in range(GRID_SIZE):
        GRID[row].append(randrange(3))




def processEvents():
    event_array = []
    for event in pygame.event.get():
        cond1 = (event.type == QUIT)
        cond2 = ((event.type == KEYDOWN) and (event.key == K_ESCAPE))
        cond3 = ((event.type == KEYDOWN) and (event.key == K_SPACE))
        cond4 = ((event.type == KEYDOWN) and (event.key == K_r))
        cond5 = ((event.type == KEYDOWN) and (event.key == K_e))
        cond6 = ((event.type == KEYDOWN) and (event.key == K_f))
        
        if cond1 or cond2:
            pygame.quit()
            print "This is too much. I quit!"
            quit()
            
        if cond3:
            event_array.append("PAUSE")
            
        if event.type == MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            pressed = pygame.mouse.get_pressed()
            if GRID[(pos[1]/TILE_SIZE)][(pos[0]/TILE_SIZE)] == 0:
                if pressed[0]:
                    colour = 1
                elif pressed[2]:
                    colour = 2
                GRID[(pos[1]/TILE_SIZE)][(pos[0]/TILE_SIZE)] = colour
                if colour == 1:
                    event_array.append("MAKE_RED")
                if colour == 2:
                    event_array.append("MAKE_BLUE")
            else:
                GRID[(pos[1]/TILE_SIZE)][(pos[0]/TILE_SIZE)] = 0
                event_array.append("MAKE_DEAD")
                
        if event.type == MOUSEBUTTONUP:
            event_array.append("MAKE_STOP")
            
        if cond4:
            event_array.append("RESET")

        if cond5:
            event_array.append("ERASE")

        if cond6:
            event_array.append("FILL")
            
    return event_array
                

def updateCells():
    #mark positions to change
    change_marks = []
    
    for row in range(len(GRID)):
        for col in range(len(GRID[0])):
            change_marks = updateCell(row,col,change_marks)

    for item in change_marks:
        if (GRID[item[0]][item[1]] == 1) or (GRID[item[0]][item[1]] == 2):
            GRID[item[0]][item[1]] = 0
        else:
            GRID[item[0]][item[1]] = item[2]
    
def updateCell(row, col, change_marks):
    #must loop twice, once to find out what to needs changing,
    #and then again to change it without being affected by my own changes.
    #which neighbours do I have? am I a corner? an edge?
    left_edge = (col == 0)
    right_edge = (col == (len(GRID[row])-1))
    top_edge = (row == 0)
    bottom_edge = (row == (len(GRID)-1))
    #now I pick up on the rules of John Conway's GoL
    #am I alive?
    living = False
    if (GRID[row][col] == 1) or (GRID[row][col] == 2):
        living = True
    #count my neighbours
    neighbours = 0
    reds = 0
    blues = 0
    for check_row in range(3):

        for check_col in range(3):
            
            checking_row = (row-1)+check_row
            checking_col = (col-1)+check_col
            if checking_row > len(GRID)-1:
                checking_row = 0
            if checking_col > len(GRID[row])-1:
                checking_col = 0
            if checking_row == row and checking_col == col:
                continue
            if (GRID[checking_row][checking_col] == 1) or (GRID[checking_row][checking_col] == 2):
                neighbours += 1
                if GRID[checking_row][checking_col] == 1:
                    reds += 1
                elif GRID[checking_row][checking_col] == 2:
                    blues += 1
    #determine which rules to use
    if living:
        #apply rules of live cells
        #1) Any live cell with fewer than two live neighbours dies,
        #   as if caused by under-population.
        if neighbours < 2:
            change_marks.append((row,col,0))
        #2) Any live cell with two or three live neighbours lives on
        #   to the next generation. (I don't need to check for this,
        #   as checking for the other living rules suffices.)
        #3) Any live cell with more than three live neighbours dies,
        #   as if by overcrowding.
        if neighbours > 3:
            change_marks.append((row,col,0))
    else:
        #apply rules of dead cells
        #4) Any dead cell with exactly three live neighbours becomes
        #   a live cell, as if by reproduction.
        if neighbours == 3:
            colour = 1
            if reds < blues:
                colour = 2
            change_marks.append((row,col,colour))

    return change_marks

    
def renderGrid():
    #let's see if I can access GRID from here.
    for row in range(len(GRID)):
        for col in range(len(GRID[0])):
            renderTile(row,col)

def renderTile(row,col):
    tile = pygame.Rect((col*TILE_SIZE),(row*TILE_SIZE),TILE_SIZE,TILE_SIZE)
    inner = pygame.Rect(((col*TILE_SIZE)+1), ((row*TILE_SIZE)+1),
                        TILE_SIZE-2, TILE_SIZE-2)
    
    if GRID[row][col] == 1:
        pygame.draw.rect(screen, (0,0,0), tile)
        pygame.draw.rect(screen, (255,0,0), inner)
    elif GRID[row][col] == 2:
        pygame.draw.rect(screen, (0,0,0), tile)
        pygame.draw.rect(screen, (0,0,255), inner)
    else:
        pygame.draw.rect(screen, (255,255,255), tile)
        pygame.draw.rect(screen, (0,0,0), inner)

def resetGrid():
    for row in range(len(GRID)):
        for col in range(len(GRID[row])):
            GRID[row][col] = randrange(3)

def eraseGrid():
    for row in range(len(GRID)):
        for col in range(len(GRID[row])):
            GRID[row][col] = 0

def fillGrid():
    for row in range(len(GRID)):
        for col in range(len(GRID[row])):
            GRID[row][col] = randrange(1,3)

#START THE SIM
pygame.init()

screen = pygame.display.set_mode(SCREEN_SIZE, DOUBLEBUF)

clock = pygame.time.Clock()

pygame.display.set_caption("click cells to change. space to pause/unpause. 'r' to reseed.")

update_timer = 0

make = ""

while True:

    time_passed = clock.tick(50) #limits FPS to 50 and stores time.

    screen.fill((0,0,0)) #draw black background.

    event_array = processEvents()

    
    if "PAUSE" in event_array:
        PAUSED = not PAUSED
    if "RESET" in event_array:
        resetGrid()
    if "ERASE" in event_array:
        eraseGrid()
    if "FILL" in event_array:
        fillGrid()
        
    if ("MAKE_RED" in event_array):
        make = "MAKE_RED"
    if ("MAKE_BLUE" in event_array):
        make = "MAKE_BLUE"
    if (make == "MAKE_RED"):
        pos = pygame.mouse.get_pos()
        GRID[(pos[1]/TILE_SIZE)][(pos[0]/TILE_SIZE)] = 1
    if (make == "MAKE_BLUE"):
        pos = pygame.mouse.get_pos()
        GRID[(pos[1]/TILE_SIZE)][(pos[0]/TILE_SIZE)] = 2
        
    if ("MAKE_DEAD" in event_array):
        make = "MAKE_DEAD"
    if (make == "MAKE_DEAD"):
        pos = pygame.mouse.get_pos()
        GRID[(pos[1]/TILE_SIZE)][(pos[0]/TILE_SIZE)] = 0
        
    if "MAKE_STOP" in event_array:
        make = ""
    
    

    if not PAUSED:
        update_timer += time_passed
        if update_timer >= SPEED:
            updateCells()
            update_timer = 0
            
    renderGrid()
    pygame.display.update()


