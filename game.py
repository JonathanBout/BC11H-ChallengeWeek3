import pygame

import config as c
from map import Map
from world import World
from player import Player


class Game:
    def __init__(self):
        # initialize pygame
        pygame.init()

        # initialize screen and clock
        self.screen = pygame.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.frame_counter = 0  # add counter for frames
        self.dt = 0  # add delta time

        # Initialize frame_update_interval using config variable
        self.frame_update_interval = c.PLAYER_FRAME_UPDATE_INTERVAL

        # initialize game objects
        self.world = World(c, c.WORLD_NAME, c.WORLD_DESCRIPTION, c.WORLD_POSITION)
        self.race_track = Map(c, c.MAP_NAME, c.MAP_DESCRIPTION, c.MAP_POSITION)
        self.player = Player(c, c.PLAYER_NAME, c.PLAYER_DESCRIPTION, c.PLAYER_POSITION)

        # Player properties
        self.flip_player = None
        self.player1 = self.player.prepare(c.PLAYER_CURRENT_FRAME)

    def start(self):
        # Start game loop
        self.update()

    def update(self):
        # Start game loop
        while True:
            # Set the current window caption
            pygame.display.set_caption(f"{c.WORLD_NAME} - {c.CURRENT_FPS}")

            # traversing through every event
            for event in pygame.event.get():
                # if the event type is QUIT then exit thwe program
                if event.type == pygame.QUIT:
                    exit()

            pygame.time.wait(10)

            # Update the player1 after refreshing the screen
            if c.CURRENT_FPS == 0:
                print("CURRENT_FPS value is Zero! Please, check the value.")
            else:
                self.dt = 1.0 / c.CURRENT_FPS
            self.player1 = self.player.move(self.screen, self.dt)
            # Print the current frame of the player
            # print(f"Current frame: {c.PLAYER_CURRENT_FRAME}")
            print(f"Current position: {c.PLAYER_CURRENT_POSITION}")

            # Update the frame counter
            self.frame_counter += 1


            # render everything
            self.render()

            # Refresh the screen
            self.refresh_screen()

    def render(self):
        # Update the full display surface to the screen
        pygame.display.flip()

        # Set target fps
        self.clock.tick(c.MAX_FPS)

        # printing the frames per second (fps) rate
        c.CURRENT_FPS = self.clock.get_fps()

        # print("FPS:", c.CURRENT_FPS)

    def refresh_screen(self):
        # Clear the screen by filling it with a single color (black in this case)
        self.screen.fill((0, 0, 0))

        # Fill the screen with a custom background
        background = pygame.image.load(c.SCREEN_BACKGROUND)
        background = pygame.transform.scale(background, c.SCREEN_SIZE)
        self.screen.blit(background, (0, 0))

    def print_config(self):
        self.world.print_config()
        self.race_track.print_config()
        self.player.print_config()


if __name__ == "__main__":
    game = Game()
    game.start()
