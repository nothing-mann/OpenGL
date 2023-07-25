import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

set_width = 800
set_height = 600
pygame.init()
screen = pygame.display.set_mode((set_width, set_height), DOUBLEBUF | OPENGL)

def init_ortho():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-4,4,-1,1)

def plot_point():
    glBegin(GL_POINTS)
    glVertex2i(0,0)
    glEnd()

done = False
init_ortho()
glPointSize(5)
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    plot_point()
    pygame.display.flip()
    pygame.time.wait(100)
pygame.quit()