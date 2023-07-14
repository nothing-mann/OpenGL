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
    gluOrtho2D(0,640,0,480)

def star_point(x, y, size):
    glPointSize(size)
    glBegin(GL_POINTS)
    glVertex2i(x,y)
    glEnd()

done = False
init_ortho()
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    #Smallest stars
    star_point(100,400,3)
    star_point(135, 280, 3)
    #Small Stars
    star_point(110, 370, 5)
    star_point(140, 300, 5)
    #Medium star
    star_point(150, 380, 10)
    star_point(250, 385, 10)
    star_point(200, 320, 10)
    #largest star
    star_point(200, 430, 15)

    pygame.display.flip()
    pygame.time.wait(100)
pygame.quit()