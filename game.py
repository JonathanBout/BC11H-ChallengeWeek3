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
        # Refresh the screen
        self.refresh_screen()

        num_frames = 10  # total number of frames in the animation

        while True:
            # traversing through every event
            for event in pygame.event.get():
                # if the event type is QUIT then exit the program
                if event.type == pygame.QUIT:
                    exit()

            # Calculate the current frame

            #         # Keydown events
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_UP:
            #         print("Up key pressed.")
            #     elif event.key == pygame.K_DOWN:
            #         print("Down key pressed.")
            #     elif event.key == pygame.K_LEFT:
            #         print("Left key pressed.")
            #         self.flip_player = True
            #     elif event.key == pygame.K_RIGHT:
            #         print("Right key pressed.")
            #         self.flip_player = False
            #     self.flip_player = not self.flip_player

            current_frame = (self.frame_counter // self.frame_update_interval) % num_frames
            c.PLAYER_CURRENT_FRAME = current_frame

            self.player1 = self.player.prepare(c.PLAYER_CURRENT_FRAME)

            # Check if the player image should be flipped
            if self.flip_player:
                self.player1 = pygame.transform.flip(self.player1, True,
                                                     False)  # Flip the image horizontally, not vertically

            # Update the frame counter
            self.frame_counter += 1

            print(f"Current frame: {current_frame}")

            # render everything
            self.render()

    def render(self):
        # Draw the player1 after refreshing the screen
        self.screen.blit(self.player1, (self.player.position[0], self.player.position[1]))

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
