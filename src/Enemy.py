import pygame

from enum import Enum

import math

from src.CooldownVariable import CooldownVariable
from src.Animation import *
from src.ImageManager import ImageManager
from src.Stickman import Stickman, StickmanState, Direction
from src.Entity import Entity

class Enemy(Stickman):
    ENEMY_SPRITE_SIZE = vec(50,50)
    ENEMY_HITBOX_SIZE = vec(30,50)

    ENEMY_MOVEMENT_SPEED = 150

    ENEMY_DAMAGE_ANIMATION_TIME = 0.7

    def __init__(self, position, hitboxSize = ENEMY_HITBOX_SIZE):
        super().__init__(position, hitboxSize, self.ENEMY_MOVEMENT_SPEED)
        self.target = None

        self.isTakingDamage = False
        self.damageAnimationTimeLeft = self.ENEMY_DAMAGE_ANIMATION_TIME
    
    def on_state_changed(self):
        match self.state:
            case StickmanState.IDLE:
                self.set_animation(ANIM_ENEMY_IDLE)
            case StickmanState.WALKING:
                self.set_animation(ANIM_ENEMY_WALKING)
            case StickmanState.JUMPING:
                self.set_animation(ANIM_ENEMY_JUMPING)
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
        self.goto_target()
        #self.go_left()
        #self.try_jump()

    def take_damage(self, damage):
        # todo: reduce health
        self.isTakingDamage = True
        self.damageAnimationTimeLeft = self.ENEMY_DAMAGE_ANIMATION_TIME

    def goto_target(self):
        if self.target is None:
            return
        
        dist = self.position.distance_to(self.target.position)
        if dist < 100:
            self.go_idle()
            return

        if self.position.x > self.target.position.x:
            self.go_left()
        else:
            self.go_right()
        
        if self.position.y > self.target.position.y:
            print("enemy: ", self.position.y, "player: ", self.target.position.y)
            self.try_jump()

    def update(self, dt: float):
        if not self.isTakingDamage:
            self.apply_strategy()

        self.apply_gravity(dt)

        super().update_position(dt)

        self.update_animation(dt)

        if self.isTakingDamage:
            self.damageAnimationTimeLeft -= dt
            if self.damageAnimationTimeLeft <= 0:
                self.isTakingDamage = False

    def set_target(self, target: Entity):
        self.target = target

    def draw(self, surface):
        sprites_pos = self.get_sprite_pos_centered_around_hitbox(self.ENEMY_SPRITE_SIZE)
        self.animation.set_position(sprites_pos)

        if not self.isTakingDamage:
            self.animation.draw(surface)
        else:
            blink_count = 10
            percentage = self.damageAnimationTimeLeft / self.ENEMY_DAMAGE_ANIMATION_TIME
            current_value = math.sin(percentage * blink_count * math.pi)
            if current_value > 0:
                red_filter = pygame.Surface(self.ENEMY_SPRITE_SIZE)
                red_filter.fill((255, 0, 0))  # (Rouge, Vert, Bleu, Alpha)
                self.animation.draw(surface, red_filter)
            else:
                self.animation.draw(surface)
