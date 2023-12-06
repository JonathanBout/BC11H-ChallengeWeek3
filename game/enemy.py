import pygame
from game.map_manager import MapConfig
from game import config
import numpy as np
import math
from random import randint
from pygame import Surface, Rect, image

from game.player import PlayerBase
from util.eventHandler import EventManager, FinishEvent, RespawnEvent

NEXT_POINT_THRESHOlD = 20
MAX_RANDOM_OFFSET = 50


class Enemy(PlayerBase):
    def __init__(self, map: MapConfig, sprite: str, screen: Surface, max_speed=100):
        self.map = map
        self.sprite = image.load(sprite)
        self.target_point_index = 1
        self.map_offset = np.array(config.MAP_POSITION)
        self.current_position = np.array(self.map.waypoints[0])
        self.max_speed = max_speed
        self.screen = screen
        self.width, self.height = self.sprite.get_size()
        self.speed = 0.0
        self.finish_event = FinishEvent(self.screen, [0, 0], config.FINISH_SOUND)
        self.current_lap = 0

    def update(self):
        if self.speed < self.max_speed:
            fps = config.MAX_FPS if config.CURRENT_FPS == 0 else config.CURRENT_FPS
            self.speed += self.max_speed / (fps)  # 5 seconds to reach full speed

        self.map_offset = np.array(config.MAP_POSITION)

        current_offset_position = self.current_position + self.map_offset
        next_point = (
            np.array(self.map.waypoints[self.target_point_index]) + self.map_offset
        )

        in_between = (
            current_offset_position
            - next_point
            + np.array(
                [
                    randint(-MAX_RANDOM_OFFSET, MAX_RANDOM_OFFSET),
                    randint(-MAX_RANDOM_OFFSET, MAX_RANDOM_OFFSET),
                ]
            )
        )

        move = normalize(in_between) * self.speed * config.SECONDS_PER_FRAME

        self.current_position = self.current_position - move
        current_offset_position = current_offset_position - move

        pygame.draw.circle(self.screen, "green", next_point, 10, 10)
        pygame.draw.circle(self.screen, "purple", current_offset_position, 10, 10)
        pygame.draw.circle(
            self.screen, "yellow", self.current_position + self.map_offset, 10, 10
        )

        if np.linalg.norm(in_between) < NEXT_POINT_THRESHOlD:
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

        self.check_for_events(self.screen, current_offset_position - sprite_size)

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

    def check_for_events(self, screen: Surface, current_position: list[int, int]):
        # Create finish event
        self.finish_event.player_position = current_position
        self.finish_event.screen = screen

        self.current_lap = self.finish_event.manual_trigger(self.current_lap)

        if self.current_lap > config.RACE_LAPS:
            pygame.event.post(pygame.event.Event(config.ENEMY_WON_EVENT))


def normalize(v: list[int]):
    vx, vy = v

    result: list[int]

    if vx == 0:
        result = [0, 1]
    elif vy == 0:
        result = [1, 0]
    else:
        n = math.sqrt(vx**2 + vy**2)
        f = min(n, 1) / n
        result = [f * vx, f * vy]
    return np.array(result)
