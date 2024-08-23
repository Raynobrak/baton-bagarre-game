import pygame.mixer

from src.VolumeManager import VolumeManager


class AudioManager:
    __instance = None
    sound = dict()

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(AudioManager,cls).__new__(cls,*args, **kwargs)
            pygame.mixer.init()
        return cls.__instance

    def load_sound(self, path, key):
        sound = pygame.mixer.Sound(path)
        AudioManager.sound.update({key:sound})

    def play_sound(self, key):
        sound: pygame.mixer.Sound = AudioManager.sound[key]
        sound.set_volume(VolumeManager().soundVolume)
        sound.play()