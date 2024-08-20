import pygame
from pygame.locals import *

from src.Constant import Constant

vec = pygame.math.Vector2  # 2 for two dimensional
FramePerSec = pygame.time.Clock()

import src.Constant
from src.Player import Player

class Game():
    __player: Player
    __displaysurface = None
    __spritegroup = pygame.sprite.Group()

    def __init__(self):
        print("Hello")
        pygame.init()
        self.__displaysurface = pygame.display.set_mode((Constant.WINDOW_WIDTH, Constant.WINDOW_HEIGHT))
        pygame.display.set_caption("Game")

        self.__player = Player()
        self.run()

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

if __name__ == "__main__":
    Game()