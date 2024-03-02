from src.physics.collision import Collision
from src.game.player import Player

class Physics:
    def __init__(self):
        self.collision = Collision()
        self.gravity = -0.1  # Gravity acceleration
        self.jump_force = 0.3  # Jump force

    def update(self, world, player):
        # Update physics for the world and player (gravity, collisions, etc.)
        player.set_velocity(player.get_velocity()[0], player.get_velocity()[1] + self.gravity, player.get_velocity()[2])

        # Check and handle collisions in X and Z axes
        new_position = self.check_and_handle_collisions(player, world, player.get_position()[0] + player.get_velocity()[0], player.get_position()[1], player.get_position()[2] + player.get_velocity()[2])

        # Check and handle collisions in Y axis (gravity and jumping)
        new_position = self.check_and_handle_collisions(player, world, new_position[0], new_position[1] + player.get_velocity()[1], new_position[2])

        player.set_position(new_position)

    def check_and_handle_collisions(self, player, world, x, y, z):
        player_position = (x, y, z)
        collided_block = self.collision.check_collision_with_blocks(player, world, ignore_y=True)

        if collided_block is not None:
            if player.get_velocity()[0] > 0:
                player_position = (collided_block.position[0] - player.get_size()[0], player_position[1], player_position[2])
            elif player.get_velocity()[0] < 0:
                player_position = (collided_block.position[0] + 1, player_position[1], player_position[2])
            if player.get_velocity()[2] > 0:
                player_position = (player_position[0], player_position[1], collided_block.position[2] - player.get_size()[2])
            elif player.get_velocity()[2] < 0:
                player_position = (player_position[0], player_position[1], collided_block.position[2] + 1)

        if player.on_ground() and player.is_jumping():
            player.set_velocity(player.get_velocity()[0], self.jump_force, player.get_velocity()[2])

        return player_position
