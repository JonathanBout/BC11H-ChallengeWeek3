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


# Window width
SCREEN_WIDTH = 1280

# Window height
SCREEN_HEIGHT = 720

SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

MAP_SCALEUP = 1


class Game:
    def __init__(self):
        pygame.init()
        map_size = (SCREEN_WIDTH * MAP_SCALEUP, SCREEN_HEIGHT * MAP_SCALEUP)
        self.window = pygame.display.set_mode(SCREEN_SIZE)
        self.image_processor = ImageProcessor(map_size, MAP_SCALEUP, self.window)
        self.rect_map = self.image_processor.load_image(self.window)
        self.npc = Npc(self.rect_map)
        map = pygame.image.load("assets/sprites/rainbow_road_map.png")
        self.map = pygame.transform.scale(map, map_size)

    def draw(self):
        self.window.fill("black")
        self.window.blit(self.map, (0, 0))
        for rect in self.rect_map:
            pygame.draw.rect(self.window, (255, 255, 255), rect, 5 * MAP_SCALEUP)
        pygame.draw.rect(self.window, (255, 0, 0), self.npc.rect)
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            self.npc.do_movement()
            self.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            pygame.time.delay(100)

        pygame.quit()

    # def run(self):
    #     clock = pygame.time.Clock()
    #     for rect in self.rect_map:
    #         print(rect)
    #         pygame.draw.rect(self.window, (255, 0, 0), rect, 5)
    #         pygame.display.flip()
    #         pygame.event.pump()
    #         clock.tick(2)


if __name__ == "__main__":
    game = Game()
    game.run()
