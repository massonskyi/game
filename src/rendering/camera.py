from OpenGL.raw.GLES1.VERSION.GLES1_1_0 import glTranslatef


class Camera:
    def __init__(self):
        self.position = (0, 0, 0)

    def set_view(self):
        glTranslatef(-self.position[0], -self.position[1], -self.position[2])
