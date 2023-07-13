import pygame
from pygame.locals import *

set_width = 1000
set_height = 800
pygame.init()
screen = pygame.display.set_mode((set_width, set_height), DOUBLEBUF | OPENGL)

done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        pygame.display.flip()
        pygame.time.wait(100)
pygame.quit()