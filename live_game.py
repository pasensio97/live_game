import pygame
import numpy as np

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

nyC, nxC = 25, 25
dimX = WIDTH / nyC
dimY = HEIGHT / nxC

# colors
WHITE = (255,255,255)
BLACK = (0,0,0)
GREY = (25,25,25)
win.fill(GREY)

# Game State; 0 dead, 1 live
global gameState
gameState = np.zeros( (nxC, nyC) )

# automata palo
gameState[10,5] = 1
gameState[10,6] = 1
gameState[10,7] = 1


# setup game loop
FPS = 2
clock = pygame.time.Clock()
run = True

def game(gameState):
    new_gameState = np.copy( gameState )
    for y in range(0, nyC):
        for x in range(0, nxC):

            # se suman el numero de vecinos vivos
            n_neight = gameState[ (x-1) % nxC ][ (y-1) % nyC ] + \
                        gameState[ (x-1) % nxC ][ y % nyC ] + \
                        gameState[ (x-1) % nxC ][ (y+1) % nyC ] + \
                        gameState[ x % nxC ][ (y-1) % nyC ] + \
                        gameState[ x % nxC ][ (y+1) % nyC ] + \
                        gameState[ (x+1) % nxC ][ (y-1) % nyC ] + \
                        gameState[ (x+1) % nxC ][ y % nyC ] + \
                        gameState[ (x+1) % nxC ][ (y+1) % nyC ]
            
            # se aplica la norma del juego
            if gameState[x,y] == 0 and n_neight == 3:
                new_gameState[x,y] = 1

            if gameState[x,y] == 1 and (n_neight < 2 or n_neight > 3):
                new_gameState[x,y] = 0


            # rect = [
            #     (y) * RWIDTH,
            #     (x) * RWIDTH,
            #     (y+1) * RWIDTH,
            #     (x+1) * RWIDTH
            # ]


            rect = [
                (y) * dimX,
                (x) * dimY,
                (y+1) * dimX,
                (x+1) * dimY
            ]
            if new_gameState[x][y] == 0:
                pygame.draw.rect(win, BLACK, rect, 1)
            else:
                pygame.draw.rect(win, WHITE, rect, 0)

    gameState = np.copy(new_gameState)
    return gameState
        
# print(nyC,nxC,RWIDTH)

while run:
    clock.tick(FPS)
    win.fill(GREY)
    gameState = game(gameState)

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            print(pos)

pygame.quit()