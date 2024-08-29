import pygame

from src.Entity import Entity
from src.ImageManager import ImageManager
from src.Animation import *
from src.Constant import *

vec = pygame.math.Vector2  # 2 for two dimensional


class Fire(Entity):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.set_position(vec(x, y))
        self.size = vec(width, height)

        self.current_animation = None  # Track current animation
        self.set_animation(ANIM_FIRE_BIG)

        self.lifePoints = Constant.FIRE_HEALTH  # Initialize life points
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
            if self.lifePoints - Constant.FIRE_DAMAGE_PER_SECOND < 0:
                self.lifePoints = 0
            else:
                self.lifePoints -= Constant.FIRE_DAMAGE_PER_SECOND

            self.time_since_last_reduction = 0
            print(f"Fire life points: {self.lifePoints}")

    def reignite(self):
        self.lifePoints = min(self.lifePoints + Constant.REIGNITE_HEALING, Constant.FIRE_HEALTH)
        print(f"Fire is healed: {self.lifePoints}")

    def get_position(self):
        return self.position

    def update(self, dt: float):
        self.reduce_life_points(dt)
        self.update_life_animation()
        self.update_animation(dt)

    def draw(self, display):
        self.animation.draw(display)
