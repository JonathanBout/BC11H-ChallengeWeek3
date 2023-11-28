import pygame


def exit_if_user_wants():
    if len(pygame.event.get(eventtype=pygame.QUIT)) > 0:
        exit()
