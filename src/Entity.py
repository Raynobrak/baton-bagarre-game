import pygame
from pygame.locals import *
vec = pygame.math.Vector2  # 2 for two dimensional

# Represents an object with a position and a velocity
class Entity():
    def __init__(self, position = vec(0,0), size = vec(0,0), vel = vec(0,0)):
        self.position = position
        self.size = size
        self.velocity = vel

    def reset_velocity(self):
        self.velocity = vec(0,0)

    def stop_vertically(self):
        self.velocity.x = 0

    def stop_horizontally(self):
        self.velocity.y = 0

    def accelerate(self, acc: vec):
        self.velocity += acc

    def apply_gravity(self, deltaTime: float):
        self.accelerate(deltaTime * vec(0, 981))

    def move(self, delta):
        self.position += delta

    def set_position(self, newPos: vec):
        self.position = newPos

    def update_position(self, deltaTime: float):
        self.position += deltaTime * self.velocity

    def get_hitbox(self) -> pygame.Rect:
        return pygame.Rect(self.position, self.size)
    
    def get_sprite_pos_centered_around_hitbox(self, spriteSize: vec) -> vec:
        hb = self.get_hitbox()
        return hb.center - spriteSize / 2