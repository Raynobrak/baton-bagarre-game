import pygame

from enum import Enum

from src.ImageManager import ImageManager
from src.Stickman import Stickman
from pygame.locals import *
vec = pygame.math.Vector2  # 2 for two dimensional

class PlayerDirection(Enum):
    IDLE = 0
    LEFT = 1
    RIGHT = 2

class Player(Stickman):
    def __init__(self):
        super().__init__()

        self.velocity = vec(20,20)

        PLAYER_IMAGE = ImageManager().get_image("player")

        self.__playerSprite = pygame.sprite.Sprite()
        self.__playerSprite.surf = pygame.Surface((30, 30))
        self.__playerSprite.rect = self.__playerSprite.surf.get_rect(center = (50, 50))
        self.__playerSprite.image = PLAYER_IMAGE

        self.currentDirection = PlayerDirection.IDLE
        self.isJumping = False

    def update(self, dt: float):
        movementSpeed = 50
        if self.currentDirection == PlayerDirection.LEFT:
            self.velocity.x = -movementSpeed
        elif self.currentDirection == PlayerDirection.RIGHT:
            self.velocity.x = movementSpeed

        super().update_position(dt)
        self.__playerSprite.rect.x = self.position.x
        self.__playerSprite.rect.y = self.position.y

    def go_left(self):
        self.currentDirection = PlayerDirection.LEFT

    def go_right(self):
        self.currentDirection = PlayerDirection.RIGHT

    def go_idle(self):
        self.currentDirection = PlayerDirection.IDLE
        self.velocity.x = 0

    def jump(self):
        if not self.isJumping:
            self.accelerate(vec(0, -150))
            self.isJumping = True

    def draw(self, surface):
        surface.blit(self.__playerSprite.image, self.__playerSprite.rect)