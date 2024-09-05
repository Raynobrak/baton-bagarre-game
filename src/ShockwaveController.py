from src.ProgressBar import ProgressBar
from src.Shockwave import Shockwave
from src.Constant import Constant

import pygame
vec = pygame.math.Vector2  # 2 for two dimensional

class ShockwaveController():
    ENEMIES_THRESHOLD = 10
    PROGRESS_BAR_SIZE = vec(200,20)
    PROGRESS_BAR_TOP_MARGIN = 60

    PBAR_FRONT_COLOR = (Shockwave.SHOCKWAVE_RED,Shockwave.SHOCKWAVE_GREEN,Shockwave.SHOCKWAVE_BLUE)
    PBAR_BACK_COLOR = (255,255,255)

    def __init__(self):
        self.enemiesKilledCounter = 0
        self.game_over = False
        left = Constant.WINDOW_WIDTH / 2 - self.PROGRESS_BAR_SIZE.x / 2

        self.progress_bar = ProgressBar(vec(left, self.PROGRESS_BAR_TOP_MARGIN), self.PROGRESS_BAR_SIZE, self.PBAR_FRONT_COLOR, self.PBAR_BACK_COLOR, self.ENEMIES_THRESHOLD)

    def notify_enemy_killed(self):
        if self.enemiesKilledCounter < self.ENEMIES_THRESHOLD:
            self.enemiesKilledCounter += 1

    def is_shockwave_available(self):
        return self.enemiesKilledCounter >= self.ENEMIES_THRESHOLD

    def reset(self):
        self.enemiesKilledCounter = 0
        self.game_over = False

    def set_game_over(self):
        self.game_over = True

    def draw(self, surface):
        if self.game_over:
            return

        self.progress_bar.set_value(self.enemiesKilledCounter)
        self.progress_bar.draw(surface)
        