import math

import pygame
import src.UnmovablePlatform
import src.Constant
import src.Fire
import src.SpawnPoint

vec = pygame.math.Vector2  # 2 for two dimensional


class LevelGenerator:
    # Color matching
    LEFT_PLATFORM = (255, 0, 0)  # Left platform
    MID_1_PLATFORM = (255, 255, 0)  # Mid_1 platform
    MID_2_PLATFORM = (255, 0, 255)  # Mid_2 platform
    RIGHT_PLATFORM = (0, 255, 0)  # Right platform
    FIRE = (0, 0, 255)  # Fire
    SPAWN_POINT = (255, 255, 255)  # Spawn point

    def __init__(self):
        pass

    def load_level_infos(self, path):
        # Get Image
        image = pygame.image.load(path).convert_alpha()
        width = image.get_width()
        height = image.get_height()

        # Check ratio
        window_width = src.Constant.Constant.WINDOW_WIDTH
        window_height = src.Constant.Constant.WINDOW_HEIGHT
        widow_ratio = window_width / window_height
        image_ratio = width / height

        if widow_ratio != image_ratio:
            raise Exception('error', 'Image ratio is not the same as window ratio')
        
        scale = math.ceil(window_width / width)

        # Get the color of each pixel and determine the type of platform
        platforms = []
        fire = None
        spawn_points = []

        for x in range(width):
            for y in range(height):
                color = image.get_at((x, y))
                match color:
                    case self.LEFT_PLATFORM:
                        platforms.append(
                            src.UnmovablePlatform.UnmovablePlatform(x * scale, y * scale, scale, scale, "LEFT"))
                    case self.MID_1_PLATFORM:
                        platforms.append(
                            src.UnmovablePlatform.UnmovablePlatform(x * scale, y * scale, scale, scale, "MID_1"))
                    case self.MID_2_PLATFORM:
                        platforms.append(
                            src.UnmovablePlatform.UnmovablePlatform(x * scale, y * scale, scale, scale, "MID_2"))
                    case self.RIGHT_PLATFORM:
                        platforms.append(
                            src.UnmovablePlatform.UnmovablePlatform(x * scale, y * scale, scale, scale, "RIGHT"))
                    case self.FIRE:
                        if fire is not None:
                            raise Exception('error', 'More than one fire in the level')
                        fire = src.Fire.Fire(x * scale, y * scale, scale, scale)
                    case self.SPAWN_POINT:
                        spawn_points.append(src.SpawnPoint.SpawnPoint(vec(x * scale, y * scale), vec(scale, scale)))
                        if len(spawn_points) > 4:
                            raise Exception('error', 'More than four spawn point in the level')

        if fire is None:
            raise Exception('error', 'No fire in the level')

        if len(spawn_points) < 2:
            raise Exception('error', 'Less than two spawn points in the level')

        return platforms, fire, spawn_points
