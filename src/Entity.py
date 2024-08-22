import pygame
from pygame.locals import *
vec = pygame.math.Vector2  # 2 for two dimensional

# Represents an object with a position and a velocity
class Entity():
    position: vec
    velocity: vec

    arbre: vec

    def __init__(self):
        self.position = vec(0,0)
        self.velocity = vec(0,0)

        self.arbre = vec(0,0)

    def reset_velocity(self):
        self.velocity = vec(0,0)

    def accelerate(self, acc: vec):
        self.velocity += acc

    def apply_gravity(self, deltaTime: float):
        self.accelerate(deltaTime * vec(0, 981))

    def set_position(self, newPos: vec):
        self.position = newPos

    def update_position(self, deltaTime: float):
        self.position += deltaTime * self.velocity