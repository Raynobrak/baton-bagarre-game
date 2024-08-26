# src/MainMenu.py
import pygame
from pygame.locals import *
from src.Button import Button
from src.ImageManager import ImageManager
from src.Constant import Constant

class MainMenu:
    def __init__(self, displaysurface):
        self.displaysurface = displaysurface
        self.play_button = Button('play_button', (Constant.WINDOW_WIDTH/2, Constant.WINDOW_HEIGHT/2), scale=(150, 75))
        self.options_button = Button('options_button', (Constant.WINDOW_WIDTH/2, Constant.WINDOW_HEIGHT/2+100), scale=(150, 75))
        self.logo_image = ImageManager().get_image('logo')
        self.logo_rect = self.logo_image.get_rect(center=(Constant.WINDOW_WIDTH/2, Constant.WINDOW_HEIGHT/5))

    def display_menu(self):
        pygame.display.set_caption("Main Menu")
        while True:
            self.displaysurface.fill((0, 0, 0))
            menu_mouse_pos = pygame.mouse.get_pos()

            self.play_button.draw(self.displaysurface)
            self.options_button.draw(self.displaysurface)
            self.displaysurface.blit(self.logo_image, self.logo_rect)

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    if self.play_button.is_clicked(menu_mouse_pos):
                        return 'play'
                    if self.options_button.is_clicked(menu_mouse_pos):
                        return 'options'

            pygame.display.update()