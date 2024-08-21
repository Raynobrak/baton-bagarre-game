from sys import platform

from src.ImageManager import ImageManager
from src.Platform import Platform

import pygame

vec = pygame.math.Vector2  # 2 for two dimensional

class UnmovablePlatform(Platform):
    __platformSprite: pygame.sprite.Sprite

    def __init__(self, x, y, heigth, width):
        super().__init__(x,y, heigth, width)
        self.velocity = vec(0, 0)

        platform_image = ImageManager().get_image('platform')

        self.__platformSprite = pygame.sprite.Sprite()
        self.__platformSprite.surf = pygame.Surface(self.size)

        self.__platformSprite.rect = self.__platformSprite.surf.get_rect(center=self.position)
        self.__platformSprite.image = platform_image
        self.__platformSprite.image = pygame.transform.smoothscale(self.__platformSprite.image, self.size)
        pygame.transform.smoothscale(self.__platformSprite.surf, self.size)


    def draw(self, surface: pygame.Surface):
        surface.blit(self.__platformSprite.image,self.__platformSprite.rect)