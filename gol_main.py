import numpy as np
import pygame
import time

pygame.init()


grid = np.zeros(shape=(50, 50))

blockSize = 15  # Set the size of the grid block
window_width = grid.shape[1] * blockSize
window_height = grid.shape[0] * blockSize
screen = pygame.display.set_mode((window_width, window_height + 45))
pygame.display.set_caption('Game of Life')


def draw_grid(gens=0):
    screen.fill((0, 0, 0))
    for x in range(0, window_width, blockSize):
        for y in range(0, window_height, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            if grid[y//blockSize, x//blockSize] == 1:
                color = (0, 200, 0)
                pygame.draw.rect(screen, color, rect)
            else:
                color = (255, 255, 255)
                pygame.draw.rect(screen, color, rect, 1)
    font = pygame.font.Font('freesansbold.ttf', 16)
    text = font.render('Left mouse button to place cells (+shift to remove), Enter to run, C to clear/reset.',
                       True, (200, 200, 200))
    screen.blit(text, (0, window_height))
    screen.blit(font.render(f'Generations:  {gens}', True, (200, 200, 200)), (0, window_height+20))


def setup():
    global grid
    while True:
        # screen.fill((0, 0, 0))
        draw_grid()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
                if event.key == pygame.K_c:
                    grid = np.zeros(shape=(50, 50))
            if event.type == pygame.QUIT:
                exit()
        m_button = pygame.mouse.get_pressed(3)
        remove = False
        if pygame.key.get_pressed()[pygame.K_LSHIFT] or pygame.key.get_pressed()[pygame.K_RSHIFT]:
            remove = True
        if m_button[0]:
            pos = pygame.mouse.get_pos()  # first element is x, second y
            target = grid[pos[1] // blockSize, pos[0] // blockSize]
            if target == 0 and not remove:
                grid[pos[1] // blockSize, pos[0] // blockSize] = 1
            elif target == 1 and remove:
                grid[pos[1] // blockSize, pos[0] // blockSize] = 0


def run():
    global grid
    generations = 0
    while True:
        pygame.display.update()
        new_gen = grid.copy()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    grid = np.zeros(shape=(50, 50))
                    generations = 0
                    return
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
        generations += 1
        draw_grid(generations)
        time.sleep(.15)


while True:
    setup()
    run()


# todo allow player to pause pause run()
# todo check when stasis achieved
# todo changing colors? (fade with time)
