import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from Utils import *

pygame.init()

screen_width = 800
screen_height = 800
ortho_left = -400
ortho_right = 400
ortho_top = -400
ortho_bottom = 400

current_pos = (0, 0)
direction = np.array([0,1,0])
# draw_length = 50

screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
pygame.display.set_caption('Turtle Graphics')


def init_ortho():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(ortho_left, ortho_right, ortho_top, ortho_bottom)


def line_to(x, y):
    global current_pos
    glBegin(GL_LINE_STRIP)
    glVertex2f(current_pos[0], current_pos[1])
    glVertex2f(x,y)
    current_pos = (x,y)
    glEnd()

def move_to(x,y):
    global current_pos
    current_pos = (x,y)

def reset_turtle():
    global current_pos
    global direction
    current_pos = (0,0)
    direction = np.array([0,1,0])


def draw_turtle():
    for i in range(10):
        forward(250)
        rotate(129)
        # move_to(100, 300)
        forward(30)


def forward(draw_length):
    new_x = current_pos[0] + direction[0] * draw_length
    new_y = current_pos[1] + direction[1] * draw_length
    line_to(new_x, new_y)


def rotate(angle):
    global direction
    direction = z_rotation(direction, math.radians(angle))

init_ortho()
done = False
glLineWidth(5)
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glBegin(GL_POINTS)
    glVertex2f(0, 0)
    glEnd()
    reset_turtle()
    draw_turtle()
    pygame.display.flip()
pygame.quit()

