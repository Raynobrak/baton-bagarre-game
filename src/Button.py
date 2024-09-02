import pygame
from src.ImageManager import ImageManager


class Button:
    def __init__(self, image_key, pos, scale=None):
        self.image = ImageManager().get_image(image_key)
        if scale:
            self.image = pygame.transform.scale(self.image, scale)
        self.rect = self.image.get_rect(center=pos)
        self.hovered = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
