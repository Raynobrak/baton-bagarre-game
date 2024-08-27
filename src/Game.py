import pygame
from pygame.locals import *

from src.AudioManager import AudioManager
from src.FontManager import FontManager
from src.LevelGenerator import LevelGenerator
from src.OptionView import OptionView
from src.Player import Player
from src.Animation import SpritesheetAnimInfos, Animation
from src.CollisionUtils import *
from src.ImageManager import ImageManager
from src.Constant import Constant
from src.Button import Button
from src.MainMenu import MainMenu

from src.Fire import Fire

vec = pygame.math.Vector2  # 2 for two dimensional
FramePerSec = pygame.time.Clock()

import src.Constant


class Game():
    __displaysurface = None
    __spritegroup = pygame.sprite.Group()

    def __init__(self):
        pygame.init()
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, 1)

        self.__displaysurface = pygame.display.set_mode((Constant.WINDOW_WIDTH, Constant.WINDOW_HEIGHT))
        pygame.display.set_caption("Game")

        self.load_all_images()

        self.__player = Player(vec(100, 100))

        self.__fire = Fire(600, 500, 100, 100)  # Initialize Fire object here

        self.main_menu()

    def load_all_images(self):
        ImageManager().load_image('./assets/textures/player_default.png', 'player')

        ImageManager().load_image('./assets/textures/background.png', 'background')
        ImageManager().load_image('./assets/textures/background2.png', 'background2')
        ImageManager().load_image('./assets/textures/background3.png', 'background3')
        ImageManager().load_image('./assets/textures/platform_left.png', 'platform_left')
        ImageManager().load_image('./assets/textures/platform_mid_1.png', 'platform_mid_1')
        ImageManager().load_image('./assets/textures/platform_mid_2.png', 'platform_mid_2')
        ImageManager().load_image('./assets/textures/platform_right.png', 'platform_right')

        ImageManager().load_image('./assets/textures/player_idle.png', 'player_idle')
        ImageManager().load_image('./assets/textures/player_move.png', 'player_walking')

        ImageManager().load_image('./assets/textures/player_jump.png', 'player_jumping')
        ImageManager().load_image('./assets/textures/player_attack.png', 'player_punch')
        ImageManager().load_image('./assets/textures/player_kick.png', 'player_kick')
        ImageManager().load_image('./assets/textures/player_yoga.png', 'player_levitating')

        ImageManager().load_image('./assets/textures/enemy_idle.png', 'enemy_idle')
        ImageManager().load_image('./assets/textures/enemy_move.png', 'enemy_walking')
        ImageManager().load_image('./assets/textures/enemy_water_bucket.png', 'enemy_water_bucket')

        ImageManager().load_image('./assets/textures/fire_big.png', 'fire_big')
        ImageManager().load_image('./assets/textures/fire_medium.png', 'fire_medium')
        ImageManager().load_image('./assets/textures/fire_small.png', 'fire_small')
        ImageManager().load_image('./assets/textures/fire_very_small.png', 'fire_very_small')

        ImageManager().load_image('./assets/textures/play_button.png', 'play_button')
        ImageManager().load_image('./assets/textures/options_button.png', 'options_button')
        ImageManager().load_image('./assets/textures/logo.png', 'logo')

        AudioManager().load_sound('./assets/audio/BatonBagarre.mp3', 'music')

        FontManager().load_font('./assets/font/upheavtt.ttf','default')

        FontManager().load_font('./assets/font/upheavtt.ttf','menu', font_size=50)

    def run(self):
        dt = 1 / 60

        # Load level

        bg = pygame.transform.smoothscale(ImageManager().get_image('background2'),
                                          (Constant.WINDOW_WIDTH, Constant.WINDOW_HEIGHT))
        platforms, fire = LevelGenerator().load_level_infos('./assets/levels/level1.png')

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit(0)

                # Keyup events only can be done in the main loop
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_e:
                        self.__player.stop_levitate()

            self.__player.update(dt, self.__fire)

            self.__player.check_collision_with_walls(vec(Constant.WINDOW_WIDTH, Constant.WINDOW_HEIGHT))

            for platform in platforms:
                handle_collision_player_vs_platform(self.__player, platform)

            # Draw Level
            self.__displaysurface.blit(bg, (0, 0))
            for platform in platforms:
                platform.draw(self.__displaysurface)

            # Update and draw fire object
            self.__fire.update(dt)
            self.__fire.draw(self.__displaysurface)

            self.__player.draw(self.__displaysurface)

            pygame.display.update()

            FramePerSec.tick(Constant.FPS)

    def main_menu(self):
        main_menu = MainMenu(self.__displaysurface)
        option_menu = OptionView(self.__displaysurface)
        while True:

            action = main_menu.display_menu()
            if action == 'play':
                AudioManager().play_music()
                self.run()
            elif action == 'options':
                print("option")
                action = option_menu.display_option()


if __name__ == "__main__":
    Game()
