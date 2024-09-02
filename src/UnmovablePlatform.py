from src.ImageManager import ImageManager
from src.Platform import Platform

import pygame

vec = pygame.math.Vector2  # 2 for two dimensional


class UnmovablePlatform(Platform):
    __platformSprite: pygame.sprite.Sprite
    PLATFORM_TYPE = {"LEFT": 0, "MID_1": 1, "MID_2": 2, "RIGHT": 3}

    def __init__(self, x, y, height, width, type):
        super().__init__(x, y, width, height)
        self.type = self.PLATFORM_TYPE[type]
        self.velocity = vec(0, 0)

        if self.type == self.PLATFORM_TYPE["LEFT"]:
            platform_image = ImageManager().get_image('platform_left')
        elif self.type == self.PLATFORM_TYPE["MID_1"]:
            platform_image = ImageManager().get_image('platform_mid_1')
        elif self.type == self.PLATFORM_TYPE["MID_2"]:
            platform_image = ImageManager().get_image('platform_mid_2')
        elif self.type == self.PLATFORM_TYPE["RIGHT"]:
            platform_image = ImageManager().get_image('platform_right')
        else:
            platform_image = ImageManager().get_image('platform_mid_1')  # Default image

        self.__platformSprite = pygame.sprite.Sprite()
        self.__platformSprite.surf = pygame.Surface(self.size)

        self.__platformSprite.rect = self.__platformSprite.surf.get_rect(topleft=self.position)
        self.__platformSprite.image = platform_image
        self.__platformSprite.image = pygame.transform.scale(self.__platformSprite.image, self.size)
        pygame.transform.scale(self.__platformSprite.surf, self.size)

    def draw(self, surface: pygame.Surface):
        surface.blit(self.__platformSprite.image, self.__platformSprite.rect)