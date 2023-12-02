import pygame
from pygame.constants import USEREVENT

from game import config
from util.music import Music


class CustomEvent:
    def __init__(self, delay=3000):
        self.EVENT_TYPE = USEREVENT + 1
        pygame.time.set_timer(self.EVENT_TYPE, delay)

    def trigger(self):
        raise NotImplementedError


class RespawnEvent(CustomEvent):
    def __init__(self, screen, player_position, respawn_sound):
        super().__init__()
        self.screen = screen
        self.player_position = player_position
        self.respawn_sound = Music(respawn_sound, 1)
        self.is_respawn_triggered = False

    def trigger(self):
        # Get the color of the pixel at the player's position
        color = self.screen.get_at(
            (
                int(self.player_position[0] + config.PLAYER_SPRITE_HEIGHT * 2),
                int(self.player_position[1] + config.PLAYER_SPRITE_WIDTH * 2),
            )
        )

        # The color of the respawn area
        respawn_color = (0, 0, 96, 255)

        # If the player is on the road, reset the respawn trigger
        if color != respawn_color:
            self.is_respawn_triggered = False

        # If the player is not on the road, trigger the respawn event
        if color == respawn_color:
            if not self.is_respawn_triggered:
                self.is_respawn_triggered = True
                self.handle_respawn()

    def handle_respawn(self):
        print("C: ", config.PLAYER_CURRENT_POSITION)
        print("R: ", config.PLAYER_RESPAWN_POSITION)
        print("You are no longer on the road!")
        self.respawn_sound.play()
        config.MAP_POSITION = [0, 0]
        config.PLAYER_CURRENT_POSITION = config.PLAYER_RESPAWN_POSITION[:]

        pygame.event.post(pygame.event.Event(config.PLAYER_GAMEOVER_EVENT))


class FinishEvent(CustomEvent):
    def __init__(self, screen, player_position, finish_sound):
        super().__init__()
        self.screen = screen
        self.player_position = player_position
        self.finish_sound = Music(finish_sound, 2)
        self.lap_sound = Music(config.LAP_SOUND, 1)
        self.is_finish_triggered = False
        self.is_lap_triggered = False
        self.finish_count = 0

    def trigger(self):
        # Get the color of the pixel at the player's position
        color = self.screen.get_at(
            (
                int(self.player_position[0] + config.PLAYER_SPRITE_HEIGHT * 2),
                int(self.player_position[1] + config.PLAYER_SPRITE_WIDTH * 2),
            )
        )

        print(color)

        # The color of the respawn area
        finish_color = (248, 248, 248, 255)

        # If the player is on the road, reset the respawn trigger
        if color != finish_color:
            self.is_finish_triggered = False

        # If the player is not on the road, trigger the respawn event
        keys = pygame.key.get_pressed()
        backwards = keys[pygame.K_s]

        if color == finish_color:
            if not backwards:
                config.RACE_CURRENT_LAP += 1
            if not backwards and config.RACE_CURRENT_LAP > config.RACE_LAPS + 1:
                self.is_finish_triggered = True
                config.RACE_CURRENT_LAP = 0
            if not self.is_finish_triggered:
                self.is_lap_triggered = True

        if not backwards and self.is_finish_triggered:
            self.handle_finish()

        if not backwards and self.is_lap_triggered and config.RACE_CURRENT_LAP > 1:
            self.handle_lap()
            self.is_lap_triggered = False

    def handle_finish(self):
        self.finish_sound.play()

    def handle_lap(self):
        self.lap_sound.play()


class EventManager:
    def __init__(self):
        self.events = []

    def register_event(self, event):
        self.events.append(event)

    def trigger_events(self):
        for event in self.events:
            event.trigger()
