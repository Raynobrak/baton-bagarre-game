import pygame.mixer


class AudioManager:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(AudioManager,cls).__new__(cls,*args, **kwargs)
            pygame.mixer.init()
        return cls.__instance

    def hurtSound(self):
        sound = pygame.mixer.Sound("./assets/audio/snore.mp3")
        sound.set_volume(1.0)
        sound.play(loops=1)