import pygame


def exit_if_user_wants():
    """
    Helper to close the window whenever the X is clicked.
    """
    if len(pygame.event.get(eventtype=pygame.QUIT)) > 0:
        print("😭why are you going away?")
        exit()
