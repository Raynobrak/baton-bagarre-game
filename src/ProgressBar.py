import math

from pygame import Color
from src.Entity import Entity
import pygame

vec = pygame.math.Vector2  # 2 for two dimensional


class ProgressBar(Entity):

    def __init__(self, position: vec, size: vec, color=None, back_color=None, max_value=None, current_value=None):
        super().__init__(position, size)
        if color is None:
            color = Color(0, 255, 0)
        if back_color is None:
            back_color = Color(255, 0, 0)
        if max_value is None:
            max_value = 100
        if current_value is None:
            current_value = 100

        self.color = color
        self.back_color = back_color
        self.max_value = max_value
        self.current_value = current_value

    def set_value(self, value):
        self.current_value = value

    def set_center(self, centerPosition: vec):
        self.set_position(centerPosition - self.size / 2)

    def draw(self, surface: pygame.Surface):
        # Draw a border around the bar
        border_size = 2
        pygame.draw.rect(surface, Color(0, 0, 0), pygame.rect.Rect(self.position - vec(border_size, border_size), self.size + 2*vec(border_size, border_size)), border_size)
        # Draw the background and the bar
        pygame.draw.rect(surface, self.back_color, pygame.rect.Rect(self.position, self.size))
        pygame.draw.rect(surface, self.color, pygame.rect.Rect(self.position, (self.size.x * self.current_value / self.max_value, self.size.y)))


