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

        self.life_points = Constant.FIRE_HEALTH  # Initialize life points
        self.time_since_last_reduction = 0  # Track time since last reduction
        self.has_lifePoints_changed_since_last_update = False

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
        if self.life_points >= 75:
            self.set_animation(ANIM_FIRE_BIG)
        elif self.life_points >= 50:
            self.set_animation(ANIM_FIRE_MEDIUM)
        elif self.life_points >= 25:
            self.set_animation(ANIM_FIRE_SMALL)
        else:
            self.set_animation(ANIM_FIRE_VERY_SMALL)

    def remove_life_points(self, damage: int):
        self.set_life_points(self.life_points - damage)

    def add_life_points(self, healing: int):
        self.set_life_points(self.life_points + healing)

    def set_life_points(self, life_points: int):
        if life_points < 0:
            self.life_points = 0
        elif life_points > Constant.FIRE_HEALTH:
            self.life_points = Constant.FIRE_HEALTH
        else:
            self.life_points = life_points
        self.has_lifePoints_changed_since_last_update = True

    def reduce_life_points_per_time(self, dt: float):
        self.time_since_last_reduction += dt

        if self.time_since_last_reduction >= 1:  # Reduce life points every second
            self.remove_life_points(Constant.FIRE_DAMAGE_PER_SECOND)
            self.time_since_last_reduction = 0

    def reignite(self):
        self.add_life_points(Constant.REIGNITE_HEALING)

    def splash(self):
        self.remove_life_points(Constant.WATER_BUCKET_DAMAGE)

    def get_position(self):
        return self.position

    def update(self, dt: float):
        self.has_lifePoints_changed_since_last_update = False
        self.reduce_life_points_per_time(dt)
        self.update_life_animation()
        self.update_animation(dt)

    def has_life_points_changed(self):
        return self.has_lifePoints_changed_since_last_update

    def draw(self, display):
        self.animation.draw(display)
