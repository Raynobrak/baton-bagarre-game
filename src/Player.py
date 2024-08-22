import pygame

from enum import Enum

from src.CooldownVariable import CooldownVariable
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

        self.isPunchingOrKicking = False

        self.movingDirection = PlayerDirection.IDLE
        self.lookingDirection = PlayerDirection.LEFT
        self.isJumping = False

        self.punchCooldown = CooldownVariable(0.2)
        self.kickCooldown = CooldownVariable(0.3)

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
        if self.movingDirection == PlayerDirection.LEFT:
            self.velocity.x = -movementSpeed
        elif self.movingDirection == PlayerDirection.RIGHT:
            self.velocity.x = movementSpeed

        super().update_position(dt)

        self.update_animation(dt)
        self.punchCooldown.update_cooldown(dt)
        self.kickCooldown.update_cooldown(dt)

        self.__playerSprite.rect.x = self.position.x
        self.__playerSprite.rect.y = self.position.y

        keysPressed = pygame.key.get_pressed()
        if keysPressed[pygame.K_a]: 
            self.go_left()
        elif keysPressed[pygame.K_d]: 
            self.go_right()

        if keysPressed[pygame.K_w]:
            self.jump()

        if keysPressed[pygame.K_SPACE]:
            self.try_punch()
        elif keysPressed[pygame.K_k]:
            self.try_kick()

        if not keysPressed[pygame.K_a] and not keysPressed[pygame.K_d]:
            self.go_idle()

        self.apply_gravity(dt)

    def go_left(self):
        self.lookingDirection = PlayerDirection.LEFT
        if self.movingDirection != PlayerDirection.LEFT:
            self.movingDirection = PlayerDirection.LEFT
            self.set_animation(ANIM_PLAYER_WALKING)

    def go_right(self):
        self.lookingDirection = PlayerDirection.RIGHT
        if self.movingDirection != PlayerDirection.RIGHT:
            self.movingDirection = PlayerDirection.RIGHT
            self.set_animation(ANIM_PLAYER_WALKING)
            self.animation.flip_horizontally()

    def go_idle(self):
        if self.movingDirection != PlayerDirection.IDLE:
            self.set_animation(ANIM_PLAYER_IDLE)
            if self.movingDirection == PlayerDirection.RIGHT:
                self.animation.flip_horizontally()
            self.movingDirection = PlayerDirection.IDLE
        self.velocity.x = 0

    def try_punch(self):
        if self.punchCooldown.try_reset():
            self.isPunchingOrKicking = True
        
    def try_kick(self):
        if self.kickCooldown.try_reset():
            self.isPunchingOrKicking = True  

    def check_collision_with_walls(self, mapSize: vec):
        if self.position.y + self.__playerSprite.rect.height > mapSize.y:
            self.position.y = mapSize.y - self.__playerSprite.rect.height
            self.velocity.y = 0

            if self.isJumping == True:
                self.isJumping = False

                if self.movingDirection == PlayerDirection.IDLE:
                    self.set_animation(ANIM_PLAYER_IDLE)
                else:
                    self.set_animation(ANIM_PLAYER_WALKING)

                if self.lookingDirection == PlayerDirection.RIGHT:
                    self.animation.flip_horizontally()

    def jump(self):
        if not self.isJumping:
            self.accelerate(vec(0, -250))
            self.isJumping = True
            self.set_animation(ANIM_PLAYER_JUMPING)
            if self.lookingDirection == PlayerDirection.RIGHT:
                    self.animation.flip_horizontally()

    def draw(self, surface):
        #surface.blit(self.__playerSprite.image, self.__playerSprite.rect)
        if not self.punchCooldown.ready():
            punchImage = ImageManager().get_image('player_punch')
            punchImage = pygame.transform.smoothscale(punchImage, self.size)
            if self.lookingDirection == PlayerDirection.RIGHT:
                punchImage = pygame.transform.flip(punchImage, True, False)
            surface.blit(punchImage, Rect(self.position, self.size))
        elif not self.kickCooldown.ready():
            kickImage = ImageManager().get_image('player_kick')
            kickImage = pygame.transform.smoothscale(kickImage, self.size)
            if self.lookingDirection == PlayerDirection.RIGHT:
                kickImage = pygame.transform.flip(kickImage, True, False)
            surface.blit(kickImage, Rect(self.position, self.size))
        else:
            self.animation.draw(surface)

        