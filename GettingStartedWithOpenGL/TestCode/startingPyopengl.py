import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

set_width = 1000
set_height = 800
pygame.init()
screen = pygame.display.set_mode((set_width, set_height), DOUBLEBUF | OPENGL)

def init_ortho():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, 640, 0, 480)

done = False
init_ortho()
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glPointSize(10)
        glBegin(GL_POINTS)
        glVertex2i(300, 300)
        glEnd()

        pygame.display.flip()
        pygame.time.wait(100)
pygame.quit()