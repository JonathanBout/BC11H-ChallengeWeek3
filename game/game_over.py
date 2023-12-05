from game.end_of_game_screen import EndOfGame
from pygame.font import Font


class GameOver(EndOfGame):
    def __init__(self, font: Font):
        super().__init__(font, "Game Over!")
