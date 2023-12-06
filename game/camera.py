# PyGame Camera Class
from pygame import Rect, sprite
from game import config


class Camera:
    # Move the screen if the player is close to the edge
    def do_movement(
        self, player_rect: Rect, screen_rect: Rect, powerups: sprite.Group
    ) -> tuple[Rect, Rect]:
        camera_move = config.PLAYER_CURRENT_SPEED / 100
        if player_rect.bottom + config.SCREEN_MOVE_OFFSET >= screen_rect.bottom:
            config.MAP_POSITION[1] -= camera_move
            player_rect.top -= camera_move
            for powerup in powerups:
                powerup.rect.top -= config.PLAYER_CURRENT_SPEED
        elif player_rect.top - config.SCREEN_MOVE_OFFSET <= screen_rect.top:
            config.MAP_POSITION[1] += config.PLAYER_CURRENT_SPEED
            player_rect.top += config.PLAYER_CURRENT_SPEED
            for powerup in powerups:
                powerup.rect.top += config.PLAYER_CURRENT_SPEED

        if player_rect.right + config.SCREEN_MOVE_OFFSET >= screen_rect.right:
            config.MAP_POSITION[0] -= config.PLAYER_CURRENT_SPEED
            player_rect.left -= config.PLAYER_CURRENT_SPEED
            for powerup in powerups:
                powerup.rect.left -= config.PLAYER_CURRENT_SPEED
        elif player_rect.left - config.SCREEN_MOVE_OFFSET <= screen_rect.left:
            config.MAP_POSITION[0] += config.PLAYER_CURRENT_SPEED
            player_rect.right += config.PLAYER_CURRENT_SPEED
            for powerup in powerups:
                powerup.rect.left += config.PLAYER_CURRENT_SPEED

        return player_rect, screen_rect

    # Reset the camera to the spawn position
    def reset(self):
        config.MAP_POSITION = config.MAP_RESPAWN_POSITION
