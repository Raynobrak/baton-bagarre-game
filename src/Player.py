import pygame

from src.ImageManager import ImageManager
from src.Stickman import Stickman
from pygame.locals import *
vec = pygame.math.Vector2  # 2 for two dimensional

class Player(Stickman):
    __playerSprite: pygame.sprite.Sprite 

    def __init__(self):
        super().__init__()

        self.velocity = vec(20,20)

        PLAYER_IMAGE = ImageManager().get_image("player")

        self.__playerSprite = pygame.sprite.Sprite()
        self.__playerSprite.surf = pygame.Surface((30, 30))
        self.__playerSprite.rect = self.__playerSprite.surf.get_rect(center = (50, 50))
        self.__playerSprite.image = PLAYER_IMAGE

    def update(self, dt: float):
        super().update_position(dt)
        self.__playerSprite.rect.x = self.position.x
        self.__playerSprite.rect.y = self.position.y

    def draw(self, surface):
        surface.blit(self.__playerSprite.image, self.__playerSprite.rect)