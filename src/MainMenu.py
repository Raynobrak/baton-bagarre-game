import pygame
from pygame.locals import *
from src.ImageManager import ImageManager
from src.Constant import Constant


class MainMenu:
    def __init__(self, displaysurface):
        self.displaysurface = displaysurface
        self.font = pygame.font.Font('./assets/font/upheavtt.ttf', 50)
        self.play_text = self.font.render('Play', True, (255, 255, 255))
        self.options_text = self.font.render('Options', True, (255, 255, 255))
        self.controls_text = self.font.render('Controls', True, (255, 255, 255))
        self.quit_text = self.font.render('Quit', True, (255, 255, 255))
        self.play_rect = self.play_text.get_rect(center=(
            Constant.WINDOW_WIDTH / 2, Constant.WINDOW_HEIGHT / 2 - 100))
        self.options_rect = self.options_text.get_rect(
            center=(Constant.WINDOW_WIDTH / 2, Constant.WINDOW_HEIGHT / 2))
        self.controls_rect = self.controls_text.get_rect(center=(
            Constant.WINDOW_WIDTH / 2, Constant.WINDOW_HEIGHT / 2 + 100))
        self.quit_rect = self.quit_text.get_rect(center=(
            Constant.WINDOW_WIDTH / 2, Constant.WINDOW_HEIGHT / 2 + 200))
        self.logo_image = ImageManager().get_image('logo')
        self.logo_rect = self.logo_image.get_rect(
            center=(Constant.WINDOW_WIDTH / 2, Constant.WINDOW_HEIGHT / 5))
        self.hovered_option = None
        self.selected_option = 0  # 0 for 'Play', 1 for 'Options', 2 for 'Controls', 3 for 'Quit'

    def display_menu(self):
        pygame.display.set_caption("Main Menu")
        while True:
            self.displaysurface.fill((0, 0, 0))
            menu_mouse_pos = pygame.mouse.get_pos()

            self.handle_mouse_hover(menu_mouse_pos)

            play_color = (255, 255,
                          255) if self.hovered_option == 'play' or self.selected_option == 0 else (
            100, 100, 100)
            options_color = (255, 255,
                             255) if self.hovered_option == 'options' or self.selected_option == 1 else (
            100, 100, 100)
            controls_color = (255, 255,
                              255) if self.hovered_option == 'controls' or self.selected_option == 2 else (
            100, 100, 100)
            quit_color = (255, 255,
                          255) if self.hovered_option == 'quit' or self.selected_option == 3 else (
            100, 100, 100)

            self.play_text = self.font.render('Play', True, play_color)
            self.options_text = self.font.render('Options', True, options_color)
            self.controls_text = self.font.render('Controls', True,
                                                  controls_color)
            self.quit_text = self.font.render('Quit', True, quit_color)

            self.displaysurface.blit(self.play_text, self.play_rect)
            self.displaysurface.blit(self.options_text, self.options_rect)
            self.displaysurface.blit(self.controls_text, self.controls_rect)
            self.displaysurface.blit(self.quit_text, self.quit_rect)
            self.displaysurface.blit(self.logo_image, self.logo_rect)

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    if self.play_rect.collidepoint(menu_mouse_pos):
                        return 'play'
                    if self.options_rect.collidepoint(menu_mouse_pos):
                        return 'options'
                    if self.controls_rect.collidepoint(menu_mouse_pos):
                        return 'controls'
                    if self.quit_rect.collidepoint(menu_mouse_pos):
                        pygame.quit()
                        sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_UP or event.key == K_DOWN:
                        self.selected_option = (
                                                           self.selected_option + 1) % 4 if event.key == K_DOWN else (
                                                                                                                                 self.selected_option - 1) % 4
                    if event.key == K_RETURN:
                        if self.selected_option == 0:
                            return 'play'
                        elif self.selected_option == 1:
                            return 'options'
                        elif self.selected_option == 2:
                            return 'controls'
                        elif self.selected_option == 3:
                            pygame.quit()
                            sys.exit()

            pygame.display.update()

    def handle_mouse_hover(self, mouse_pos):
        if self.play_rect.collidepoint(mouse_pos):
            self.hovered_option = 'play'
        elif self.options_rect.collidepoint(mouse_pos):
            self.hovered_option = 'options'
        elif self.controls_rect.collidepoint(mouse_pos):
            self.hovered_option = 'controls'
        elif self.quit_rect.collidepoint(mouse_pos):
            self.hovered_option = 'quit'
        else:
            self.hovered_option = None
