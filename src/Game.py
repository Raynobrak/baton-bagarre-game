import pygame
from pygame.locals import *

from src.AudioManager import AudioManager
from src.FontManager import FontManager
from src.LevelGenerator import LevelGenerator
from src.OptionView import OptionView
from src.Player import Player
from src.Enemy import Enemy
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
    DELTA_TIME = 1 / Constant.FPS

    def __init__(self):
        pygame.init()
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, 1)

        self.__displaysurface = pygame.display.set_mode((Constant.WINDOW_WIDTH, Constant.WINDOW_HEIGHT))
        pygame.display.set_caption("Game")

        self.load_all_images()
        
        self.visibility = 1

        self.__player = Player(vec(100,100))
        self.enemy = Enemy(vec(900,100))

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

        ImageManager().load_image('./assets/textures/player_move.png', 'player_reignite') # todo fix this

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

        ImageManager().load_image('./assets/textures/circle.png', 'circle')

        AudioManager().load_sound('./assets/audio/BatonBagarre.mp3', 'music')

        FontManager().load_font('./assets/font/upheavtt.ttf','default')

        FontManager().load_font('./assets/font/upheavtt.ttf','menu', font_size=50)


    def run(self):
        dt = 1 / 60

        # Load level
        bg = pygame.transform.smoothscale(ImageManager().get_image('background2'),
                                          (Constant.WINDOW_WIDTH, Constant.WINDOW_HEIGHT))
        platforms, fire = LevelGenerator().load_level_infos('./assets/levels/level1.png')

        original_circle = ImageManager().get_image('circle')

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()

            self.__player.update(self.DELTA_TIME)
            self.enemy.update(self.DELTA_TIME)

            self.__player.check_collision_with_walls(vec(Constant.WINDOW_WIDTH, Constant.WINDOW_HEIGHT))
            self.enemy.check_collision_with_walls(vec(Constant.WINDOW_WIDTH, Constant.WINDOW_HEIGHT))

            for platform in platforms:
                handle_collision_stickman_vs_platform(self.__player, platform)
                handle_collision_stickman_vs_platform(self.enemy, platform)

            # Draw Level
            self.__displaysurface.blit(bg, (0, 0))
            for platform in platforms:
                platform.draw(self.__displaysurface)

            # Update and draw fire object
            fire.update(dt)
            fire.draw(self.__displaysurface)

            self.__player.draw(self.__displaysurface)
            self.enemy.draw(self.__displaysurface)

            # Center the circle with the fire and scale it based on fire's life points
            fire_pos = fire.get_position()
            fire_size = fire.size
            fire_life_points = fire.lifePoints

            # Calculate new size for the circle
            max_circle_size = 200  # Maximum size of the circle
            min_circle_size = 50   # Minimum size of the circle
            circle_size = min_circle_size + (max_circle_size - min_circle_size) * (fire_life_points / Constant.FIRE_HEALTH)

            # Scale the circle image
            circle = pygame.transform.smoothscale(original_circle, (int(circle_size), int(circle_size)))

            # Calculate position to center the circle with the fire
            circle_pos = (fire_pos.x + fire_size.x / 2 - circle.get_width() / 2,
                          fire_pos.y + fire_size.y / 2 - circle.get_height() / 2)

            filter = pygame.surface.Surface((Constant.WINDOW_WIDTH, Constant.WINDOW_HEIGHT))
            filter.fill(pygame.color.Color('white'))
            filter.set_alpha(200)
            filter.blit(circle, circle_pos)
            self.__displaysurface.blit(filter, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
            pygame.display.flip()

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
