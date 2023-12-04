import cv2
import numpy as np
import pygame
import math


class ImageProcessor:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((1280, 720))
        self.surface = pygame.Surface(self.window.get_size())

    def merge_rects(self, rects, threshold):
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
            "assets/sprites/rainbow_road_heat_map.png", 0
        )  # Confirm the image path is correct
        blurred = cv2.GaussianBlur(image, (13, 13), 0)
        return cv2.Canny(blurred, 10, 30), image

    def load_image(self, screen: pygame.Surface):
        edges, image = self.get_lines()

        contours, _ = cv2.findContours(
            edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        scale_x = self.window.get_width() / image.shape[1]
        scale_y = self.window.get_height() / image.shape[0]
        rects = [
            pygame.Rect(
                cv2.boundingRect(contour)[0] * scale_x,
                cv2.boundingRect(contour)[1] * scale_y,
                cv2.boundingRect(contour)[2] * scale_x,
                cv2.boundingRect(contour)[3] * scale_y,
            )
            for contour in contours
        ]

        threshold_distance = 40
        merged_rects = self.merge_rects(rects, threshold_distance)

        non_overlapping_rects = []

        for i in range(len(merged_rects) - 1):
            current = merged_rects[i]
            if current.collidelist(non_overlapping_rects) == -1:
                non_overlapping_rects.append(current)

        return self.simplify_rects(non_overlapping_rects, screen)

        # center_x = (
        #     sum(rect.center[0] for rect in merged_rects) / len(merged_rects) - 300
        # )
        # center_y = sum(rect.center[1] for rect in merged_rects) / len(merged_rects) - 20
        # def get_angle(rect):
        #     dx = rect.center[0] - center_x
        #     dy = rect.center[1] - center_y
        #     return math.atan2(dy, dx)
        # unsorted_rects = merged_rects[::]
        # # sorted_rects = sorted(merged_rects, key=get_angle)

        # sorted_rects =

    def simplify_rects(self, rects: list[pygame.Rect], screen: pygame.Surface):
        rects = [pygame.Rect(rect.left, rect.top, 50, 50) for rect in rects]

        STARTING_POINT = [60, 475]  # TODO: from config
        ordered_rects: list[pygame.Rect] = []
        rects_left = rects[::]
        last_position = STARTING_POINT
        screen.fill((0, 0, 0))
        pygame.draw.circle(screen, (255, 0, 0), STARTING_POINT, 5, 5)
        for i in range(len(rects)):
            closest: pygame.Rect = None
            closest_distance = 9999999
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
                pygame.time.delay(10)
            print("closest:", closest, "at distance: ", dist)
            if closest:
                pygame.draw.circle(screen, (0, 255, 0), closest.center, 20, 20)
                pygame.draw.line(
                    screen, (255 - i, 255 - i, 255 - i), closest.center, last_position
                )
                rects_left.remove(closest)
                ordered_rects.append(closest)
                last_position = closest.center
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

    def run(self):
        rects = self.load_image()
        self.draw(rects)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.window.fill((0, 0, 0))
            self.window.blit(self.surface, (0, 0))
            pygame.display.flip()
        pygame.quit()
