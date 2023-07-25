import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from Utils import *

set_width = 800
set_height = 600
pygame.init()
screen = pygame.display.set_mode((set_width, set_height), DOUBLEBUF | OPENGL)

def init_ortho():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0,640,480,0)

def plot_point():
    glBegin(GL_POINTS)
    for p in points:
        glVertex2f(p[0],p[1])
    glEnd()

done = False
init_ortho()
glPointSize(50)
points = []
while not done:
    p = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == MOUSEBUTTONDOWN:
            p = pygame.mouse.get_pos()
            points.append(
                (map_value(0, set_width, 0, 640, p[0]),
                 map_value(0, set_height, 0, 480, p[1])
                )
            )

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    plot_point()
    pygame.display.flip()
    pygame.time.wait(100)
pygame.quit()