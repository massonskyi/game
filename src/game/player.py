import math

import numpy as np
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from src.game.block import Block
from src.game.chunk import Chunk


class Player:
    def __init__(self, position, direction):
        self.position = position
        self.rotation = (0, 0)
        self.movement_speed = 0.1
        self.size = (0.6, 1.8, 0.6)
        self.jumping = False
        self.on_ground = False
        self.velocity = (0, 0, 0)
        self.camera_distance = 5
        self.camera_pitch = 0
        self.camera_yaw = 0
        self.direction = direction
        self.speed = 0.1

    def update(self, delta_time, world):
        if self.jumping and self.on_ground:
            self.jumping = False
            self.on_ground = False
            self.velocity = (self.velocity[0], 0.3, self.velocity[2])

        # Update position based on direction and speed
        new_position = (
            self.position[0] + self.direction.get_player_direction().get_direction() * self.speed * delta_time,
            self.position[1] + self.direction.get_player_direction().get_direction() * self.speed * delta_time,
            self.position[2] + self.direction.get_player_direction().get_direction() * self.speed * delta_time
        )

        is_blocked = False
        for chunk in world.chunks:
            chunk_x = int(new_position[0] - chunk.position[0])
            chunk_y = int(new_position[1] - chunk.position[1])
            chunk_z = int(new_position[2] - chunk.position[2])

            # Check if the new position is within the chunk boundaries
            if 0 <= chunk_x < Chunk.CHUNK_SIZE and 0 <= chunk_y < Chunk.CHUNK_SIZE and 0 <= chunk_z < Chunk.CHUNK_SIZE:
                block = chunk.get_block(chunk_x, chunk_y, chunk_z)
                if block is not None:  # Check if a block exists at that position
                    is_blocked = True
                    break

        if not is_blocked:
            self.position = new_position

        keys = pygame.key.get_pressed()
        if keys[K_w]:
            self.position += (0, 0, -self.speed * delta_time)
        if keys[K_s]:
            self.position += (0, 0, self.speed * delta_time)
        if keys[K_a]:
            self.position += (-self.speed * delta_time, 0, 0)
        if keys[K_d]:
            self.position += (self.speed * delta_time, 0, 0)

    def move(self, direction):
        x, z = direction
        dx = math.cos(self.rotation[1]) * x - math.sin(self.rotation[1]) * z
        dz = math.sin(self.rotation[1]) * x + math.cos(self.rotation[1]) * z
        self.position = (self.position[0] + dx * self.movement_speed, self.position[1], self.position[2] + dz * self.movement_speed)

    def get_size(self):
        return self.size

    def is_jumping(self):
        return self.jumping

    def set_jumping(self, jumping):
        self.jumping = jumping

    def on_ground(self):
        return self.on_ground

    def set_on_ground(self, on_ground):
        self.on_ground = on_ground

    def get_position(self):
        return self.position

    def set_position(self, position):
        self.position = position

    def get_velocity(self):
        return self.velocity

    def set_velocity(self, velocity):
        self.velocity = velocity

    def rotate(self, d_pitch, d_yaw):
        self.rotation = (self.rotation[0] + d_pitch, self.rotation[1] + d_yaw)

    def get_view_matrix(self):
        pitch = math.radians(self.camera_pitch)
        yaw = math.radians(self.camera_yaw)

        front = np.array([
            math.cos(pitch) * math.cos(yaw),
            math.sin(pitch),
            math.cos(pitch) * math.sin(yaw)
        ])
        front = np.normalize(front)

        right = np.cross(np.array([0, 1, 0]), front)
        right = np.normalize(right)

        up = np.cross(front, right)

        view_matrix = np.identity(4)
        view_matrix[:3, 0] = right
        view_matrix[:3, 1] = up
        view_matrix[:3, 2] = -front
        view_matrix[:3, 3] = self.position

        return view_matrix

    def interact_with_world(self, world, action, block_type=None):
        reach = 5.0
        x, y, z = self.position

        # Calculate the ray direction based on the camera's view matrix
        view_matrix = self.get_view_matrix()
        ray_direction = np.dot(view_matrix[:3, 2], np.linalg.inv(view_matrix)[:3, :3])

        # Normalize the ray direction
        ray_direction = ray_direction / np.linalg.norm(ray_direction)

        # Calculate the target point
        target_point = self.position + ray_direction * reach

        # Check if the target point intersects with any blocks in the world
        intersected_block = None
        for chunk in world.chunks:
            if chunk.position[0] <= target_point[0] <= chunk.position[0] + Chunk.CHUNK_SIZE and \
                    chunk.position[1] <= target_point[1] <= chunk.position[1] + Chunk.CHUNK_SIZE and \
                    chunk.position[2] <= target_point[2] <= chunk.position[2] + Chunk.CHUNK_SIZE:

                chunk_x = int(target_point[0] - chunk.position[0])
                chunk_y = int(target_point[1] - chunk.position[1])
                chunk_z = int(target_point[2] - chunk.position[2])

                intersected_block = chunk.get_block(chunk_x, chunk_y, chunk_z)
                if intersected_block is not None:
                    break

        if intersected_block is not None:
            if action == 'break':
                # Remove the block from the chunk
                chunk.set_block(chunk_x, chunk_y, chunk_z, Block((chunk_x, chunk_y, chunk_z), 'air'))
            elif action == 'place' and block_type is not None:
                # Add the new block to the chunk
                chunk.set_block(chunk_x, chunk_y, chunk_z, Block((chunk_x, chunk_y, chunk_z), block_type))

