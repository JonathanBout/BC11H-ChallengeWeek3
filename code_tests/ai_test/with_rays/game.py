import pygame
import math

class Npc:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.font = pygame.font.Font(None, 24)
        self.text = self.font.render("", True, (255, 255, 255))
        self.prev_distance = None


    def draw_rays(self, window, rects):
        for angle in range(0, 360, 10):
            angle_rad = math.radians(angle)
            end_x = int(self.x + 1000 * math.cos(angle_rad))
            end_y = int(self.y + 1000 * math.sin(angle_rad))

            ray = pygame.draw.line(window, (0, 255, 0), (self.x, self.y), (end_x, end_y), 1)

            # Check for collisions with map rects
            min_distance = float('inf')
            intersection_point = None  # Initialize intersection_point
            for rect in rects:
                if ray.colliderect(rect):
                    intersection_points = ray.clipline(rect)
                    for point in intersection_points:
                        distance = math.hypot(point[0] - self.x, point[1] - self.y)
                        if distance < min_distance:
                            min_distance = distance
                            intersection_point = point

            # Draw the distance as an integer
            if intersection_point is not None:
                text = self.font.render(f"{int(min_distance)}", True, (255, 255, 255))
                text_rect = text.get_rect(topleft=(intersection_point[0] + 5, intersection_point[1] - 20))
                window.blit(text, text_rect.topleft)

            if intersection_point:
                distance = str(int(min_distance))
                self.text = self.font.render(distance, True, (255, 255, 255))

    def draw_player_circle(self, window):
        pygame.draw.circle(window, (255, 0, 0), (self.x, self.y), 10)

    def npc_run(self, window, rects):
        self.draw_rays(window, rects)
        self.draw_player_circle(window)


class Game:
    def __init__(self):
        pygame.init()  # Initialize pygame
        self.surface = pygame.display.set_mode((1280, 720))
        self.npc = Npc("Player2", 640, 360)
        self.controls_enabled = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()

    def run(self):
        self.handle_events()
        self.surface.fill((0, 0, 0))
        self.npc.npc_run(self.surface, [])  # Pass your rects list here
        pygame.display.flip()

    def start(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.run()

            pygame.time.delay(16)  # Add a small delay to control the frame rate

        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.start()
