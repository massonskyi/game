import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *
from src.game.game import Game
from src.game.world import Direction


def main():
    pygame.init()
    pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL | pygame.RESIZABLE)

    glClearColor(0.7, 0.9, 1.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)

    game = Game(800, 600)
    # Set directional light (replace with desired direction and color)
    game.world.set_directional_light(Direction(0, -1, 0), (1.0, 1.0, 1.0))  # Example

    game.run()


if __name__ == "__main__":
    main()
