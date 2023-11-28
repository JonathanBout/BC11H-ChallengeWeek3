import pygame


class Music:
    def __init__(self, music_file, channel_id=0):
        pygame.mixer.init()
        self.sound_file = pygame.mixer.Sound(music_file)
        self.channel = pygame.mixer.Channel(channel_id)

    def set_channel(self, channel_id):
        self.channel = pygame.mixer.Channel(channel_id)

    def play(self):
        if not self.channel.get_busy():
            self.channel.play(self.sound_file)

    def stop(self):
        self.channel.stop()

    def pause(self):
        self.channel.pause()

    def unpause(self):
        self.channel.unpause()
