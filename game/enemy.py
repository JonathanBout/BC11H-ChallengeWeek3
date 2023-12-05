import pygame
from game.map_manager import MapConfig
from game import config
import numpy as np
import math
from pygame import Surface, Rect, image

from game.player import PlayerBase


class Enemy(PlayerBase):
    NEXT_POINT_THRESHOlD = 20

    def __init__(self, map: MapConfig, sprite: str, screen: Surface, max_speed=300):
        self.map = map
        self.sprite = image.load(sprite)
        self.target_point_index = 0
        self.current_position = np.array(self.map.waypoints[0])
        self.max_speed = max_speed
        self.screen = screen
        self.width, self.height = self.sprite.get_size()

    def update(self):
        map_position = np.array(config.MAP_POSITION)

        next_point = (
            np.array(self.map.waypoints[self.target_point_index]) + map_position
        )

        current_point = np.array(
            self.current_position
            + map_position
            - np.array([self.width / 2, self.height / 2])
        )
        # last_point = np.array(self.map.waypoints[self.current_point_index])

        direction = np.array(normalize(next_point - current_point))
        move = np.array(direction * self.max_speed)

        self.current_position = np.array(
            [self.current_position[0] + move[0], self.current_position[1] + move[1]]
        )

        if abs(np.linalg.norm(current_point - next_point)) < self.NEXT_POINT_THRESHOlD:
            self.target_point_index += 1
            self.target_point_index %= len(self.map.waypoints)

        self.screen.blit(self.prepare(direction), Rect(*current_point, self.width, self.height))

        print(current_point)

    def prepare(self, move_direction: list[float]):
        game_image = self.sprite
        sprite_width = config.PLAYER_SPRITE_WIDTH
        sprite_height = config.PLAYER_SPRITE_HEIGHT
        num_sprites = game_image.get_width() // sprite_width
        up = move_direction[1] < 0
        frame = 0
        if -1 < move_direction[0] < 1:
            if not up:
                frame = num_sprites - 1
        else:
            if up:
                frame = 3
            elif abs(move_direction[1]) < 1:
                frame = 7
            else:
                frame = 9

        sprites = []
        for i in range(num_sprites):
            sprite_x = i * sprite_width
            sprite = game_image.subsurface(
                pygame.Rect((sprite_x, 0, sprite_width, sprite_height))
            )
            sprite = pygame.transform.scale(
                sprite,
                (
                    sprite_width * config.PLAYER_SPRITE_SCALE,
                    sprite_height * config.PLAYER_SPRITE_SCALE,
                ),
            )
            sprites.append(sprite)

        return self.check_flip(sprites[frame], move_direction[0])

    def check_flip(self, player, x_movement: int):
        return pygame.transform.flip(player, flip_x=x_movement < 0, flip_y=False)


def normalize(v: list[int]):
    vx, vy = v
    n = math.sqrt(vx**2 + vy**2)
    f = min(n, 1) / n
    return [f * vx, f * vy]
