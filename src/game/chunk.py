import numpy as np
from OpenGL.GL import glGetFloatv
from OpenGL.raw.GL.VERSION.GL_1_0 import GL_MODELVIEW_MATRIX, glLoadMatrixf, glPushMatrix, glPopMatrix

from src.game.block import Block
from src.rendering.shader import Shader


class Chunk:
    """Represents a chunk of the game world."""

    CHUNK_SIZE = 16

    def __init__(self, position):
        """
        Initializes a Chunk object.

        Args:
            position (Tuple[int, int, int]): X, Y, and Z coordinates of the chunk's origin.
        """

        self.position = position
        self.blocks = self.generate_blocks()

    def generate_blocks(self):
        """
        Generates blocks for the chunk using basic procedural noise.

        This method uses NumPy's random number generator for a basic noise
        generation approach. You can replace this with more sophisticated noise
        libraries or techniques for enhanced terrain generation.

        Returns:
            List[Block]: A list of Block objects representing the terrain in the chunk.
        """

        blocks = []
        scale = 10
        octaves = 6
        persistence = 0.5
        lacunarity = 2.0

        for x in range(self.CHUNK_SIZE):
            for y in range(self.CHUNK_SIZE):
                for z in range(self.CHUNK_SIZE):
                    noise_value = generate_noise(
                        x / scale,
                        y / scale,
                        z / scale,
                        octaves=octaves,
                        persistence=persistence,
                        lacunarity=lacunarity,
                    )
                    block_type = self.determine_block_type(noise_value)
                    block = Block((x, y, z), block_type)
                    blocks.append(block)
        return blocks

    def determine_block_type(self, noise_value):
        """
        Maps the noise value to a block type based on thresholds.

        You can adjust the thresholds and block types to create different terrain patterns.

        Args:
            noise_value (float): Noise value between 0 and 1.

        Returns:
            str: The type of block based on the noise value (e.g., "air", "dirt", "stone").
        """

        if noise_value > 0.6:
            return "stone"
        elif noise_value > 0.4:
            return "dirt"
        else:
            return "air"

    def update(self, delta_time):
        """
        Updates the chunk based on game logic and time passed.

        This is a placeholder for potential updates like gravity, block interactions,
        or dynamic changes in the environment.

        Args:
            delta_time (float): Time elapsed since the last update in seconds.
        """

        # Implement your update logic here (e.g., block physics, particle effects)
        pass

    def render(self, block_renderer):
        """
        Renders the blocks in the chunk using the provided block renderer.

        Args:
            block_renderer (BlockRenderer): An object responsible for rendering blocks.
        """

        for block in self.blocks:
            # Get the current modelview matrix
            model_matrix = glGetFloatv(GL_MODELVIEW_MATRIX)

            # Create a translation matrix using the block's position
            translation_matrix = np.array([
                [1, 0, 0, block.get_position()[0]],
                [0, 1, 0, block.get_position()[1]],
                [0, 0, 1, block.get_position()[2]],
                [0, 0, 0, 1]
            ])

            # Multiply the current modelview matrix by the translation matrix
            model_matrix = np.matmul(model_matrix, translation_matrix)

            # Convert the model matrix to GLfloat before loading
            model_matrix = model_matrix.astype(np.float32)

            # Load the new model matrix
            glLoadMatrixf(model_matrix)
            glPushMatrix()  # Push the matrix to avoid side effects

            # Render the block
            block_renderer.render_block(block, model_matrix)

            glPopMatrix()  # Pop the matrix after rendering

    def get_block(self, x, y, z):
        """
        Retrieves the block at the specified coordinates within the chunk.

        Args:
            x (int): X coordinate within the chunk (0-15).
            y (int): Y coordinate within the chunk (0-15).
            z (int): Z coordinate within the chunk (0-15).

        Returns:
            Block: The block object at the specified coordinates, or None if out of bounds.
        """

        if 0 <= x < self.CHUNK_SIZE and 0 <= y < self.CHUNK_SIZE and 0 <= z < self.CHUNK_SIZE:
            index = x + y * self.CHUNK_SIZE + z * self.CHUNK_SIZE * self.CHUNK_SIZE
            return self.blocks[index]
        else:
            return None

    def set_block(self, x, y, z, block):
        """
        Sets the block at the specified coordinates within the chunk.

        Args:
            x (int): X coordinate within the chunk (0-15).
            y (int): Y coordinate within the chunk (0-15).
            z (int): Z coordinate within the chunk (0-15).
            block (Block): The Block object to set at the specified coordinates.

        Raises:
            ValueError: If the provided coordinates are out of bounds or the block is not a Block object.
        """

        if not isinstance(block, Block):
            raise ValueError("block must be a Block object")

        if 0 <= x < self.CHUNK_SIZE and 0 <= y < self.CHUNK_SIZE and 0 <= z < self.CHUNK_SIZE:
            index = x + y * self.CHUNK_SIZE + z * self.CHUNK_SIZE * self.CHUNK_SIZE
            self.blocks[index] = block

            # Optional: Update neighboring blocks or chunk data as needed
            # based on the block change (e.g., gravity, light propagation)

        else:
            raise ValueError("Coordinates are out of bounds")


def generate_noise(x, y, z, scale=1, octaves=6, persistence=0.5, lacunarity=2.0):
  """
  Generates a simple noise value using NumPy's random number generator.

  This function implements a basic noise generation approach that is not equivalent to Perlin noise
  provided by libraries like `pynoise`. It can be used as a starting point for further customization
  or exploration of alternative noise generation techniques.

  Args:
      x: X coordinate.
      y: Y coordinate.
      z: Z coordinate.
      scale: Scale factor for the noise (default: 1).
      octaves: Number of octaves for the noise (more octaves increase detail, default: 6).
      persistence: Persistence of the noise (higher means more roughness, default: 0.5).
      lacunarity: Lacunarity of the noise (higher means more stretched features, default: 2.0).

  Returns:
      A noise value between 0 and 1.
  """

  # Normalize coordinates
  x /= scale
  y /= scale
  z /= scale

  # Initialize noise value (using random number between 0 and 1)
  noise_value = np.random.rand()

  # Iterate over octaves (replace with Perlin noise implementation for a more accurate approach)
  for i in range(octaves):
    # Increase frequency and decrease amplitude for each octave
    frequency = 2**i
    amplitude = persistence**i

    # Sample noise using simple linear interpolation (replace with Perlin noise function)
    noise_sample = (np.random.rand() + np.random.rand()) / 2

    # Add noise to the total noise value with scaled amplitude
    noise_value += noise_sample * amplitude

  return noise_value