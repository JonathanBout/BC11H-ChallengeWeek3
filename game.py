import pygame
from pygame.time import Clock
from pygame.surface import Surface


def loop(screen: Surface, clock: Clock):
    screen.fill("white")

    # game logic

    # render everything
    pygame.display.flip()
    # target 60 fps
    clock.tick(60)


def game_loop(screen: Surface, clock: Clock):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        loop(screen, clock)


def main_menu(screen: Surface, clock: Clock):

    # TODO: make a fancy menu

    game_loop(screen, clock)


def main():
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    clock = pygame.time.Clock()
    main_menu(screen, clock)


if __name__ == "__main__":
    main()
