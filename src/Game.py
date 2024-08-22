import pygame
from pygame.locals import *

from src.Player import Player

from src.ImageManager import ImageManager

from src.Constant import Constant

from src.Button import Button



vec = pygame.math.Vector2  # 2 for two dimensional
FramePerSec = pygame.time.Clock()

import src.Constant

class Game():
    __player: Player
    __displaysurface = None
    __spritegroup = pygame.sprite.Group()

    def __init__(self):
        print("Hello")
        pygame.init()


        self.__displaysurface = pygame.display.set_mode((Constant.WINDOW_WIDTH, Constant.WINDOW_HEIGHT))
        pygame.display.set_caption("Game")

        ImageManager().load_image('./assets/textures/player_default.png', 'player')
        ImageManager().load_image('./assets/textures/play_button.png', 'play_button')
        ImageManager().load_image('./assets/textures/options_button.png', 'options_button')
        ImageManager().load_image('./assets/textures/logo.png', 'logo')


        self.__player = Player()
        self.main_menu()

    def run(self):
        print("Game is running")
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            self.__displaysurface.fill((0,0,0))

            self.__player.draw(self.__displaysurface)

            self.__player.update(1 / 60)

            pygame.display.update()
            FramePerSec.tick(Constant.FPS)

    def main_menu(self):
        pygame.display.set_caption("Main Menu")
        play_button = Button('play_button', (Constant.WINDOW_WIDTH/2, Constant.WINDOW_HEIGHT/2), scale=(150, 75))
        options_button = Button('options_button', (Constant.WINDOW_WIDTH/2, Constant.WINDOW_HEIGHT/2+100), scale=(150, 75))

        logo_image = ImageManager().get_image('logo')
        logo_rect = logo_image.get_rect(center=(Constant.WINDOW_WIDTH/2, Constant.WINDOW_HEIGHT/5))


        while True:
            self.__displaysurface.fill((0, 0, 0))
            MENU_MOUSE_POS = pygame.mouse.get_pos()

            play_button.draw(self.__displaysurface)
            options_button.draw(self.__displaysurface)
            self.__displaysurface.blit(logo_image, logo_rect)

            for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == MOUSEBUTTONDOWN:
                        if play_button.is_clicked(MENU_MOUSE_POS):
                            self.run()
                        if options_button.is_clicked(MENU_MOUSE_POS):
                            print("Options")

            pygame.display.update()

if __name__ == "__main__":
    Game()