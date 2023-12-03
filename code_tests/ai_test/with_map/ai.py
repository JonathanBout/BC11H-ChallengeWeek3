import random

import pygame
import math


class Npc:
    def __init__(self, rect_map, path_points):
        if not path_points:
            raise ValueError("path_points cannot be empty")
        try:
            self.rect = pygame.Rect((path_points[0][0] - 25, path_points[0][1] - 25), (50, 50))
        except IndexError:
            raise ValueError("path_points does not contain enough elements")

        self.rect_map = rect_map
        self.path = path_points
        self.target_point_index = 0
        self.speed = 8

    def update(self):
        target_point = self.path[self.target_point_index]
        dx = target_point[0] - self.rect.x
        dy = target_point[1] - self.rect.y
        dist = math.hypot(dx, dy)

        # Use a smaller step size to follow the path more closely.
        step_size = min(self.speed, dist)

        if dist != 0:
            dx /= dist  # Normalize
            dy /= dist  # Normalize
            self.rect.x += dx * step_size
            self.rect.y += dy * step_size

        if dist <= step_size:
            self.target_point_index = (self.target_point_index + 1) % len(self.path)

        self.check_track()

    def move_towards(self, target_point, speed):
        dx = target_point[0] - self.rect.x
        dy = target_point[1] - self.rect.y
        dist = math.hypot(dx, dy)

        if dist != 0:
            correction = 0.1  # set your own correction value
            dx = (dx / dist) + correction * (dx / dist)
            dy = (dy / dist) + correction * (dy / dist)

            # Normalize the resultant vector
            resultant_dist = math.hypot(dx, dy)
            dx /= resultant_dist
            dy /= resultant_dist

            self.rect.x += dx * speed
            self.rect.y += dy * speed

    def check_track(self):
        if not any(rect.colliderect(self.rect) for rect in self.rect_map):
            nearest_point_index = self.get_nearest_point_index()
            if nearest_point_index != self.target_point_index:
                np = self.path[nearest_point_index]
                dist_to_nearest = math.hypot(self.rect.x - np[0], self.rect.y - np[1])
                speed = self.speed

                if dist_to_nearest > 100:  # choose your own distance threshold
                    speed = self.speed * 2  # speed is twice as fast if distance is more than threshold

                self.move_towards(self.path[nearest_point_index], speed)

    def get_nearest_point_index(self):
        npc_center = self.rect.center
        # Calculate the distances to the path points
        distances = [math.hypot(npc_center[0] - point[0], npc_center[1] - point[1]) for point in self.path]
        # Return the index of the nearest path point
        return distances.index(min(distances))