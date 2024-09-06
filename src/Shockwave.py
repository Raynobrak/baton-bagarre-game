from enum import Enum

import pygame
from pygame.locals import *

from src.CollisionUtils import *
from src.Entity import Entity
from src.Enemy import Enemy
from src.Animation import *
from src.CooldownVariable import CooldownVariable
from src.Fire import Fire
from src.ImageManager import ImageManager
from src.Stickman import Stickman, StickmanState, Direction

vec = pygame.math.Vector2  # 2 for two dimensional

class Shockwave():
    SHOCKWAVE_RADIUS = 200
    SHOCKWAVE_RADIUS_SQUARED = SHOCKWAVE_RADIUS * SHOCKWAVE_RADIUS
    SHOCKWAVE_ANIMATION_DURATION = 3
    SHOCKWAVE_EFFECT_DURATION = 0.01
    SHOCKWAVE_DMG = 1000 # shockwave one-shots enemies
    SHOCKWAVE_IMPULSE = 800

    SHOCKWAVE_RED = 0
    SHOCKWAVE_GREEN = 130
    SHOCKWAVE_BLUE = 194

    def __init__(self, center: vec):
        self.center = center
        self.timeRemaining = self.SHOCKWAVE_ANIMATION_DURATION

    def update(self, dt):
        self.timeRemaining -= dt

    def apply_to_enemy(self, enemy):
        if self.timeRemaining < self.SHOCKWAVE_ANIMATION_DURATION - self.SHOCKWAVE_EFFECT_DURATION:
            return # explosion finished
        
        enemyCenter = vec(enemy.get_hitbox().center)

        delta = enemyCenter - self.center
        distanceSquared = delta.length_squared()

        if distanceSquared < self.SHOCKWAVE_RADIUS_SQUARED:
            dir = delta.normalize()
            impulse = dir * self.SHOCKWAVE_IMPULSE
            enemy.accelerate(impulse)
            enemy.take_damage(self.SHOCKWAVE_DMG)

    def is_active(self):
        return self.timeRemaining > 0
    
    def topleft(self):
        return self.center - self.SHOCKWAVE_RADIUS * vec(1,1)
    
    def draw(self, surface):
        alpha = 255 * self.timeRemaining / self.SHOCKWAVE_ANIMATION_DURATION

        circle_surface = pygame.Surface(self.SHOCKWAVE_RADIUS * vec(2, 2), pygame.SRCALPHA)

        color = (self.SHOCKWAVE_RED, self.SHOCKWAVE_GREEN, self.SHOCKWAVE_BLUE, int(alpha))
        pygame.draw.circle(circle_surface, color, self.SHOCKWAVE_RADIUS * vec(1, 1), self.SHOCKWAVE_RADIUS)
        surface.blit(circle_surface, self.topleft())
