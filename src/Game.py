# src/Game.py
import pygame
from pygame.locals import *
import sys
from src.Player import Player
from src.ImageManager import ImageManager
from src.Constant import Constant
from src.Button import Button
from src.MainMenu import MainMenu

vec = pygame.math.Vector2  # 2 for two dimensional
FramePerSec = pygame.time.Clock()

class Game:
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
        main_menu = MainMenu(self.__displaysurface)
        while True:
            action = main_menu.display_menu()
            if action == 'play':
                self.run()
            elif action == 'options':
                print("Options")

if __name__ == "__main__":
    Game()