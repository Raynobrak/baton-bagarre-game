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

        self.set_animation(ANIM_FIRE_BIG)

        self.lifePoints = 100

    def set_animation(self, animInfos):
        self.animation = Animation(animInfos, self.position, self.size)
        self.animation.set_position(self.position)
        self.animation.start()  # Ensure the animation is started

    def update_animation(self, dt: float):
        self.animation.update(dt)
        self.animation.set_position(self.position)

    def update_life_animation(self, newLifePoints=None):
        if newLifePoints is not None:
            self.lifePoints = newLifePoints

            if self.lifePoints >= 75:
                self.set_animation(ANIM_FIRE_BIG)
            elif self.lifePoints >= 50:
                self.set_animation(ANIM_FIRE_MEDIUM)
            elif self.lifePoints >= 25:
                self.set_animation(ANIM_FIRE_SMALL)
            else:
                self.set_animation(ANIM_FIRE_VERY_SMALL)


    def update(self, dt: float):
        self.update_life_animation()
        self.update_animation(dt)

    def draw(self, display):
        self.animation.draw(display)