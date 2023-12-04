import cv2
import numpy as np
import pygame
import math


class ImageProcessor:
    def __init__(
        self, map_size: list[int, int], map_scale: int, screen: pygame.Surface
    ):
        pygame.init()
        self.map_width = map_size[0]
        self.map_height = map_size[1]
        self.map_scale = map_scale
        self.window = screen

    def merge_rects(self, rects: list[pygame.Rect], threshold: int):
        merged_rects = []
        while rects:
            main_rect = rects.pop(0)
            close_rects = [
                rect
                for rect in rects
                if np.linalg.norm(np.array(main_rect.center) - np.array(rect.center))
                < threshold
            ]
            for rect in close_rects:
                rects.remove(rect)
            x_values = [r.x for r in close_rects + [main_rect]]
            y_values = [r.y for r in close_rects + [main_rect]]
            last_values_x = [r.x + r.width for r in close_rects + [main_rect]]
            last_values_y = [r.y + r.height for r in close_rects + [main_rect]]
            x_min = min(x_values)
            y_min = min(y_values)
            width = max(last_values_x) - x_min
            height = max(last_values_y) - y_min
            merged_rects.append(pygame.Rect(x_min, y_min, width, height))
        return merged_rects

    def get_lines(self):
        image = cv2.imread(
            "assets/sprites/rainbow_road_heat_map.png", cv2.IMREAD_GRAYSCALE
        )  # Confirm the image path is correct
        blurred = cv2.GaussianBlur(image, (9, 9), 0)
        return cv2.Canny(blurred, 200, 400), image

    def load_image(self, screen: pygame.Surface):
        edges, image = self.get_lines()

        contours, _ = cv2.findContours(
            edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        scale_x = self.map_width / image.shape[1]
        scale_y = self.map_height / image.shape[0]
        rects = [
            pygame.Rect(
                cv2.boundingRect(contour)[0] * scale_x,
                cv2.boundingRect(contour)[1] * scale_y,
                cv2.boundingRect(contour)[2] * scale_x,
                cv2.boundingRect(contour)[3] * scale_y,
            )
            for contour in contours
        ]

        threshold_distance = 20 * self.map_scale
        merged_rects = self.merge_rects(rects, threshold_distance)

        non_overlapping_rects = []

        for i in range(len(merged_rects) - 1):
            current = merged_rects[i]
            if current.collidelist(non_overlapping_rects) == -1:
                non_overlapping_rects.append(current)

        return self.simplify_rects(non_overlapping_rects, screen)

    def simplify_rects(self, rects: list[pygame.Rect], screen: pygame.Surface):
        rects = [pygame.Rect(rect.left, rect.top, 70, 70) for rect in rects]
        STARTING_POINT = [60, 475]  # TODO: from config
        ordered_rects: list[pygame.Rect] = []
        rects_left = rects[::]
        last_position = STARTING_POINT
        screen.fill((0, 0, 0))
        pygame.draw.circle(screen, (255, 0, 0), STARTING_POINT, 5, 5)
        for i in range(len(rects)):
            closest: pygame.Rect = None
            closest_distance = 9999999
            potential_closest: pygame.Rect = None
            for rect in rects_left:
                dist = self.calculate_distance(rect, last_position)
                if dist < closest_distance:
                    closest = rect
                    closest_distance = dist
                    pygame.draw.circle(screen, (0, 0, 255), rect.center, 5, 5)
                pygame.draw.rect(
                    screen,
                    "yellow",
                    rect,
                    2,
                )
                pygame.draw.line(screen, (10, 10, 10), rect.center, last_position)
                pygame.display.flip()
                # pygame.time.delay(10)
            print("closest:", closest, "at distance: ", dist)
            if (not closest) and potential_closest:
                closest = potential_closest
            if closest:
                if i > 10 and math.dist(
                    last_position, ordered_rects[0].center
                ) < math.dist(last_position, closest.center):
                    # if close to starting point, early return
                    return ordered_rects

                rects_left.remove(closest)
                last_position = closest.center
                if closest.collidelist(ordered_rects) == -1:
                    ordered_rects.append(closest)
                    pygame.draw.circle(screen, (0, 255, 0), closest.center, 20, 20)
                    pygame.draw.line(
                        screen,
                        (255 - i, 255 - i, 255 - i),
                        closest.center,
                        last_position,
                    )
                    pygame.display.flip()
            else:
                return ordered_rects

        return [pygame.Rect(*rect.topleft, 100, 100) for rect in ordered_rects]

    def calculate_distance(self, rect: pygame.Rect, point: list[int]):
        return math.dist(rect.center, point)

    def draw(self, rects: list[str]):
        step = 255 // len(rects)
        index = 0
        rect_temp = rects[::-1]
        for rect in rect_temp:
            index += step
            pygame.draw.rect(self.window, (index, index, index), rect)
