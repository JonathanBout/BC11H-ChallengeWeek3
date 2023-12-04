import random
import numpy as np
import pygame
import math


DISTANCE_THRESHOLD = 20


class Npc:
    def __init__(self, rect_map: list[pygame.Rect]):
        self.rect_map = rect_map
        self.speed = 8
        self.rect = rect_map[0]
        self.last_point_index = 0
        self.next_point_index = 1

    def do_movement(self) -> pygame.Rect:
        target = self.rect_map[self.next_point_index]
        if (math.dist(target.center, self.rect.center)) < DISTANCE_THRESHOLD:
            self.next_point_index += 1
            self.last_point_index += 1
            self.next_point_index %= len(self.rect_map)
            self.last_point_index %= len(self.rect_map)
            print("new target:", self.get_points()[1])
        next_move = self.get_next_move()
        self.rect = pygame.Rect(
            self.rect.left - next_move[0], self.rect.top - next_move[1], *self.rect.size
        )
        return self.rect

    def get_next_move(self):
        next_point, last_point = self.get_points()

        return next_point - last_point

    def get_points(self):
        next_point = np.array(self.rect_map[self.next_point_index].center)
        last_point = np.array(self.rect_map[self.last_point_index].center)
        return last_point, next_point
