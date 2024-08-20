import pygame
from pygame.locals import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        PLAYER_IMAGE = pygame.image.load('./assets/textures/player_default.png').convert_alpha()

        super().__init__()
        self.surf = pygame.Surface((30, 30))
        #self.surf.fill((128,255,40))
        self.rect = self.surf.get_rect(center = (50, 50))
        self.image = PLAYER_IMAGE
        print("hi")

    def draw(self, surface):
        surface.blit(self.image, self.rect)