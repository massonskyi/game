from src.game.chunk import Chunk
from src.rendering.block_renderer import BlockRenderer


class World:
    def __init__(self):
        self.chunks = []
        self.block_renderer = BlockRenderer()
        self.player_direction = Direction()  # Create a Direction object for player direction
        self.generate_chunks()
        self.directional_light = None

    def generate_chunks(self):
        # Generate chunks around the origin (0, 0, 0)
        for x in range(-1, 2):
            for z in range(-1, 2):
                chunk = Chunk((x * Chunk.CHUNK_SIZE, 0, z * Chunk.CHUNK_SIZE))
                self.chunks.append(chunk)

    def update(self, delta_time):
        for chunk in self.chunks:
            chunk.update(delta_time)  # Pass delta_time to chunk update

    def get_player_direction(self):
        """Returns the current direction of the player."""
        return self.player_direction

    def set_player_direction(self, direction):
        """Sets the player's direction."""
        if isinstance(direction, Direction):
            self.player_direction = direction
        else:
            raise TypeError("Player direction must be a Direction object")

    def render(self, block_renderer):
        for chunk in self.chunks:
            chunk.render(block_renderer)

    def set_directional_light(self, light_direction, light_color):
        """
        Sets the directional light properties.

        Args:
            light_direction (Direction): Direction of the light.
            light_color (tuple): Color of the light (e.g., (1.0, 1.0, 1.0) for white).
        """
        self.directional_light = (light_direction, light_color)


class Direction:
    """Represents a direction in 3D space."""

    def __init__(self, x=0, y=0, z=0):
        """
        Initializes a Direction object.

        Args:
            x (int, optional): X component of the direction vector. Defaults to 0.
            y (int, optional): Y component of the direction vector. Defaults to 0.
            z (int, optional): Z component of the direction vector. Defaults to 0.
        """

        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        """Provides a string representation of the direction."""
        return f"({self.x}, {self.y}, {self.z})"

    def __mul__(self, other):
        """Implements multiplication for Direction objects."""
        if isinstance(other, (int, float)):
            return Direction(self.x * other, self.y * other, self.z * other)
        else:
            raise TypeError("Can only multiply Direction by numbers")

    def __add__(self, other):
        """Implements addition for Direction objects."""
        if isinstance(other, Direction):
            return Direction(self.x + other.x, self.y + other.y, self.z + other.z)
        else:
            raise TypeError("Can only add Direction to another Direction")

    def get_direction(self):
        """Returns the direction of te direction."""

        return [self.x, self.y, self.z]

    def __getitem__(self, item):
        """
        Returns the direction by index or raises an IndexError if the index is out of range
        :param item:
        :return:
        """
        return [self.x, self.y, self.z][item]
