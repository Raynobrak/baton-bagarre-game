import pygame
from pygame.locals import *
vec = pygame.math.Vector2  # 2 for two dimensional

# Represents an object with a position and a velocity
class Entity():
    __position: vec
    __velocity: vec

    def __init__(self):
        self.__position = vec(0,0)
        self.__velocity = vec(0,0)

    def reset_velocity(self):
        self.__velocity = vec(0,0)

    def accelerate(self, acc: vec):
        self.__velocity += acc

    def set_position(self, newPos: vec):
        self.__position = newPos

    def update_position(self, deltaTime: float):
        self.__position += deltaTime * self.__velocity