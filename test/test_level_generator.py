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

    # level_test_1 as 1 fire and 2 spawn points
    # level_test_2 as 0 fire and 2 spawn points
    # level_test_3 as 2 fire and 2 spawn points
    # level_test_4 as 1 fire and 1 spawn points
    # level_test_5 as 1 fire and 5 spawn points

    def test_level_ok(self):
        platforms, fire, spawn_points = LevelGenerator().load_level_infos('./assets/levels/level_test1.png')
        assert platforms is not None
        assert fire is not None
        assert spawn_points is not None and 4 >= len(spawn_points) > 1

    def test_level_with_no_fire(self):
        try:
            platforms, fire, spawn_points = LevelGenerator().load_level_infos('./assets/levels/level_test2.png')
            assert False
        except Exception:
            assert True

    def test_level_with_two_fire(self):
        try:
            platforms, fire, spawn_points = LevelGenerator().load_level_infos('./assets/levels/level_test3.png')
            assert False
        except Exception:
            assert True

    def test_level_with_not_enough_spawn_points(self):
        try:
            platforms, fire, spawn_points = LevelGenerator().load_level_infos('./assets/levels/level_test4.png')
            assert False
        except Exception:
            assert True

    def test_level_with_too_many_spawn_points(self):
        try:
            platforms, fire, spawn_points = LevelGenerator().load_level_infos('./assets/levels/level_test5.png')
            assert False
        except Exception:
            assert True
