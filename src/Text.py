from pygame import Color

from src.Entity import Entity
from src.FontManager import FontManager

import pygame

vec = pygame.math.Vector2  # 2 for two dimensional

class Text(Entity):

    __font: pygame.font.Font

    def __init__(self, position: vec, text: str, color=Color(0,0,0), font='default', font_size=12):
        super().__init__()
        self.position = position
        if not pygame.font.get_init():
            pygame.font.init()
        self.__font = FontManager().get_font(font)
        self.color = color
        self.text = text

    def load_font(self, key: str):
        self.__font = FontManager().get_font(key)

    def update_text(self, text: str):
        self.text = text

    def update_position(self, new_position: vec):
        self.position = new_position

    def update_color(self, color: pygame.Color):
        self.color = color

    def draw(self, surface: pygame.Surface):
        surface.blit(self.__font.render(self.text, True, self.color), self.position)

    def draw_center(self, surface: pygame.Surface):
        size = self.__font.size(self.text)
        width, height = size
        width /= 2
        height /= 2
        old_pos = self.position
        self.update_position(vec(self.position.x - width, self.position.y - height))
        self.draw(surface)
        self.position = old_pos
