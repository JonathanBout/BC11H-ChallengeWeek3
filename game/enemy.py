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
        self.target_point_index = 1
        self.map_offset = np.array(config.MAP_POSITION)
        self.current_position = np.array(self.map.waypoints[0])
        self.max_speed = max_speed
        self.screen = screen
        self.width, self.height = self.sprite.get_size()

    def update(self):
        self.map_offset = np.array(config.MAP_POSITION)

        current_offset_position = self.current_position + self.map_offset
        next_point = (
            np.array(self.map.waypoints[self.target_point_index]) + self.map_offset
        )

        in_between = current_offset_position - next_point

        move = normalize(in_between) * 10
        # direction[0] = -direction[0]
        self.current_position = self.current_position - move
        current_offset_position = current_offset_position - move

        pygame.draw.circle(self.screen, "green", next_point, 10, 10)
        pygame.draw.circle(self.screen, "purple", current_offset_position, 10, 10)
        pygame.draw.circle(
            self.screen, "yellow", self.current_position + self.map_offset, 10, 10
        )

        pygame.display.flip()

        if np.linalg.norm(in_between) < Enemy.NEXT_POINT_THRESHOlD:
            self.target_point_index += 1
            self.target_point_index %= len(self.map.waypoints)
        sprite_size = np.array(
            [config.PLAYER_SPRITE_WIDTH, config.PLAYER_SPRITE_HEIGHT]
        )
        self.screen.blit(
            self.prepare(normalize(-move)),
            Rect(
                *(current_offset_position - sprite_size),
                config.PLAYER_SPRITE_WIDTH,
                config.PLAYER_SPRITE_HEIGHT,
            ),
        )

    def prepare(self, move_direction: list[float]):
        game_image = self.sprite
        sprite_width = config.PLAYER_SPRITE_WIDTH
        sprite_height = config.PLAYER_SPRITE_HEIGHT
        num_sprites = game_image.get_width() // sprite_width
        right = move_direction[0] > 0.5
        left = move_direction[0] < -0.5
        down = move_direction[1] > 0.5
        up = move_direction[1] < -0.5
        frame = 0
        if down:
            if right or left:
                frame = 9
            else:
                frame = 11
        elif up:
            if right or left:
                frame = 3
            else:
                frame = 0
        elif right or left:
            frame = 7

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

        return self.check_flip(sprites[frame], left)

    def check_flip(self, player, horizontal_flip: bool):
        return pygame.transform.flip(player, flip_x=horizontal_flip, flip_y=False)


def normalize(v: list[int]):
    vx, vy = v
    n = math.sqrt(vx**2 + vy**2)
    f = min(n, 1) / n
    return np.array([f * vx, f * vy])
