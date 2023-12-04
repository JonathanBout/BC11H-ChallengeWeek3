import math
import pygame
from rect_map import ImageProcessor
from ai import Npc


def get_direction(point1, point2):
    dx = point2[0] - point1[0]
    dy = point2[1] - point1[1]
    return dx > 0, dy > 0


def interpolate_points(start, end, num_points=10):
    return [
        (
            start[0] + (end[0] - start[0]) * t / num_points,
            start[1] + (end[1] - start[1]) * t / num_points,
        )
        for t in range(num_points + 1)
    ]


pygame.init()


class Game:
    def __init__(self):
        self.image_processor = ImageProcessor()
        self.window = pygame.display.set_mode((1280, 720))
        self.rect_map = self.image_processor.load_image(self.window)
        # self.player = pygame.Rect(50, 50, 100, 100)

        # ordered_path_points = [rect.center for rect in self.rect_map]
        # self.path_points = self.get_turn_points(ordered_path_points)

        # self.npc = Npc(self.rect_map, self.path_points)

        # self.rect_ids = {id(rect): rect for rect in self.rect_map}
        # self.player_touched_rects = set()

    # def get_turn_points(self, path):
    #     turn_points = [path[0]]  # Always start with the first point

    #     for rect in self.rect_map:
    #         turn_points.append(rect.center)

    #     turn_points.append(path[-1])  # Add the last point of the path

    #     return turn_points

    # def handle_collisions(self):
    #     if self.player.colliderect(self.npc.rect):
    #         print("Collision detected")

    # def draw(self):
    #     self.window.fill((0, 0, 0))
    #     pygame.draw.rect(self.window, (255, 0, 0), self.player)
    #     self.image_processor.draw(self.rect_map)
    #     for rect in self.rect_map:
    #         rect_id = id(rect)
    #         if rect_id in self.player_touched_rects:
    #             color = (
    #                 (0, 255, 0)
    #                 if rect_id in self.player_touched_rects
    #                 or self.npc.rect.colliderect(rect)
    #                 else (255, 0, 0)
    #             )
    #             pygame.draw.rect(self.window, color, rect, 1)

    #     pygame.draw.rect(
    #         self.window, (0, 0, 255), self.rect_map[self.npc.target_point_index], 5
    #     )

    #     # Drawing path points as small cyan circles
    #     for point in self.path_points:
    #         pygame.draw.circle(self.window, (0, 255, 255), point, 5)

    #     pygame.draw.rect(self.window, (0, 255, 0), self.npc.rect)
    #     pygame.display.flip()

    # def handle_npc_movement(self):
    #     self.npc.update()

    #     npc_rect_id = id(self.npc.rect)
    #     if npc_rect_id not in self.player_touched_rects:
    #         self.player_touched_rects.add(npc_rect_id)

    #     # Skip collision check for the first few updates
    #     for rect in self.rect_map:
    #         if (
    #             self.npc.rect.colliderect(rect)
    #             and id(rect) not in self.player_touched_rects
    #         ):
    #             self.player_touched_rects.add(id(rect))

    # def run(self):
    #     running = True
    #     while running:
    #         self.draw()

    #         # self.handle_collisions()

    #         for rect in self.rect_map:
    #             if (
    #                 self.player.colliderect(rect)
    #                 and id(rect) not in self.player_touched_rects
    #             ):
    #                 self.player_touched_rects.add(id(rect))

    #         # self.handle_npc_movement()

    #         for event in pygame.event.get():
    #             if event.type == pygame.QUIT:
    #                 running = False

    #         pygame.time.delay(100)

    #     pygame.quit()

    def run(self):
        clock = pygame.time.Clock()
        for rect in self.rect_map:
            print(rect)
            pygame.draw.rect(self.window, (255, 0, 0), rect, 5)
            pygame.display.flip()
            pygame.event.pump()
            clock.tick(2)

if __name__ == "__main__":
    game = Game()
    game.run()
