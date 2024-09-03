import pygame

from enum import Enum

import math

from src.CooldownVariable import CooldownVariable
from src.Animation import *
from src.ImageManager import ImageManager
from src.Stickman import Stickman, StickmanState, Direction
from src.Entity import Entity
from src.Enemy import Enemy

class EnemyParticle(Entity):
    PARTICLE_LIFETIME = 1

    def __init__(self, position, size, velocity, image):
        super().__init__(position, size, velocity)
        self.image = pygame.transform.scale(image, size)
        self.lifetime = self.PARTICLE_LIFETIME

    def update(self, dt):
        self.lifetime -= dt
        self.apply_gravity(dt)
        self.update_position(dt)

    def needs_to_disappear(self):
        return self.lifetime <= 0

    def draw(self, surface):
        percentage = self.lifetime / self.PARTICLE_LIFETIME
        self.image.set_alpha(int(percentage * 255))
        surface.blit(self.image, self.get_hitbox())
