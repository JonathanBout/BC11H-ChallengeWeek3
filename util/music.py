import pygame


class Music:
    def __init__(self, music_file, channel_id=0):
        pygame.mixer.init()
        self.sound_file = pygame.mixer.Sound(music_file)
        self.channel = pygame.mixer.Channel(channel_id)
        self.volume = self.channel.get_volume()

    def set_channel(self, channel_id):
        self.channel = pygame.mixer.Channel(channel_id)

    def play(self, loop=0):
        if not self.channel.get_busy():
            self.channel.play(self.sound_file, loops=loop)

    def stop(self):
        self.channel.stop()

    def stop_on_channel(self, channel_id):
        pygame.mixer.Channel(channel_id).stop()

    def set_volume(self, volume):
        self.channel.set_volume(volume)

    def get_volume(self):
        return self.channel.get_volume()

    def pause(self):
        self.channel.pause()

    def unpause(self):
        self.channel.unpause()
