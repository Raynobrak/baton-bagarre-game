import pygame

from src.LevelGenerator import LevelGenerator
from src.ImageManager import ImageManager
from src.Constant import Constant
from src.Game import Game


class TestLevelGenerator():

    pygame.init()
    # Set the video mode
    pygame.display.set_mode((Constant.WINDOW_WIDTH, Constant.WINDOW_HEIGHT))

    ImageManager().load_image('./assets/textures/platform_left.png', 'platform_left')
    ImageManager().load_image('./assets/textures/platform_mid_1.png', 'platform_mid_1')
    ImageManager().load_image('./assets/textures/platform_mid_2.png', 'platform_mid_2')
    ImageManager().load_image('./assets/textures/platform_right.png', 'platform_right')

    ImageManager().load_image('./assets/textures/fire_big.png', 'fire_big')
    ImageManager().load_image('./assets/textures/fire_medium.png', 'fire_medium')
    ImageManager().load_image('./assets/textures/fire_small.png', 'fire_small')
    ImageManager().load_image('./assets/textures/fire_very_small.png', 'fire_very_small')

    def test_level_ok(self):
        platforms, fire = LevelGenerator().load_level_infos('./assets/levels/level_test1.png')
        assert platforms is not None
        assert fire is not None

    def test_level_with_no_fire(self):
        platforms, fire = LevelGenerator().load_level_infos('./assets/levels/level_test3.png')
        assert platforms is None
        assert fire is None

    def test_level_with_two_fire(self):
        platforms, fire = LevelGenerator().load_level_infos('./assets/levels/level_test4.png')
        assert platforms is None
        assert fire is None