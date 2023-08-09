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


def plot_line():
    for l in points:
        glBegin(GL_LINE_STRIP)
        for coords in l:
            glVertex2f(coords[0], coords[1])
        glEnd()

def save_drawing():
    f = open("drawing.txt", "w")
    f.write(str(len(points)) + '\n')
    for l in points:
        f.write(str(len(l)) + '\n')
        for coords in l:
            f.write(str(coords[0]) + " " + str(coords[1]) + '\n')
    f.close()
    print('The file was saved.')


def load_drawing():
    f = open("drawing.txt", "r")
    no_of_lines = int(f.readline())
    global points
    global line
    points = []
    for l in range(no_of_lines):
        line = []
        points.append(line)
        no_of_coords = int(f.readline())
        for coords in range(no_of_coords):
            px, py = [float(value) for value in next(f).split()]
            line.append((px, py))
            print(str(px) +"," + str(py))



done = False
init_ortho()
glPointSize(50)
points = []
line = []
mouse_down = False
while not done:
    p = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                save_drawing()
            elif event.key == pygame.K_l:
                load_drawing()
            elif event.key == pygame.K_SPACE:
                points = []
        elif event.type == MOUSEBUTTONDOWN:
            mouse_down = True
            line = []
            points.append(line)
        elif event.type == MOUSEBUTTONUP:
            mouse_down = False
        # elif event.type == MOUSEBUTTONDOWN:
        elif event.type == MOUSEMOTION and mouse_down:
                p = pygame.mouse.get_pos()
                line.append(
                        (map_value(0, set_width, 0, 640, p[0]),
                         map_value(0, set_height, 0, 480, p[1])
                        )
                )

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    plot_line()
    pygame.display.flip()
    # pygame.time.wait(100)
pygame.quit()