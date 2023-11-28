import pygame

import config as c
from map import Map
from world import World
from player import Player
from display import Display


class Game:
    def __init__(self):
        # initialize pygame
        pygame.init()

        # initialize screen and clock
        self.display = Display()
        self.display.set_display_size()

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

        # setup menu
        from menu import Menu
        self.menu = Menu()

        # initialize game objects
        self.world = World(c, c.WORLD_NAME, c.WORLD_DESCRIPTION, c.WORLD_POSITION)
        self.race_track = Map(c, c.MAP_NAME, c.MAP_DESCRIPTION, c.MAP_POSITION)
        self.player = Player(c, c.PLAYER_NAME, c.PLAYER_DESCRIPTION, c.PLAYER_POSITION)

        # Player properties
        self.flip_player = None
        self.player1 = self.player.prepare(c.PLAYER_CURRENT_FRAME)

    def start(self):
        while True:
            match self.menu.show(self):
                case 1:
                    self.update()
                case 2:
                    return

    def update(self):
        # Start game loop
        while True:
            # Set the current window caption
            pygame.display.set_caption(f"{c.WORLD_NAME} - {c.CURRENT_FPS}")

            # traversing through every event
            for event in pygame.event.get():
                # if the event type is QUIT then exit the program
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == self.RESPAWN_TEXT_EVENT:
                    self.respawn_text = False
            pygame.time.wait(10)

            # Move the player
            self.player1 = self.player.move(self.display.screen)

            # Check if player is on the road
            self.player1 = self.player.check_for_events(self.display.screen)

            # Update the display and fps
            self.display.draw()


    def refresh_screen(self):

        pixelPosition = (int(c.PLAYER_CURRENT_POSITION[0] + 60), int(c.PLAYER_CURRENT_POSITION[1] + 60))
        color = self.screen.get_at(pixelPosition)

        if color == (0, 0, 96, 255):
            self.respawn_text = True
            pygame.time.set_timer(self.RESPAWN_TEXT_EVENT, 3000)
            print("You are no longer on the road!")
            self.boo_laugh.play()
            c.PLAYER_CURRENT_POSITION = [283.1699855873012, 101.21998571824301]

        if self.respawn_text is True:
            respawn_text = self.font.render("You are no longer on the road!", True, self.font_color)
            self.screen.blit(respawn_text, (c.SCREEN_CENTER_X - 200, c.SCREEN_CENTER_Y - 100))
        print(color)

    def print_config(self):
        self.world.print_config()
        self.race_track.print_config()
        self.player.print_config()


if __name__ == "__main__":
    game = Game()
    game.start()
