import pygame

from src.Entity import Entity
from src.ImageManager import ImageManager
from src.Animation import *

vec = pygame.math.Vector2  # 2 for two dimensional

class Fire(Entity):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.set_position(vec(x, y))
        self.size = vec(width, height)

        self.current_animation = None  # Track current animation
        self.set_animation(ANIM_FIRE_BIG)

        self.lifePoints = 100  # Initialize life points
        self.time_since_last_reduction = 0  # Track time since last reduction

    def set_animation(self, animInfos):
        if self.current_animation != animInfos:  # Only set animation if different
            self.animation = Animation(animInfos, self.position, self.size)
            self.animation.set_position(self.position)
            self.animation.start()
            self.current_animation = animInfos

    def update_animation(self, dt: float):
        self.animation.update(dt)
        self.animation.set_position(self.position)

    def update_life_animation(self):
        if self.lifePoints >= 75:
            self.set_animation(ANIM_FIRE_BIG)
        elif self.lifePoints >= 50:
            self.set_animation(ANIM_FIRE_MEDIUM)
        elif self.lifePoints >= 25:
            self.set_animation(ANIM_FIRE_SMALL)
        else:
            self.set_animation(ANIM_FIRE_VERY_SMALL)

    def reduce_life_points(self, dt: float):
        self.time_since_last_reduction += dt

        if self.time_since_last_reduction >= 1:  # Reduce life points every second
            self.lifePoints -= 1
            self.time_since_last_reduction = 0

    def update(self, dt: float):
        self.reduce_life_points(dt)
        self.update_life_animation()
        self.update_animation(dt)

    def draw(self, display):
        self.animation.draw(display)