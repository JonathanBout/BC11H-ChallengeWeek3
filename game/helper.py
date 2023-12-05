import pygame


# Exit the game if the user wants to
def exit_if_user_wants():
    """
    Pumps the pygame events and closes the window whenever the X is clicked.
    """
    if len(pygame.event.get(eventtype=pygame.QUIT)) > 0:
        exit()


# Print a message to the console if the quit event is triggered
def why_quit_if_you_can_stay():
    print("😭 why are you going away?")


def wait_for_mouse_up(button: int = None):
    clock = pygame.time.Clock()
    while True:
        buttons = pygame.mouse.get_pressed()

        if not button and not any(buttons):
            return
        elif button and not buttons[button]:
            return

        print("release mouse to navigate")
        pygame.event.pump()
        clock.tick(100)
