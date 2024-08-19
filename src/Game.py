import pygame
from pygame.locals import *
vec = pygame.math.Vector2  # 2 for two dimensional
FramePerSec = pygame.time.Clock()

from constants import *

from Player import *

class Game():
    __player = None
    __displaysurface = None
    __spritegroup = pygame.sprite.Group()

    def __init__(self):
        pygame.init()
        self.__displaysurface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Game")

        self.__player = Player()
        self.__spritegroup.add(self.__player)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            self.__displaysurface.fill((0,0,0))

            #for entity in self.__spritegroup:

            self.__player.draw(self.__displaysurface)

            pygame.display.update()
            FramePerSec.tick(FPS)
