import pygame

from src.ImageManager import ImageManager

vec = pygame.math.Vector2  # 2 for two dimensional

class SpritesheetAnimInfos():
    def __init__(self, textureManagerKey, frameSize: vec, origin: vec, frameCount, animationTime):
        self.key = textureManagerKey
        self.frameSize = frameSize
        self.origin = origin
        self.frameCount = frameCount
        self.animationTime = animationTime

class Animation():
    def __init__(self, infos: SpritesheetAnimInfos, position: vec, size: vec):
        self.surfaces = list()
        self.infos = infos
        self.initialize_surfaces(infos)
        self.isRunning = False
        self.timeSinceStart = 0
        self.spriteIndex = 0
        self.position = position
        self.size = size

        self.animSprite = pygame.sprite.Sprite()
        self.animSprite.surf = self.surfaces[0]
        self.animSprite.rect = pygame.rect.Rect(position, size)

    def initialize_surfaces(self, infos):
        spritesheet = ImageManager().get_image(infos.key)
        for i in range(infos.frameCount):
            xpos = infos.origin.x + i * infos.frameSize.x
            surf = pygame.Surface.subsurface(spritesheet, xpos, infos.origin.y, infos.frameSize.x, infos.frameSize.y)
            self.surfaces.append(surf)

    def start(self):
        self.isRunning = True
    
    def stop(self):
        self.isRunning = False

    def update(self, dt: float):
        if not self.isRunning:
            return
        self.timeSinceStart += dt
        timePerFrame = self.infos.animationTime / self.infos.frameCount
        if(self.timeSinceStart > timePerFrame):
            self.goto_next_frame()
            self.timeSinceStart -= timePerFrame

    def goto_next_frame(self):
        self.spriteIndex = (self.spriteIndex + 1) % self.infos.frameCount

    def draw(self, surface):
        surface.blit(self.surfaces[self.spriteIndex], self.animSprite.rect)
        

