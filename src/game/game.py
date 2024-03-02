import pygame
from OpenGL.raw.GL.VERSION.GL_1_0 import glClear, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT

from src.game.world import World
from src.game.player import Player
from src.physics.physics import Physics
from src.rendering.block_rengerer import BlockRenderer


class Game:
    """Represents the main game loop and handles core functionality."""

    def __init__(self, window_width, window_height):
        """
        Initializes the game object.

        Args:
            window_width (int): Width of the game window.
            window_height (int): Height of the game window.
        """

        self.window_width = window_width
        self.window_height = window_height

        # Initialize game components
        self.world = World()
        self.player = Player((0, 10, 0), self.world)
        self.block_renderer = BlockRenderer()
        self.physics = Physics()

        # Initialize clock and delta time
        self.clock = pygame.time.Clock()
        self.delta_time = 0.0
        self.last_update_time = pygame.time.get_ticks()
        # Initialize display and OpenGL context
        pygame.init()
        pygame.display.set_mode((self.window_width, self.window_height), pygame.DOUBLEBUF | pygame.OPENGL)
        pygame.display.set_caption("Your Game Title")

    def run(self):
        """
        Runs the main game loop.
        """

        running = True
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Update game logic
            self.delta_time = self.clock.tick() / 1000.0  # Update delta time in seconds
            self.update(self.delta_time)  # Pass delta_time to update method

            # Render the game
            self.render()

        pygame.quit()

    def update(self, delta_time):
        """
        Updates the game logic based on the given delta time.

        Args:
            delta_time (float): Time elapsed since the last update in seconds.
        """

        self.world.update(delta_time)
        self.player.update(delta_time, self.world.directional_light)
        self.physics.update(self.world, self.player)

    def render(self):
        """
        Renders the game scene.
        """

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        self.world.render(self.block_renderer)
        self.player.render()

        pygame.display.flip()

    def run(self):
        """
        Runs the main game loop.
        """

        running = True
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Update game logic
            self.delta_time = self.clock.tick() / 1000.0  # Update delta time in seconds
            self.update(self.delta_time)

            # Render the game
            self.render()

        pygame.quit()