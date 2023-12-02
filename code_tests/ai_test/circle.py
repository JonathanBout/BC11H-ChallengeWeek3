"""
File: pygame_ai_integration.py
Description: A program that demonstrates how to implement AI in a Pygame project.
"""
import math

# Import the required modules and libraries
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


# Create the Game class
class Game:
    def __init__(self):
        self.running = True
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.all_sprites = pygame.sprite.Group()
        self.player = Player()
        self.all_sprites.add(self.player)
        self.enemies = pygame.sprite.Group()
        self.ai = AI(self.player, self.enemies)

    def new(self):
        # Create enemy instances
        for i in range(1):
            enemy = Enemy()
            self.enemies.add(enemy)

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
        pygame.draw.circle(
            self.screen, WHITE, self.ai.center, self.ai.radius, 1
        )  # Draw AI path
        self.all_sprites.draw(self.screen)
        self.enemies.draw(self.screen)

        pygame.display.flip()

    def quit(self):
        # Quit the game
        self.running = False

    def run(self):
        # Game loop
        while self.running:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.render()


# Create the Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
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


# Create the Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 30))
        self.image.fill(
            (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        )
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH)
        self.rect.y = random.randint(0, HEIGHT)

    def update(self):
        # Update enemy state
        self.rect.x = max(0, min(self.rect.x, WIDTH))
        self.rect.y = max(0, min(self.rect.y, HEIGHT))


# Create the AI class
class AI:
    def __init__(self, player, enemies):
        self.player = player
        self.enemies = enemies
        self.angle = 0  # We'll be using a polar angle to define the path
        self.radius = 100
        self.center = [WIDTH / 2, HEIGHT / 2]

    def update(self):
        # Update AI state
        for enemy in self.enemies:
            self.angle += 0.01
            if self.angle > 2 * math.pi:
                self.angle = 0
            x = self.center[0] + self.radius * math.cos(self.angle)
            y = self.center[1] + self.radius * math.sin(self.angle)
            enemy.rect.x = x
            enemy.rect.y = y


# Create and run the game
if __name__ == "__main__":
    game = Game()
    game.new()
    game.run()
