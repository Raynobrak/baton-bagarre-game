import pygame

from enum import Enum

from src.CooldownVariable import CooldownVariable
from src.Animation import *
from src.ImageManager import ImageManager
from src.Stickman import Stickman, StickmanState, Direction

class Enemy(Stickman):
    ENEMY_SPRITE_SIZE = vec(50,50)
    ENEMY_HITBOX_SIZE = vec(30,50)

    ENEMY_MOVEMENT_SPEED = 150

    def __init__(self, position, hitboxSize = ENEMY_HITBOX_SIZE):
        super().__init__(position, hitboxSize, self.ENEMY_MOVEMENT_SPEED)
    
    def on_state_changed(self):
        match self.state:
            case StickmanState.IDLE:
                self.set_animation(ANIM_ENEMY_IDLE)
            case StickmanState.WALKING:
                self.set_animation(ANIM_ENEMY_WALKING)
            case StickmanState.JUMPING:
                self.set_animation(ANIM_PLAYER_JUMPING)
            case StickmanState.ATTACKING_FIRE:
                pass
                # todo
        
        if self.lookingDirection is Direction.RIGHT:
            self.animation.flip_horizontally()

    def set_animation(self, animInfos):
        pos = self.get_sprite_pos_centered_around_hitbox(self.ENEMY_SPRITE_SIZE)
        self.animation = Animation(animInfos, pos, self.ENEMY_SPRITE_SIZE)
        self.animation.start()

    def update_animation(self, dt: float):
        self.animation.update(dt)

    def apply_strategy(self):
        self.go_left()
        self.try_jump()

    def update(self, dt: float):
        self.apply_strategy()

        self.apply_gravity(dt)

        super().update_position(dt)

        self.update_animation(dt)

    def draw(self, surface):
        sprites_pos = self.get_sprite_pos_centered_around_hitbox(self.ENEMY_SPRITE_SIZE)
        self.animation.set_position(sprites_pos)
        self.animation.draw(surface)