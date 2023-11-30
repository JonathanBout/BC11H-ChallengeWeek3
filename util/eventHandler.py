import pygame
from pygame.constants import USEREVENT

import game.config as c
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
                int(self.player_position[0] + 60),
                int(self.player_position[1] + 60)
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
        print("C: ", c.PLAYER_CURRENT_POSITION)
        print("R: ", c.PLAYER_RESPAWN_POSITION)
        print("You are no longer on the road!")
        self.respawn_sound.play()
        c.MAP_POSITION = [0, 0]
        c.PLAYER_CURRENT_POSITION = c.PLAYER_RESPAWN_POSITION[:]

        pygame.event.post(pygame.event.Event(c.PLAYER_GAMEOVER_EVENT))


class EventManager:
    def __init__(self):
        self.events = []

    def register_event(self, event):
        self.events.append(event)

    def trigger_events(self):
        for event in self.events:
            event.trigger()
