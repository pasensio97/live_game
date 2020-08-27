import pygame
import numpy as np
import time

# setup display
pygame.init()
HEIGHT, WIDTH = 800, 800
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Live game")
# UPD = pygame.display.update()

# rectangle dimansions
# RWIDTH = int( min(WIDTH, HEIGHT) / 10 )
# nyC = int(WIDTH/RWIDTH) # numero celdas eje y
# nxC = int(HEIGHT/RWIDTH) # numero celdas eje x

# set number rows and cols
nyC, nxC = 20, 20
dimY = WIDTH / nyC
dimX = HEIGHT / nxC

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (25, 25, 25)
win.fill(GREY)

# Game State; 0 dead, 1 live
global gameState
gameState = np.zeros((nxC, nyC))

# automata palo
gameState[5, 5] = 1
gameState[5, 6] = 1
gameState[5, 7] = 1

gameState[12, 12] = 1
gameState[13, 12] = 1
gameState[14, 12] = 1

# Setup game loop
LPS = 1  # Loops per second
FPS = 30
clock = pygame.time.Clock()
run = True

# Game function
def game(gameState):
    new_gameState = np.copy(gameState)
    for y in range(0, nyC):
        for x in range(0, nxC):

            # se suman el numero de vecinos vivos
            n_neight = (
                gameState[(x - 1) % nxC, (y - 1) % nyC]
                + gameState[(x - 1) % nxC, (y) % nyC]
                + gameState[(x - 1) % nxC, (y + 1) % nyC]
                + gameState[(x) % nxC, (y - 1) % nyC]
                + gameState[(x) % nxC, (y + 1) % nyC]
                + gameState[(x + 1) % nxC, (y - 1) % nyC]
                + gameState[(x + 1) % nxC, (y) % nyC]
                + gameState[(x + 1) % nxC, (y + 1) % nyC]
            )

            # Game rules
            if gameState[x, y] == 0 and n_neight == 3:
                new_gameState[x, y] = 1

            if gameState[x, y] == 1 and (n_neight < 2 or n_neight > 3):
                new_gameState[x, y] = 0

            # Drawing rect
            rect = [(y) * dimY, (x) * dimX, dimY, dimX]
            if new_gameState[x][y] == 0:
                pygame.draw.rect(win, BLACK, rect, 1)
            else:
                pygame.draw.rect(win, WHITE, rect, 0)

    gameState = np.copy(new_gameState)
    return gameState


# Control vars
pauseState = False
time_now = time.clock()

while run:
    # clock.tick(FPS)
    win.fill(GREY)

    time2 = time.clock() - time_now
    if time2 > 1.0 / LPS + 0.1 and not pauseState:
        gameState = game(gameState)
        pygame.display.update()
        time_now = time.clock()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            print(pos)
        if event.type == pygame.KEYDOWN:
            pauseState = not pauseState


pygame.quit()
