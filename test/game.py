import pygame
from pygame.time import Clock
from pygame.surface import Surface

SCREEN_X_SIZE = 250
SCREEN_Y_SIZE = 250
SCREEN_CENTER_Y = SCREEN_Y_SIZE / 2
SCREEN_CENTER_X = SCREEN_X_SIZE / 2


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_X_SIZE, SCREEN_Y_SIZE))
        self.clock = pygame.time.Clock()
        self.player_x = SCREEN_CENTER_X
        self.main_menu()

    def do_movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.player_x -= 250 / self.clock.get_fps()
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.player_x += 250 / self.clock.get_fps()

    def loop_frame(self):
        self.screen.fill("white")

        # game logic
        self.do_movement()
        print(self.player_x)
        pygame.draw.circle(self.screen, "red", (self.player_x, SCREEN_CENTER_Y), 50)

        # render everything
        pygame.display.flip()

        # target 120 fps. If we want a more retro look,
        # this can be lowered to e.g. 10fps
        self.clock.tick(120)

    def game_loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
            print(self.clock.get_fps())
            self.loop_frame()

    def main_menu(self):
        # TODO: make a fancy menu

        self.game_loop()


def main():
    Game()


if __name__ == "__main__":
    main()
