import numpy as np
import pygame
import time

pygame.init()


grid = np.zeros(shape=(40, 40))

blockSize = 20  # Set the size of the grid block
window_width = grid.shape[1] * blockSize
window_height = grid.shape[0] * blockSize
screen = pygame.display.set_mode((window_height, window_width))
pygame.display.set_caption('Game of Life')


def draw_grid():
    for x in range(0, window_width, blockSize):
        for y in range(0, window_height, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            if grid[y//blockSize, x//blockSize] == 1:
                color = (0, 200, 0)
                pygame.draw.rect(screen, color, rect)
            else:
                color = (200, 200, 200)
                pygame.draw.rect(screen, color, rect, 1)


def setup():
    while True:
        screen.fill((0, 0, 0))
        draw_grid()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()  # first element is x, second y
                target = grid[pos[1]//blockSize, pos[0]//blockSize]
                if target == 0:
                    grid[pos[1]//blockSize, pos[0]//blockSize] = 1
                else:
                    grid[pos[1]//blockSize, pos[0]//blockSize] = 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return


def run():
    global grid
    draw_grid()
    while True:
        pygame.display.update()
        new_gen = grid.copy()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        time.sleep(1)
        for pos, cell in np.ndenumerate(grid):
            i = pos[0]
            j = pos[1]
            neighbors = 0
            for n in [i - 1, i, i + 1]:
                if n < 0 or n >= grid.shape[0]:
                    continue
                for m in [j - 1, j, j + 1]:
                    if m < 0 or m >= grid.shape[1]:
                        continue
                    if n == i and m == j:
                        continue
                    elif grid[n, m] == 1:
                        neighbors += 1
            if cell == 0:  # check for generation conditions
                if neighbors == 3:
                    new_gen[i, j] = 1
            elif cell == 1:  # check for death conditions
                if neighbors <= 1:
                    new_gen[i, j] = 0
                elif neighbors >= 4:
                    new_gen[i, j] = 0
        grid = new_gen
        screen.fill((0, 0, 0))
        draw_grid()
        # time.sleep(.0001)


setup()
run()

# todo click and drag mouse to place/remove cells
# todo count generations
# todo check when stasis achieved

