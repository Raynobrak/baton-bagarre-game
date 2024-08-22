import pygame

from enum import Enum

from src.Animation import *
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

        self.size = size

        PLAYER_IMAGE = ImageManager().get_image("player")

        resized_image = pygame.transform.smoothscale(PLAYER_IMAGE, size)

        self.__playerSprite = pygame.sprite.Sprite()
        self.__playerSprite.size = size
        
        self.__playerSprite.surf = pygame.Surface(size)
        self.__playerSprite.rect = self.__playerSprite.surf.get_rect(center = (50, 50))
        self.__playerSprite.image = resized_image

        self.currentDirection = PlayerDirection.IDLE
        self.isJumping = False

        self.set_animation(ANIM_PLAYER_IDLE)

    def set_animation(self, animInfos):
        self.animation = Animation(animInfos, self.position, self.size)
        self.animation.set_position(self.position)
        self.animation.start()

    def update_animation(self, dt: float):
        self.animation.update(dt)
        self.animation.set_position(self.position)

    def update(self, dt: float):
        movementSpeed = 150
        if self.currentDirection == PlayerDirection.LEFT:
            self.velocity.x = -movementSpeed
        elif self.currentDirection == PlayerDirection.RIGHT:
            self.velocity.x = movementSpeed

        super().update_position(dt)

        self.update_animation(dt)

        self.__playerSprite.rect.x = self.position.x
        self.__playerSprite.rect.y = self.position.y

        keysPressed = pygame.key.get_pressed()
        keyAorDPressed = False
        if keysPressed[pygame.K_a]: 
            self.go_left()
            keyAorDPressed = True
        elif keysPressed[pygame.K_d]: 
            self.go_right()
            keyAorDPressed = True

        if keysPressed[pygame.K_w]:
            self.jump()
        if not keyAorDPressed:
            self.go_idle()

        self.apply_gravity(dt)

    def go_left(self):
        if self.currentDirection != PlayerDirection.LEFT:
            self.currentDirection = PlayerDirection.LEFT
            self.set_animation(ANIM_PLAYER_WALKING)

    def go_right(self):
        if self.currentDirection != PlayerDirection.RIGHT:
            self.currentDirection = PlayerDirection.RIGHT
            self.set_animation(ANIM_PLAYER_WALKING)
            self.animation.flip_horizontally()

    def go_idle(self):
        if self.currentDirection != PlayerDirection.IDLE:
            self.set_animation(ANIM_PLAYER_IDLE)
            if self.currentDirection == PlayerDirection.RIGHT:
                self.animation.flip_horizontally()
            self.currentDirection = PlayerDirection.IDLE
        self.velocity.x = 0

    def try_punch(self):
        pass
        
    def try_kick(self):
        pass  

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
        #surface.blit(self.__playerSprite.image, self.__playerSprite.rect)
        self.animation.draw(surface)