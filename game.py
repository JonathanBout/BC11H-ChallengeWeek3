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

        # set up font for text rendering
        self.font_color = (144, 238, 144)
        self.font = pygame.font.SysFont("Arial", 40)
        self.font.set_bold(True)
        self.respawn_text = False
        self.RESPAWN_TEXT_EVENT = pygame.USEREVENT + 1

        # set up sounds mixer
        pygame.mixer.init()
        self.boo_laugh = pygame.mixer.Sound("sounds/mk64_boo_laugh.wav")

        # initialize game objects
        self.world = World(c, c.WORLD_NAME, c.WORLD_DESCRIPTION, c.WORLD_POSITION)
        self.race_track = Map(c, c.MAP_NAME, c.MAP_DESCRIPTION, c.MAP_POSITION)
        self.player = Player(c, c.PLAYER_NAME, c.PLAYER_DESCRIPTION, c.PLAYER_POSITION)

        from menu import Menu  # import menu over here due to circular import problems

        self.menu = Menu()

        # Player properties
        self.flip_player = None
        self.player1 = self.player.prepare(c.PLAYER_CURRENT_FRAME)

    def start(self):
        # show the menu over and over again
        while True:
            match self.menu.show(self):
                case 1:  # 1=start game
                    self.update()
                case 2:  # 2=quit
                    return
                # add more cases e.g. for a leader board

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
                elif event.type == self.RESPAWN_TEXT_EVENT:
                    self.respawn_text = False
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
        self.screen.fill((0, 0, 96))

        # Fill the screen with a custom background
        background = pygame.image.load(c.WORLD_BACKGROUND)
        background = pygame.transform.scale(
            background, (c.SCREEN_WIDTH * 2, c.SCREEN_HEIGHT * 2)
        )
        self.screen.blit(background, (0, 0))

        pixelPosition = (
            int(c.PLAYER_CURRENT_POSITION[0] + 60),
            int(c.PLAYER_CURRENT_POSITION[1] + 60),
        )
        color = self.screen.get_at(pixelPosition)

        if color == (0, 0, 96, 255):
            self.respawn_text = True
            pygame.time.set_timer(self.RESPAWN_TEXT_EVENT, 3000)
            print("You are no longer on the road!")
            self.boo_laugh.play()
            c.PLAYER_CURRENT_POSITION = [283.1699855873012, 101.21998571824301]

        if self.respawn_text is True:
            respawn_text = self.font.render(
                "You are no longer on the road!", True, self.font_color
            )
            self.screen.blit(
                respawn_text, (c.SCREEN_CENTER_X - 200, c.SCREEN_CENTER_Y - 100)
            )
        print(color)

    def print_config(self):
        self.world.print_config()
        self.race_track.print_config()
        self.player.print_config()


if __name__ == "__main__":
    game = Game()
    game.start()
