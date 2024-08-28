import pygame

from src.Entity import Entity
from src.ImageManager import ImageManager
from src.Animation import *
from src.Constant import *

vec = pygame.math.Vector2  # 2 for two dimensional

class SpawnPoint(Entity):
    def __init__(self, pos: vec, size: vec):
        super().__init__(pos, size)