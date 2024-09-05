import pygame
from pygame.locals import *

from src.FontManager import FontManager
from src.ImageManager import ImageManager
from src.Constant import Constant

# This class is responsible for displaying the main menu
# It displays the game logo, and four buttons: "Play", "Options", "Controls", and "Quit"
class MainMenu:
    def __init__(self, displaysurface):
        self.displaysurface = displaysurface
        self.font = FontManager().get_font('menu')

        # Set the color of the text
        self.color = (255, 255, 255)

        # Create text objects for the buttons
        self.play_text = self.font.render('Play', True, self.color)
        self.options_text = self.font.render('Options', True, self.color)
        self.controls_text = self.font.render('Controls', True, self.color)
        self.quit_text = self.font.render('Quit', True, self.color)

        # Create rectangles for the text objects
        self.play_rect = self.play_text.get_rect(center=(
            Constant.WINDOW_WIDTH / 2, Constant.WINDOW_HEIGHT / 2 - 100))
        self.options_rect = self.options_text.get_rect(
            center=(Constant.WINDOW_WIDTH / 2, Constant.WINDOW_HEIGHT / 2))
        self.controls_rect = self.controls_text.get_rect(center=(
            Constant.WINDOW_WIDTH / 2, Constant.WINDOW_HEIGHT / 2 + 100))
        self.quit_rect = self.quit_text.get_rect(center=(
            Constant.WINDOW_WIDTH / 2, Constant.WINDOW_HEIGHT / 2 + 200))

        # Load the game logo
        self.logo_image = ImageManager().get_image('logo')

        # Create a rectangle for the logo
        self.logo_rect = self.logo_image.get_rect(
            center=(Constant.WINDOW_WIDTH / 2, Constant.WINDOW_HEIGHT / 5))

        # Initialize the hovered option and selected option
        self.hovered_option = None
        self.selected_option = 0  # 0 for 'Play', 1 for 'Options', 2 for 'Controls', 3 for 'Quit'

    # Display the main menu
    def display_menu(self):
        pygame.display.set_caption("Main Menu")
        while True:
            self.displaysurface.fill((0, 0, 0))
            menu_mouse_pos = pygame.mouse.get_pos()

            self.handle_mouse_hover(menu_mouse_pos)

            # Set the color of the text based on whether it is hovered over or selected
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

            # Render the text objects
            self.play_text = self.font.render('Play', True, play_color)
            self.options_text = self.font.render('Options', True, options_color)
            self.controls_text = self.font.render('Controls', True,controls_color)
            self.quit_text = self.font.render('Quit', True, quit_color)

            # Blit the text objects onto the display surface
            self.displaysurface.blit(self.play_text, self.play_rect)
            self.displaysurface.blit(self.options_text, self.options_rect)
            self.displaysurface.blit(self.controls_text, self.controls_rect)
            self.displaysurface.blit(self.quit_text, self.quit_rect)
            self.displaysurface.blit(self.logo_image, self.logo_rect)

            # Check for events
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()

                # If the user clicks the mouse
                if event.type == MOUSEBUTTONDOWN:

                    if self.play_rect.collidepoint(menu_mouse_pos):
                        return 'play'
                    if self.options_rect.collidepoint(menu_mouse_pos):
                        return 'options'
                    if self.controls_rect.collidepoint(menu_mouse_pos):
                        return 'controls'
                    if self.quit_rect.collidepoint(menu_mouse_pos):
                        pygame.quit()
                        exit()

                # If the user presses a key
                if event.type == KEYDOWN:
                    if event.key == K_UP or event.key == K_DOWN:
                        self.selected_option = (self.selected_option + 1) % 4 \
                            if event.key == K_DOWN else (self.selected_option - 1) % 4
                    if event.key == K_RETURN:
                        if self.selected_option == 0:
                            return 'play'
                        elif self.selected_option == 1:
                            return 'options'
                        elif self.selected_option == 2:
                            return 'controls'
                        elif self.selected_option == 3:
                            pygame.quit()
                            exit()

            pygame.display.update()

    # Handle mouse hover
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
