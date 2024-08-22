import pygame

from src.Entity import Entity

vec = pygame.math.Vector2  # 2 for two dimensional
class Fire(Entity):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.set_position(vec(x,y))
        self.size = vec(width,height)

