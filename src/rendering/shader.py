import glm
import pygame
from OpenGL.GL import *
from OpenGL.GL.shaders import *

class Shader:
    def __init__(self, vertex_file, fragment_file):
        self.vertex_file = vertex_file
        self.fragment_file = fragment_file
        self.program = self.compile_shader()
        self.uniform_locations = {}

    def compile_shader(self):
        vertex_shader = self.compile_shader_file(self.vertex_file, GL_VERTEX_SHADER)
        fragment_shader = self.compile_shader_file(self.fragment_file, GL_FRAGMENT_SHADER)

        program = glCreateProgram()
        glAttachShader(program, vertex_shader)
        glAttachShader(program, fragment_shader)
        glLinkProgram(program)

        success = glGetProgramiv(program, GL_LINK_STATUS)
        if not success:
            info_log = glGetProgramInfoLog(program)
            print(f"Error linking shader program: {info_log}")
            raise ValueError("Error linking shader program")

        glDeleteShader(vertex_shader)
        glDeleteShader(fragment_shader)

        return program

    def compile_shader_file(self, file_path, shader_type):
        with open(file_path, "r") as file:
            shader_source = file.read()

        shader = glCreateShader(shader_type)
        glShaderSource(shader, shader_source)
        glCompileShader(shader)

        success = glGetShaderiv(shader, GL_COMPILE_STATUS)
        if not success:
            info_log = glGetShaderInfoLog(shader)
            print(f"Error compiling {file_path}: {info_log}")
            raise ValueError(f"Error compiling {file_path}")

        return shader

    def use(self):
        glUseProgram(self.program)

    def set_uniform(self, name, value):
        if name not in self.uniform_locations:
            location = glGetUniformLocation(self.program, name)
            self.uniform_locations[name] = location

        location = self.uniform_locations[name]

        if isinstance(value, (int, float)):
            glUniform1f(location, value)
        elif isinstance(value, tuple) and len(value) == 2:
            glUniform2f(location, *value)
        elif isinstance(value, tuple) and len(value) == 3:
            glUniform3f(location, *value)
        elif isinstance(value, tuple) and len(value) == 4:
            glUniform4f(location, *value)
        elif isinstance(value, glm.mat4):
            glUniformMatrix4fv(location, 1, GL_FALSE, glm.value_ptr(value))
        else:
            raise ValueError(f"Invalid uniform value: {value}")
