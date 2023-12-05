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

        current_point = np.array(self.current_position + map_position - np.array([self.width / 2, self.height / 2]))
        # last_point = np.array(self.map.waypoints[self.current_point_index])

        direction = np.array(normalize(next_point - current_point))
        move = np.array(direction * self.max_speed)

        self.current_position = np.array(
            [self.current_position[0] + move[0], self.current_position[1] + move[1]]
        )

        if abs(np.linalg.norm(current_point - next_point)) < self.NEXT_POINT_THRESHOlD:
            self.target_point_index += 1
            self.target_point_index %= len(self.map.waypoints)

        self.screen.blit(
            self.prepare(), Rect(*current_point, self.width, self.height)
        )

        print(current_point)


def normalize(v: list[int]):
    vx, vy = v
    n = math.sqrt(vx**2 + vy**2)
    f = min(n, 1) / n
    return [f * vx, f * vy]
