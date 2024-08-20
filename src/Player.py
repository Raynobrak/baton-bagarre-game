import pygame
import Stickman
from pygame.locals import *
vec = pygame.math.Vector2  # 2 for two dimensional

class Player(Stickman):
    __playerSprite: pygame.sprite.Sprite 

    def __init__(self):
        super().__init__()

        PLAYER_IMAGE = pygame.image.load('./assets/textures/player_default.png').convert_alpha()

        self.__playerSprite.surf = pygame.Surface((30, 30))
        self.__playerSprite.rect = self.surf.get_rect(center = (50, 50))
        self.__playerSprite.image = PLAYER_IMAGE

        print("hi")

    def draw(self, surface):
        surface.blit(self.__playerSprite.image, self.__playerSprite.rect)