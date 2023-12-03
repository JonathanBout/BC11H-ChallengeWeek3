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
            close_rects = [rect for rect in rects if
                           np.linalg.norm(np.array(main_rect.center) - np.array(rect.center)) < threshold]
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

    def load_image(self):
        image = cv2.imread('../../../assets/sprites/rainbow_road_heat_map.png', 0)  # Confirm the image path is correct
        blurred = cv2.GaussianBlur(image, (13, 13), 0)
        edges = cv2.Canny(blurred, 10, 30)
        contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        scale_x = self.window.get_width() / image.shape[1]
        scale_y = self.window.get_height() / image.shape[0]
        rects = [pygame.Rect(cv2.boundingRect(contour)[0] * scale_x, cv2.boundingRect(contour)[1] * scale_y,
                             cv2.boundingRect(contour)[2] * scale_x, cv2.boundingRect(contour)[3] * scale_y) for contour
                 in
                 contours]
        threshold_distance = 80
        merged_rects = self.merge_rects(rects, threshold_distance)

        center_x = sum(rect.center[0] for rect in merged_rects) / len(merged_rects) - 300
        center_y = sum(rect.center[1] for rect in merged_rects) / len(merged_rects) - 20

        def get_angle(rect):
            dx = rect.center[0] - center_x
            dy = rect.center[1] - center_y
            return math.atan2(dy, dx)

        sorted_rects = sorted(merged_rects, key=get_angle)

        return sorted_rects

    def draw(self, rects):
        for rect in rects:
            pygame.draw.rect(self.window, (255, 255, 255), rect)

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


if __name__ == '__main__':
    processor = ImageProcessor()
    processor.run()