from game.end_of_game_screen import EndOfGame
from pygame.font import Font


class GameOver(EndOfGame):
    def __init__(self, font: Font):
        super().__init__(font, "Game Over!")

    def show(self, did_enemy_win: bool):
        if did_enemy_win:
            super().set_text("You Lost!")
        else:
            super().set_text("Game Over!")
        return super().show()
