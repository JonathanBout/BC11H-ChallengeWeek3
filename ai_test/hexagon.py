# Import necessary modules
import pygame
from pygame.locals import *
import random

# Initialize Pygame
pygame.init()

# Define global constants
WIDTH = 800
HEIGHT = 600
FPS = 60

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)


# Create the Point class
class Point(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 5))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# Create the Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, target_point_index=0):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH)
        self.rect.y = random.randint(0, HEIGHT)
        self.target_point_index = target_point_index

    def update_target_point_index(self):
        self.target_point_index = (self.target_point_index + 1) % len(AI.path_points)


# Create the Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH / 2
        self.rect.y = HEIGHT / 2

    def update(self):
        # Update player state based on user input
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            self.rect.x -= 5
        if keys[K_RIGHT]:
            self.rect.x += 5
        if keys[K_UP]:
            self.rect.y -= 5
        if keys[K_DOWN]:
            self.rect.y += 5


# Create the AI class
# Create the AI class
class AI:
    # Determine hexagon dimensions and margins
    horizontal_margin = 150
    vertical_margin = 75
    third_width = (WIDTH - 2 * horizontal_margin) / 3
    half_height = (HEIGHT - 2 * vertical_margin) / 2

    # Now, create the points that form the hexagon
    path_points = [
        (horizontal_margin + third_width, vertical_margin),  # Top left point
        (horizontal_margin + 2 * third_width, vertical_margin),  # Top right point
        (WIDTH - horizontal_margin, HEIGHT / 2),  # Middle right point
        (horizontal_margin + 2 * third_width, HEIGHT - vertical_margin),  # Bottom right point
        (horizontal_margin + third_width, HEIGHT - vertical_margin),  # Bottom left point
        (horizontal_margin, HEIGHT / 2)  # Middle left point
    ]

    def __init__(self, path_surface, player, enemies):
        self.path_surface = path_surface
        self.player = player
        self.enemies = enemies
        self.points = pygame.sprite.Group()
        # Draw path points on surface.
        for point in self.path_points:
            pygame.draw.circle(self.path_surface, GREEN, point, 5)

    def update(self):
        # Update AI state
        for enemy in self.enemies:
            target_x, target_y = self.path_points[enemy.target_point_index]
            speed = 2  # The speed the enemy moves to the point.
            # Calculate the new x and y for this enemy.
            if enemy.rect.x < target_x:
                enemy.rect.x += speed
            elif enemy.rect.x > target_x:
                enemy.rect.x -= speed
            if enemy.rect.y < target_y:
                enemy.rect.y += speed
            elif enemy.rect.y > target_y:
                enemy.rect.y -= speed
            # If the enemy is close enough to the current point, go to the next point.
            if abs(enemy.rect.x - target_x) < speed and abs(enemy.rect.y - target_y) < speed:
                enemy.rect.x = target_x
                enemy.rect.y = target_y
                enemy.update_target_point_index()
                point = Point(target_x, target_y)
                self.points.add(point)
                game.all_sprites.add(point)  # Add new point to all_sprites group.


# Create the Game class
class Game:
    def __init__(self):
        self.running = True
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.path_surface = pygame.Surface((WIDTH, HEIGHT))
        self.path_surface.set_colorkey(BLACK)
        self.clock = pygame.time.Clock()

        # Create sprites
        self.all_sprites = pygame.sprite.Group()
        self.player = Player()
        self.all_sprites.add(self.player)
        self.enemies = pygame.sprite.Group()  # Create enemies group before initializing the AI
        self.ai = AI(self.path_surface, self.player, self.enemies)
        for enemy in self.enemies:
            self.all_sprites.add(enemy)
        for point in self.ai.points:
            self.all_sprites.add(point)

    def new(self):
        # Create enemy instances
        for _ in range(10):
            enemy = Enemy()
            self.enemies.add(enemy)
            self.all_sprites.add(enemy)  # Add each enemy to the all_sprites group.

    def events(self):
        # Process game events
        for event in pygame.event.get():
            if event.type == QUIT:
                self.quit()

    def update(self):
        # Update game state
        self.player.update()
        self.enemies.update()
        self.ai.update()

    def render(self):
        # Render game objects
        self.screen.fill(BLACK)
        self.screen.blit(self.path_surface, (0, 0))
        self.all_sprites.draw(self.screen)
        # self.enemies.draw(self.screen) This line is no longer needed since enemies are part of all_sprites.
        pygame.display.flip()

    def quit(self):
        self.running = False

    def run(self):
        # Game loop
        while self.running:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.render()


# Create and run the game
if __name__ == '__main__':
    game = Game()
    game.new()
    game.run()