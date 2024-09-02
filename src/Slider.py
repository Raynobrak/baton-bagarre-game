import pygame
vec = pygame.math.Vector2  # 2 for two dimensional

class Slider:

    def __init__(self, position: vec, size:vec, initialvalue: float = 1.0):
        self.position = position
        self.size = size
        self.value = initialvalue

        self.border_rect = pygame.Rect(position, size)
        self.button_rect = pygame.Rect(vec(position.x + size.x * initialvalue, position.y), vec(10,size.y))

        self.is_grabbing = False


    def render(self,surface: pygame.Surface):
        self.button_rect.x = self.position.x + self.size.x * self.value
        pygame.draw.rect(surface, pygame.Color('grey'), self.border_rect)
        pygame.draw.rect(surface,pygame.Color('blue'),self.button_rect)

    def update_slider(self, mouse_pos: vec):
        if self.border_rect.collidepoint(mouse_pos):
            self.value = (mouse_pos.x - self.border_rect.x) / self.border_rect.width

    def start_grabbing(self):
        self.is_grabbing = True

    def update_grabing_position(self, mouse_pos: vec):
        if self.border_rect.x > mouse_pos.x:
            self.value = 0
            return
        if self.border_rect.x + self.size.x < mouse_pos.x:
            self.value = 1.0
            return

        self.value = (mouse_pos.x - self.border_rect.x) / self.border_rect.width

    def stop_grabbing(self):
        self.is_grabbing = False

    def is_grabed(self):
        return self.is_grabbing
