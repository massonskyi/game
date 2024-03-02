import numpy as np
import pygame
from OpenGL.GL import *
from OpenGL.arrays import vbo
from OpenGL.GL.shaders import *
from src.rendering.shader import Shader
from src.game.block import Block


class BlockRenderer:
    def __init__(self):
        self.shader = Shader("C:\\Users\\gavri\\PycharmProjects\\minecraft\\assets\\shaders\\vertex.glsl",
                             "C:\\Users\\gavri\\PycharmProjects\\minecraft\\assets\\shaders\\fragment.glsl")
        self.vao = glGenVertexArrays(1)
        self.vbo = glGenBuffers(1)

        vertices = [
            # Positions            # Texture Coords
            # Back face
            -0.5, -0.5, -0.5, 0.0, 0.0,
            0.5, -0.5, -0.5, 1.0, 0.0,
            0.5, 0.5, -0.5, 1.0, 1.0,
            0.5, 0.5, -0.5, 1.0, 1.0,
            -0.5, 0.5, -0.5, 0.0, 1.0,
            -0.5, -0.5, -0.5, 0.0, 0.0,
            # Front face
            -0.5, -0.5, 0.5, 0.0, 0.0,
            0.5, -0.5, 0.5, 1.0, 0.0,
            0.5, 0.5, 0.5, 1.0, 1.0,
            0.5, 0.5, 0.5, 1.0, 1.0,
            -0.5, 0.5, 0.5, 0.0, 1.0,
            -0.5, -0.5, 0.5, 0.0, 0.0,
            # Left face
            -0.5, 0.5, 0.5, 1.0, 0.0,
            -0.5, 0.5, -0.5, 1.0, 1.0,
            -0.5, -0.5, -0.5, 0.0, 1.0,
            -0.5, -0.5, -0.5, 0.0, 1.0,
            -0.5, -0.5, 0.5, 0.0, 0.0,
            -0.5, 0.5, 0.5, 1.0, 0.0,
            # Right face
            0.5, 0.5, 0.5, 1.0, 0.0,
            0.5, 0.5, -0.5, 1.0, 1.0,
            0.5, -0.5, -0.5, 0.0, 1.0,
            0.5, -0.5, -0.5, 0.0, 1.0,
            0.5, -0.5, 0.5, 0.0, 0.0,
            0.5, 0.5, 0.5, 1.0, 0.0,
            # Bottom face
            -0.5, -0.5, -0.5, 0.0, 1.0,
            0.5, -0.5, -0.5, 1.0, 1.0,
            0.5, -0.5, 0.5, 1.0, 0.0,
            0.5, -0.5, 0.5, 1.0, 0.0,
            -0.5, -0.5, 0.5, 0.0, 0.0,
            -0.5, -0.5, -0.5, 0.0, 1.0,
            # Top face
            -0.5, 0.5, -0.5, 0.0, 1.0,
            0.5, 0.5, -0.5, 1.0, 1.0,
            0.5, 0.5, 0.5, 1.0, 0.0,
            0.5, 0.5, 0.5, 1.0, 0.0,
            -0.5, 0.5, 0.5, 0.0, 0.0,
            -0.5, 0.5, -0.5, 0.0, 1.0
        ]

        vertices = np.array(vertices, dtype=np.float32)

        self.bind()
        self.vbo_data(vertices, GL_STATIC_DRAW)
        self.setup_vertex_attributes()
        self.unbind()

    def bind(self):
        glBindVertexArray(self.vao)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)

    def unbind(self):
        glBindVertexArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

    def vbo_data(self, data, usage):
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, data.nbytes, data, usage)

    def setup_vertex_attributes(self):
        self.shader.use()

        stride = 5 * 4  # 5 float components per vertex (position + texture coords)

        # Position attribute
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        # Texture coordinate attribute
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(12))
        glEnableVertexAttribArray(1)

    def render_block(self, block: Block, model_matrix: np.array):
        ...
        """
        self.shader.use()

        # Ensure the model matrix is a 4x4 matrix
        if model_matrix.shape != (4, 4):
            raise ValueError("Invalid model matrix shape. Expected a 4x4 matrix.")
        self.shader.set_uniform("model", model_matrix)
        self.shader.set_uniform("texture_sampler", 0)

        # Bind the appropriate texture for this block
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, block.texture.id)

        # Draw the block
        glBindVertexArray(self.vao)
        glDrawArrays(GL_TRIANGLES, 0, 36)
        glBindVertexArray(0)
        """