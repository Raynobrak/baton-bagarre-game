import pygame

from enum import Enum

from src.CooldownVariable import CooldownVariable
from src.Animation import *
from src.Fire import Fire
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

        self.isPunchingOrKicking = False

        self.movingDirection = PlayerDirection.IDLE
        self.lookingDirection = PlayerDirection.LEFT
        self.isJumping = True
        self.isLevitating = False

        self.punchCooldown = CooldownVariable(0.2) # todo improve punch and kick cooldown mechanics
        self.kickCooldown = CooldownVariable(0.3)

        self.set_animation(ANIM_PLAYER_IDLE)

    def set_animation(self, animInfos):
        self.animation = Animation(animInfos, self.position, self.size)
        self.animation.start()

    def update_animation(self, dt: float):
        self.animation.update(dt)

    def update(self, dt: float, fire: Fire):
        keysPressed = pygame.key.get_pressed()

        if keysPressed[pygame.K_e] and self.is_near_fire(fire):
            self.go_levitate()
        else:
            if self.isLevitating:
                self.go_idle()
            self.isLevitating = False

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

        movementSpeed = 150
        if self.movingDirection == PlayerDirection.LEFT:
            self.velocity.x = -movementSpeed
        elif self.movingDirection == PlayerDirection.RIGHT:
            self.velocity.x = movementSpeed

        self.apply_gravity(dt)

        super().update_position(dt)

        self.update_animation(dt)

        self.punchCooldown.update_cooldown(dt)
        self.kickCooldown.update_cooldown(dt)

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

    def go_levitate(self):
        if not self.isLevitating:
            self.set_animation(ANIM_PLAYER_LEVITATING)
            self.isLevitating = True
            if self.lookingDirection == PlayerDirection.RIGHT:
                self.animation.flip_horizontally()


    def try_punch(self):
        if self.punchCooldown.try_reset():
            self.isPunchingOrKicking = True
        
    def try_kick(self):
        if self.kickCooldown.try_reset():
            self.isPunchingOrKicking = True

    def reset_jump(self):
        if self.isJumping:
            self.isJumping = False

            if self.movingDirection == PlayerDirection.IDLE:
                self.set_animation(ANIM_PLAYER_IDLE)
            else:
                self.set_animation(ANIM_PLAYER_WALKING)

            if self.lookingDirection == PlayerDirection.RIGHT:
                self.animation.flip_horizontally()

    def check_collision_with_walls(self, mapSize: vec):
        if self.position.y + self.size.y > mapSize.y:
            self.position.y = mapSize.y - self.size.y
            self.velocity.y = 0
            self.reset_jump()

    def jump(self):
        if not self.isJumping:
            self.accelerate(vec(0, -350))
            self.isJumping = True
            self.set_animation(ANIM_PLAYER_JUMPING)
            if self.lookingDirection == PlayerDirection.RIGHT:
                    self.animation.flip_horizontally()

    def draw(self, surface):
        if not self.punchCooldown.ready():
            punchImage = ImageManager().get_image('player_punch')
            punchImage = pygame.transform.scale(punchImage, self.size)
            if self.lookingDirection == PlayerDirection.RIGHT:
                punchImage = pygame.transform.flip(punchImage, True, False)
            surface.blit(punchImage, Rect(self.position, self.size))
        elif not self.kickCooldown.ready():
            kickImage = ImageManager().get_image('player_kick')
            kickImage = pygame.transform.scale(kickImage, self.size)
            if self.lookingDirection == PlayerDirection.RIGHT:
                kickImage = pygame.transform.flip(kickImage, True, False)
            surface.blit(kickImage, Rect(self.position, self.size))
        else:
            self.animation.set_position(self.position)
            self.animation.draw(surface)

    def is_near_fire(self, fire: Fire):
        distance = self.position.distance_to(fire.position)
        return distance < 50
        