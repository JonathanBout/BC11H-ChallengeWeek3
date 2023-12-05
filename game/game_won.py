from game.end_of_game_screen import EndOfGame
from pygame.font import Font


class GameWon(EndOfGame):
    def __init__(self, font: Font) -> None:
        super().__init__(font, "You Won!")
