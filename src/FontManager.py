import pygame

class FontManager:
    fonts = dict()  # static attribute

    def __init__(self):
        pass

    def load_font(self, path, key):
        font = pygame.font.Font(path)
        FontManager.fonts.update({key: font})

    def get_font(self, key):
        return FontManager.fonts[key]