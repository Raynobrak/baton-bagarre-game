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
    def __init__(self, size: vec):
        super().__init__()

        self.velocity = vec(20,20)

        PLAYER_IMAGE = ImageManager().get_image("player")

        resized_image = pygame.transform.smoothscale(PLAYER_IMAGE, size)
        self.__playerSprite = pygame.sprite.Sprite()
        self.__playerSprite.size = size
        
        self.__playerSprite.surf = pygame.Surface(size)
        self.__playerSprite.rect = self.__playerSprite.surf.get_rect(center = (50, 50))
        self.__playerSprite.image = resized_image

        self.currentDirection = PlayerDirection.IDLE
        self.isJumping = False

    def update(self, dt: float):
        movementSpeed = 150
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

    def check_collision_with_walls(self, mapSize: vec):
        if self.position.y + self.__playerSprite.rect.height > mapSize.y:
            self.isJumping = False
            self.position.y = mapSize.y - self.__playerSprite.rect.height
            print("coll")
            self.velocity.y = 0

    def jump(self):
        if not self.isJumping:
            self.accelerate(vec(0, -250))
            self.isJumping = True

    def draw(self, surface):
        surface.blit(self.__playerSprite.image, self.__playerSprite.rect)