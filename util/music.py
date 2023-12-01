import pygame


class Music:
    def __init__(self, music_file, channel_id=0):
        pygame.mixer.init()
        self.sound_file = pygame.mixer.Sound(music_file)
        self.channel = pygame.mixer.Channel(channel_id)
        self.volume = self.channel.get_volume()

    def set_channel(self, channel_id):
        """
        :param channel_id: The ID of the channel to set as the active channel for playing music.
        :return: None
        """
        self.channel = pygame.mixer.Channel(channel_id)

    def play(self, loop=0):
        """
        Plays the music.
        :param loop: The number of times to loop the music. Defaults to 0, which means it won't loop.
        If loop is -1, the music will loop indefinitely.
        :return: None
        """
        if not self.channel.get_busy():
            self.channel.play(self.sound_file, loops=loop)

    def stop(self):
        """
        Stops the music playback.
        :return: None
        """
        self.channel.stop()

    def stop_on_channel(self, channel_id):
        """
        :param channel_id: The ID of the channel to stop playing music on.
        :return: None
        """
        pygame.mixer.Channel(channel_id).stop()

    def set_volume(self, volume):
        """
        :param volume: The desired volume level for the music.
        The value should be between 0.0 and 1.0, where 0.0 is minimum volume (silence) and 1.0 is maximum volume.
        :return: None
        """
        self.channel.set_volume(volume)

    def get_volume(self):
        """
        Returns the current volume of the music.
        :return: The current volume of the music.
        """
        return self.channel.get_volume()

    def pause(self):
        """
        Pauses the currently playing music.
        :return: None
        """
        self.channel.pause()

    def unpause(self):
        """
        Unpauses the currently playing music.
        :return: None
        """
        self.channel.unpause()
