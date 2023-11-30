import pygame


def exit_if_user_wants():
    """
    Helper to close the window whenever the X is clicked.
    """
    if len(pygame.event.get(eventtype=pygame.QUIT)) > 0:
        why_quit_if_you_can_stay()
        exit()


def why_quit_if_you_can_stay():
    print("😭why are you going away?")
