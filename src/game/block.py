from typing import Tuple, Union


class Block:
    """Represents a block in the game world."""

    def __init__(
            self,
            position: Tuple[int, int, int],
            texture: str,
            hardness: Union[int, float] = 1,
            light_level: int = 0,
    ):
        """
        Initializes a Block object.

        Args:
            position (Tuple[int, int, int]): X, Y, and Z coordinates of the block.
            texture (str): Path to the texture image file.
            hardness (Union[int, float], optional): How difficult it is to break the block. Defaults to 1.
            light_level (int, optional): Amount of light emitted by the block (0-15). Defaults to 0.
        """

        self.position = position
        self.texture = texture
        self.hardness = hardness
        self.light_level = light_level

        if not isinstance(position, tuple):
            raise TypeError("Position must be a tuple of (x, y, z) integers")
        if not isinstance(hardness, (int, float)):
            raise TypeError("Hardness must be a number")
        if light_level < 0 or light_level > 15:
            raise ValueError("Light level must be between 0 and 15")

    def get_position(self) -> Tuple[int, int, int]:
        """Returns the block's position as a tuple."""
        return self.position

    def get_texture(self) -> str:
        """Returns the path to the block's texture."""
        return self.texture

    def set_texture(self, texture: str):
        """Sets the path to the block's texture."""
        self.texture = texture

    def get_hardness(self) -> Union[int, float]:
        """Returns the block's hardness."""
        return self.hardness

    def set_hardness(self, hardness: Union[int, float]):
        """Sets the block's hardness."""
        if not isinstance(hardness, (int, float)):
            raise TypeError("Hardness must be a number")
        self.hardness = hardness

    def get_light_level(self) -> int:
        """Returns the block's light level."""
        return self.light_level

    def set_light_level(self, light_level: int):
        """Sets the block's light level (0-15)."""
        if light_level < 0 or light_level > 15:
            raise ValueError("Light level must be between 0 and 15")
        self.light_level = light_level

    def __str__(self):
        """Provides a string representation of the Block."""
        return f"Block(position={self.position}, texture={self.texture}, hardness={self.hardness}, light_level={self.light_level})"
