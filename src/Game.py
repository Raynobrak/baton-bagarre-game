import pygame
from pygame.locals import *

from src.LevelGenerator import LevelGenerator
from src.Player import Player
from src.Animation import SpritesheetAnimInfos, Animation

from src.ImageManager import ImageManager

from src.Constant import Constant

vec = pygame.math.Vector2  # 2 for two dimensional
FramePerSec = pygame.time.Clock()

import src.Constant

class Game():
    __displaysurface = None
    __spritegroup = pygame.sprite.Group()

    def __init__(self):
        print("Hello")
        pygame.init()

        self.__displaysurface = pygame.display.set_mode((Constant.WINDOW_WIDTH, Constant.WINDOW_HEIGHT))
        pygame.display.set_caption("Game")

        self.load_all_images()
        self.anim_test = Animation(src.Animation.ANIM_PLAYER_IDLE, vec(100,100), vec(50,50))
        self.anim_test.start()

        self.__player = Player(vec(50,50))
        self.run()

    def load_all_images(self):
        ImageManager().load_image('./assets/textures/player_default.png', 'player')

        ImageManager().load_image('./assets/textures/background.png', 'background')
        ImageManager().load_image('./assets/textures/platform_left.png', 'platform_left')
        ImageManager().load_image('./assets/textures/platform_mid_1.png', 'platform_mid_1')
        ImageManager().load_image('./assets/textures/platform_mid_2.png', 'platform_mid_2')
        ImageManager().load_image('./assets/textures/platform_right.png', 'platform_right')

        ImageManager().load_image('./assets/textures/player_idle.png', 'player_idle')
        ImageManager().load_image('./assets/textures/player_move.png', 'player_walking')

        ImageManager().load_image('./assets/textures/player_jump.png', 'player_jumping')
        ImageManager().load_image('./assets/textures/player_attack.png', 'player_punch')
        ImageManager().load_image('./assets/textures/player_kick.png', 'player_kick')

        ImageManager().load_image('./assets/textures/enemy_idle.png', 'enemy_idle')
        ImageManager().load_image('./assets/textures/enemy_move.png', 'enemy_walking')
        ImageManager().load_image('./assets/textures/enemy_water_bucket.png', 'enemy_water_bucket')

        ImageManager().load_image('./assets/textures/fire_big.png', 'fire_big')
        ImageManager().load_image('./assets/textures/fire_medium.png', 'fire_medium')
        ImageManager().load_image('./assets/textures/fire_small.png', 'fire_small')
        ImageManager().load_image('./assets/textures/fire_very_small.png', 'fire_very_small')

    def run(self):
        print("Game is running")

        # Load level
        bg = pygame.transform.smoothscale(ImageManager().get_image('background'), (Constant.WINDOW_WIDTH, Constant.WINDOW_HEIGHT))
        platforms,fire = LevelGenerator().load_level_infos('./assets/levels/level1.png')

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    self.anim_test.flip_vertically()
                    self.anim_test.set_position(vec(10,10))
                    self.anim_test.set_size(vec(20,20))
            
            self.__player.update(1 / 60)

            self.__player.check_collision_with_walls(vec(Constant.WINDOW_WIDTH, Constant.WINDOW_HEIGHT))

            # Draw Level
            self.__displaysurface.blit(bg, (0,0))
            for platform in platforms:
                platform.draw(self.__displaysurface)

            self.anim_test.update(1 / 60)

            self.__player.draw(self.__displaysurface)
            self.anim_test.draw(self.__displaysurface)

            pygame.display.update()
            FramePerSec.tick(Constant.FPS)

if __name__ == "__main__":
    Game()