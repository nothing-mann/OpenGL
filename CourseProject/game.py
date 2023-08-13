#change from pygame to glfw for accurate mouse movements
import math
import glfw
import glfw.GLFW as GLFW_CONSTANTS
# import pygame as pg
from OpenGL.GL import *
import numpy as np
import ctypes
from OpenGL.GL.shaders import compileProgram, compileShader
import pyrr
from PIL import Image


SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720
RETURN_ACTION_CONTINUE = 0
RETURN_ACTION_END = 1

def initialize_glfw():
    glfw.init()
    glfw.window_hint(GLFW_CONSTANTS.GLFW_CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(GLFW_CONSTANTS.GLFW_CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(
        GLFW_CONSTANTS.GLFW_OPENGL_PROFILE,
        GLFW_CONSTANTS.GLFW_OPENGL_CORE_PROFILE
    )
    glfw.window_hint(
        GLFW_CONSTANTS.GLFW_OPENGL_FORWARD_COMPAT,
        GLFW_CONSTANTS.GLFW_TRUE
    )
    glfw.window_hint(GLFW_CONSTANTS.GLFW_DOUBLEBUFFER, GL_FALSE)

    window = glfw.create_window(SCREEN_WIDTH, SCREEN_HEIGHT, "My Game", None, None)
    glfw.make_context_current(window)
    glfw.set_input_mode(
        window,
        GLFW_CONSTANTS.GLFW_CURSOR,
        GLFW_CONSTANTS.GLFW_CURSOR_HIDDEN
    )
    return window

def loadMesh(filename: str) -> list[float]:
    """
        Load a mesh from an obj file.

        Parameters:

            filename: the filename.

        Returns:

            The loaded data, in a flattened format.
    """

    v = []
    vt = []
    vn = []

    vertices = []

    with open(filename, "r") as file:

        line = file.readline()

        while line:

            words = line.split(" ")
            match words[0]:

                case "v":
                    v.append(read_vertex_data(words))

                case "vt":
                    vt.append(read_texcoord_data(words))

                case "vn":
                    vn.append(read_normal_data(words))

                case "f":
                    read_face_data(words, v, vt, vn, vertices)

            line = file.readline()

    return vertices


def read_vertex_data(words: list[str]) -> list[float]:
    """
        Returns a vertex description.
    """

    return [
        float(words[1]),
        float(words[2]),
        float(words[3])
    ]


def read_texcoord_data(words: list[str]) -> list[float]:
    """
        Returns a texture coordinate description.
    """

    return [
        float(words[1]),
        float(words[2])
    ]


def read_normal_data(words: list[str]) -> list[float]:
    """
        Returns a normal vector description.
    """

    return [
        float(words[1]),
        float(words[2]),
        float(words[3])
    ]


def read_face_data(
        words: list[str],
        v: list[list[float]], vt: list[list[float]],
        vn: list[list[float]], vertices: list[float]) -> None:
    """
        Reads an edgetable and makes a face from it.
    """

    triangleCount = len(words) - 3

    for i in range(triangleCount):
        make_corner(words[1], v, vt, vn, vertices)
        make_corner(words[2 + i], v, vt, vn, vertices)
        make_corner(words[3 + i], v, vt, vn, vertices)


def make_corner(corner_description: str,
                v: list[list[float]], vt: list[list[float]],
                vn: list[list[float]], vertices: list[float]) -> None:
    """
        Composes a flattened description of a vertex.
    """

    v_vt_vn = corner_description.split("/")

    for element in v[int(v_vt_vn[0]) - 1]:
        vertices.append(element)
    for element in vt[int(v_vt_vn[1]) - 1]:
        vertices.append(element)
    for element in vn[int(v_vt_vn[2]) - 1]:
        vertices.append(element)


class Cube:
    def __init__(self, position, eulers):
        self.position = np.array(position, dtype=np.float32)
        self.eulers = np.array(eulers, dtype=np.float32)

class Light:
    def __init__(self, position, color, strength):
        self.position = np.array(position, dtype=np.float32)
        self.color = np.array(color, dtype=np.float32)
        self.strength = strength

class Player:
    def __init__(self, position):
        self.position = np.array(position, dtype=np.float32)
        #Angle in the horizontal direction (North, east, south, west)
        self.theta = 0
        #Angle in the vertical direction (up, down)
        self.phi = 0
        #for forward, up and right
        self.update_vectors()

    def update_vectors(self):
        #we are using spherical coordinates for this.
        self.forwards = np.array(
            [
                np.cos(np.deg2rad(self.theta))*np.cos(np.deg2rad(self.phi)),
                np.sin(np.deg2rad(self.theta))*np.cos(np.deg2rad(self.phi)),
                np.sin(np.deg2rad(self.phi))
            ]
        )
        globalUp = np.array([0,0,1], dtype=np.float32)

        #for right, we will cross product between the forwards and up direction. We will also use cross product for up
        self.right = np.cross(self.forwards, globalUp)
        self.up = np.cross(self.right, self.forwards)

#The scene class adds all the entities that are to be rendered in the scene
class Scene:
    def __init__(self):
        self.cubes = [
            Cube(
            position=[6,0,1],
            eulers=[0,0,0]),
        ]
        self.bblights = [
            Cube(
                position=[3, 0, 0.5],
                eulers=[0, 0, 0]),
        ]
        self.lights = [
            Light(
                position= [
                    np.random.uniform(low=2.0, high=8.0),
                    np.random.uniform(low=-4.0, high=4.0),
                    np.random.uniform(low=2.0, high=4.0)
                ],
                color= [
                    np.random.uniform(low=0.0, high=1.0),
                    np.random.uniform(low=0.0, high=1.0),
                    np.random.uniform(low=0.0, high=1.0)
                ],
                strength=3
            )
            for i in range(8)
        ]
        self.player = Player(position=[0,0,2])


    def update(self, rate):

        #cube is rotated here.

        for cube in self.cubes:
            cube.eulers[1] +=  0.25 * rate
            if cube.eulers[1] > 360:
                cube.eulers[1] -= 360

    #moving the player
    def move_player(self, dPos):
        dPos = np.array(dPos, dtype=np.float32)
        self.player.position += dPos
    def spin_player(self, dTheta, dPhi):
        #horizontal spinning
        self.player.theta += dTheta
        if self.player.theta > 360:
            self.player.theta -= 360
        if self.player.theta < 0:
            self.player.theta += 360

        #vertical spinning done so that player cannot look too high up or too low down
        self.player.phi = min(89, max(-89, self.player.phi +dPhi))
        self.player.update_vectors()


class App:
    def __init__(self, window):
        self.window = window
        self.renderer = GraphicsEngine()
        self.scene = Scene()

        self.lastTime = glfw.get_time()
        self.currentTime = 0
        self.numFrames = 0
        self.frameTime = 0
        # self.cube = Cube(
        #     position=[0, 0, -3],
        #     eulers=[0, 0, 0]
        # )
        """
        w : 1
        a : 2
        w and a : 3
        s : 4
        w and s : 5
        a and s : 6
        w and a and s: 7
        d : 8
        w and d : 9
        a and d : 10
        w and a and d: 11 
        s and d: 12
        w and s and d: 13
        a and s and d: 14
        w and a and s and d: 15
        """
        self.walk_offset_lookup = {
            1 : 0,
            2 : 90,
            3 : 45,
            4 : 180,
            6 : 135,
            7 : 90,
            8 : 270,
            9 : 315,
            11 : 0,
            12 : 225,
            13 : 270,
            14 : 180
        }

        self.main_loop()



    def main_loop(self):
        running = True
        while running:
            if glfw.window_should_close(self.window) or glfw.get_key(self.window, GLFW_CONSTANTS.GLFW_KEY_ESCAPE) == GLFW_CONSTANTS.GLFW_PRESS:
               running = False

            self.handleKeys()
            self.handleMouse()

            glfw.poll_events()

            self.scene.update(self.frameTime / 16.7)
            self.renderer.render(self.scene)

                #update cube
                    # self.cube.eulers[2] += 0.2
                    # if (self.cube.eulers[2] > 360):
                    #     self.cube.eulers[2] -= 360

                #refresh screen
                #timing
            self.calculateFramerate()
        self.quit()

    def handleKeys(self):
        """
            Takes action based on the keys currently pressed.
        """
        combo = 0
        directionModifier = 0
        if glfw.get_key(self.window, GLFW_CONSTANTS.GLFW_KEY_W) == GLFW_CONSTANTS.GLFW_PRESS:
            combo += 1
        if glfw.get_key(self.window, GLFW_CONSTANTS.GLFW_KEY_A) == GLFW_CONSTANTS.GLFW_PRESS:
            combo += 2
        if glfw.get_key(self.window, GLFW_CONSTANTS.GLFW_KEY_S) == GLFW_CONSTANTS.GLFW_PRESS:
            combo += 4
        if glfw.get_key(self.window, GLFW_CONSTANTS.GLFW_KEY_D) == GLFW_CONSTANTS.GLFW_PRESS:
            combo += 8

        if combo in self.walk_offset_lookup:
            directionModifier = self.walk_offset_lookup[combo]
            dPos = [
                #...................................................
                # set the time for the movement using the keys here
                #...................................................
                0.1 * self.frameTime / 16.7 * np.cos(np.deg2rad(self.scene.player.theta + directionModifier)),
                0.1 * self.frameTime / 16.7 * np.sin(np.deg2rad(self.scene.player.theta + directionModifier)),
                0
            ]
            self.scene.move_player(dPos)

    def handleMouse(self):
        (x,y) = glfw.get_cursor_pos(self.window)
        rate = self.frameTime / 16.7
        theta_increment = rate * ((SCREEN_WIDTH / 2) - x)
        phi_increment = rate * ((SCREEN_HEIGHT / 2) - y)
        self.scene.spin_player(theta_increment, phi_increment)
        glfw.set_cursor_pos(self.window, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    def calculateFramerate(self):
        self.currentTime = glfw.get_time()
        delta = self.currentTime - self.lastTime
        if (delta >= 1):
            framerate = max(1, int(self.numFrames / delta))
            glfw.set_window_title(self.window, f"Running at {framerate} fps.")
            self.lastTime = self.currentTime
            self.numFrames = -1
            self.frameTime = float(1000.0/max(1,framerate))
        self.numFrames += 1

    def quit(self):
        self.renderer.quit()

#everything related to rendering is done here in GraphicsEngine
class GraphicsEngine:
    def __init__(self):
        #initialize OpenGL
        glClearColor(0, 0, 0, 1)
        self.shader = self.createShader("shaders/vertex.txt", "shaders/fragment.txt")
        glUseProgram(self.shader)
        glUniform1i(glGetUniformLocation(self.shader, "ImageTexture"), 0)

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        self.random_texture = Material("textures/wood.jpeg")
        self.cube_mesh = Mesh("models/cube.obj")

        self.light_texture = Material("billboards/greenlight.png")
        self.light_billboard = BillBoard(w=0.2, h=0.1)

        projection_transform = pyrr.matrix44.create_perspective_projection(
            fovy=45, aspect=640 / 480,
            near=0.1, far=10, dtype=np.float32
        )
        glUniformMatrix4fv(
            glGetUniformLocation(self.shader, "projection"),
            1, GL_FALSE, projection_transform
        )
        self.modelMatrixLocation = glGetUniformLocation(self.shader, "model")
        self.viewMatrixLocation = glGetUniformLocation(self.shader, "view")
        self.lightLocation = {
            "position":
                [
                    glGetUniformLocation(self.shader, f"Lights[{i}].position")
                    for i in range(8)
                ],
            "color":
                [
                    glGetUniformLocation(self.shader, f"Lights[{i}].color")
                    for i in range(8)
                ],
            "strength":
                [
                    glGetUniformLocation(self.shader, f"Lights[{i}].strength")
                    for i in range(8)
                ]
        }
        self.cameraPosition = glGetUniformLocation(self.shader, "cameraPosition")
        self.tintPosition = glGetUniformLocation(self.shader, "tint")

    def createShader(self, vertexFilepath, fragmentFilepath):
        with open(vertexFilepath, 'r') as f:
            vertex_src = f.readlines()
        with open(fragmentFilepath, 'r') as f:
            fragment_src = f.readlines()
        shader = compileProgram(
            compileShader(vertex_src, GL_VERTEX_SHADER),
            compileShader(fragment_src, GL_FRAGMENT_SHADER)
        )
        return shader

    def render(self, scene):
        #refresh screen
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # glEnable(GL_BLEND)
        # glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        glUseProgram(self.shader)

        view_transformation = pyrr.matrix44.create_look_at(
            eye= scene.player.position,
            target= scene.player.position + scene.player.forwards,
            up = scene.player.up,
            dtype=np.float32
        )
        glUniformMatrix4fv(self.viewMatrixLocation, 1, GL_FALSE, view_transformation)

        for i,light in enumerate(scene.lights):
            glUniform3fv(self.lightLocation["position"][i], 1, light.position)
            glUniform3fv(self.lightLocation["color"][i], 1, light.color)
            glUniform1f(self.lightLocation["strength"][i], light.strength)
        glUniform3fv(self.cameraPosition, 1, scene.player.position)


        self.random_texture.use()
        glBindVertexArray(self.cube_mesh.vao)


        for cube in scene.cubes:
            model_transformation = pyrr.matrix44.create_identity(dtype=np.float32)
            model_transformation = pyrr.matrix44.multiply(
                m1= model_transformation,
                m2= pyrr.matrix44.create_from_eulers(
                    eulers=np.radians(cube.eulers),
                    dtype=np.float32
                )
            )
            model_transformation = pyrr.matrix44.multiply(
                m1=model_transformation,
                m2=pyrr.matrix44.create_from_translation(
                    vec= cube.position,
                    dtype=np.float32
                )
            )
            glUniformMatrix4fv(self.modelMatrixLocation, 1, GL_FALSE, model_transformation)

            glDrawArrays(GL_TRIANGLES, 0, self.cube_mesh.vertex_count)


        for light in scene.lights:
            self.light_texture.use()
            glUniform3fv(self.tintPosition, 1, light.color)

            directionFromPlayer = light.position - scene.player.position
            angle1 = np.arctan2(-directionFromPlayer[1], directionFromPlayer[0])
            dist2d = math.sqrt(directionFromPlayer[0]**2 + directionFromPlayer[1]**2)
            angle2 = np.arctan2(directionFromPlayer[2], dist2d)

            model_transform = pyrr.matrix44.create_identity(dtype=np.float32)
            model_transform = pyrr.matrix44.multiply(
                model_transform,
                pyrr.matrix44.create_from_y_rotation(theta = angle2, dtype=np.float32)
            )
            model_transform = pyrr.matrix44.multiply(
                model_transform,
                pyrr.matrix44.create_from_z_rotation(theta=angle1, dtype=np.float32)
            )
            model_transform = pyrr.matrix44.multiply(
                model_transform,
                pyrr.matrix44.create_from_translation(vec=light.position, dtype=np.float32)
            )

            glUniformMatrix4fv(self.modelMatrixLocation, 1, GL_FALSE, model_transform)
            glBindVertexArray(self.light_billboard.vao)
            glDrawArrays(GL_TRIANGLES, 0, self.light_billboard.vertex_count)

        glUniform3fv(self.tintPosition, 1, np.array([1,1,1], dtype=np.float32))

        glFlush()
        # pg.display.flip()

    def quit(self):
        self.cube_mesh.destroy()
        self.random_texture.destroy()
        self.light_billboard.destroy()
        self.light_texture.destroy()
        glDeleteProgram(self.shader)
        # pg.quit()
class Mesh:
    """
        A mesh that can represent an obj model.
    """

    def __init__(self, filename: str):
        """
            Initialize the mesh.
        """

        # x, y, z, s, t, nx, ny, nz
        vertices = loadMesh(filename)
        self.vertex_count = len(vertices) // 8
        vertices = np.array(vertices, dtype=np.float32)

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        # Vertices
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        # position
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(0))
        # texture
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(12))
        # normal
        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(20))

    def arm_for_drawing(self) -> None:
        """
            Arm the triangle for drawing.
        """
        glBindVertexArray(self.vao)

    def draw(self) -> None:
        """
            Draw the triangle.
        """

        glDrawArrays(GL_TRIANGLES, 0, self.vertex_count)

    def destroy(self) -> None:
        """
            Free any allocated memory.
        """
        glDeleteVertexArrays(1, (self.vao,))
        glDeleteBuffers(1, (self.vbo,))

# class CubeMesh:
#     # x,y,z,s,t
#     def __init__(self):
#         self. vertices = (
#             -0.5, -0.5, -0.5, 0, 0,
#              0.5, -0.5, -0.5, 1, 0,
#              0.5,  0.5, -0.5, 1, 1,
#
#              0.5,  0.5, -0.5, 1, 1,
#             -0.5,  0.5, -0.5, 0, 1,
#             -0.5, -0.5, -0.5, 0, 0,
#
#             -0.5, -0.5,  0.5, 0, 0,
#              0.5, -0.5,  0.5, 1, 0,
#              0.5,  0.5,  0.5, 1, 1,
#
#              0.5,  0.5,  0.5, 1, 1,
#             -0.5,  0.5,  0.5, 0, 1,
#             -0.5, -0.5,  0.5, 0, 0,
#
#             -0.5,  0.5,  0.5, 1, 0,
#             -0.5,  0.5, -0.5, 1, 1,
#             -0.5, -0.5, -0.5, 0, 1,
#
#             -0.5, -0.5, -0.5, 0, 1,
#             -0.5, -0.5,  0.5, 0, 0,
#             -0.5,  0.5,  0.5, 1, 0,
#
#              0.5,  0.5,  0.5, 1, 0,
#              0.5,  0.5, -0.5, 1, 1,
#              0.5, -0.5, -0.5, 0, 1,
#
#              0.5, -0.5, -0.5, 0, 1,
#              0.5, -0.5,  0.5, 0, 0,
#              0.5,  0.5,  0.5, 1, 0,
#
#             -0.5, -0.5, -0.5, 0, 1,
#              0.5, -0.5, -0.5, 1, 1,
#              0.5, -0.5,  0.5, 1, 0,
#
#              0.5, -0.5,  0.5, 1, 0,
#             -0.5, -0.5,  0.5, 0, 0,
#             -0.5, -0.5, -0.5, 0, 1,
#
#             -0.5,  0.5, -0.5, 0, 1,
#              0.5,  0.5, -0.5, 1, 1,
#              0.5,  0.5,  0.5, 1, 0,
#
#              0.5,  0.5,  0.5, 1, 0,
#             -0.5,  0.5,  0.5, 0, 0,
#             -0.5,  0.5, -0.5, 0, 1
#         )
#         self.vertex_count = len(self.vertices) // 5
#         #we use np.array to convert the vertices into float32 datatype for opengl to read the vertices properly.
#         self.vertices = np.array(self.vertices, dtype=np.float32)
#
#         self.vao = glGenVertexArrays(1) #Generates vertex arrays
#         glBindVertexArray(self.vao)
#         self.vbo = glGenBuffers(1) #Generates vertex buffers
#         glBindBuffer(GL_ARRAY_BUFFER,self.vbo)
#         glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)
#
#         glEnableVertexAttribArray(0)
#         glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p(0))
#
#         glEnableVertexAttribArray(1)
#         glVertexAttribPointer(1 , 2, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p(12))
#
#     def destroy(self):
#         glDeleteVertexArrays(1, (self.vao,))
#         glDeleteBuffers(1, (self.vbo,))

class Material:
    def __init__(self, filepath: str):
        self.texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        with Image.open(filepath, mode = 'r') as image:
            # image = pg.image.load(filepath).convert_alpha()
            image_width, image_height = image.size
            image = image.convert("RGBA")
            image_data = bytes(image.tobytes())
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image_width, image_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
        glGenerateMipmap(GL_TEXTURE_2D)

    def use(self):
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture)

    def destroy(self):
        glDeleteTextures(1,(self.texture,))

class BillBoard:
    def __init__(self, w, h):

        #x, y, z, s, t, normal
        self.vertices =  (
            0, -w/2,  h/2, 0, 0, 1, 0, 0,
            0, -w/2, -h/2, 0, 1, 1, 0, 0,
            0,  w/2, -h/2, 1, 1, 1, 0, 0,

            0, -w/2,  h/2, 0, 0, 1, 0, 0,
            0,  w/2, -h/2, 1, 1, 1, 0, 0,
            0,  w/2,  h/2, 1, 0, 1, 0, 0
        )

        self.vertex_count = 6
        self.vertices = np.array(self.vertices, dtype=np.float32)

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        # Vertices
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)
        # position
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(0))
        # texture
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(12))
        # normal
        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(20))

    def destroy(self):
        glDeleteVertexArrays(1, (self.vao,))
        glDeleteBuffers(1, (self.vbo,))


if __name__ == "__main__":
    window = initialize_glfw()
    myapp = App(window)