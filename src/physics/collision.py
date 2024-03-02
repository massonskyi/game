from src.game.block import Block
from src.game.player import Player

class Collision:
    def __init__(self):
        pass

    def check_collision_with_blocks(self, player, world):
        player_position = player.get_position()
        player_size = player.get_size()

        for chunk in world.chunks:
            for block in chunk.blocks:
                if (
                    player_position[0] < block.position[0] + 1
                    and player_position[0] + player_size[0] > block.position[0]
                    and player_position[1] < block.position[1] + 1
                    and player_position[1] + player_size[1] > block.position[1]
                    and player_position[2] < block.position[2] + 1
                    and player_position[2] + player_size[2] > block.position[2]
                ):
                    # Collision detected, handle accordingly
                    return block

        # No collision detected
        return None
