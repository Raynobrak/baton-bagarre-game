import pygame

from src.ImageManager import ImageManager

vec = pygame.math.Vector2  # 2 for two dimensional

# Describes the information needed for an animation
# Used in the ctor of Animation
# Requirements :
# 1. All the frames of the animation must be contained and be aligned in a single file (a spritesheet)
# 2. The file must be loaded in the ImageManager
class SpritesheetAnimInfos():
    # textureManagerKey : key of the texture in the ImageManager
    # frameSize : size of a single frame on the sprite sheet
    # origin : top left coordinates of the first frame on the spritesheet 
    # frameCount : total number of frames in the animation
    # animationTime : time needed for a single loop of the animation to complete, reduce to increase fps
    def __init__(self, imageManagerKey, frameSize: vec, origin: vec, frameCount, animationTime):
        self.key = imageManagerKey
        self.frameSize = frameSize
        self.origin = origin
        self.frameCount = frameCount
        self.animationTime = animationTime

# Represents an Animation that can be drawn on a surface
# Example usage :
#
# infos = SpritesheetAnimInfos('player_idle', vec(32,32), vec(0,0), 4, 0.5)
# anim_test = Animation(infos, vec(100,100), vec(80,80))
# anim_test.start()
#
# ... in the main loop ...
# anim_test.update(0.5)
#
# anim_test.draw(displaysurface)
class Animation():
    def __init__(self, infos: SpritesheetAnimInfos, position: vec, size: vec):
        self.surfaces = list()
        self.infos = infos
        self.initialize_surfaces(infos)
        self.isRunning = False
        self.timeSinceStart = 0
        self.spriteIndex = 0

        self.animSprite = pygame.sprite.Sprite()
        self.animSprite.surf = self.surfaces[0]
        self.animSprite.rect = pygame.rect.Rect(position, size)

        self.set_position(position)
        self.set_size(size)

    def set_size(self, newSize: vec):
        self.animSprite.rect.size = newSize
        for index, surface in enumerate(self.surfaces):
            self.surfaces[index] = pygame.transform.scale(surface, newSize)

    def set_position(self, newPos):
        self.animSprite.rect.left = newPos.x
        self.animSprite.rect.top = newPos.y

    def flip_horizontally(self):
        for index, surface in enumerate(self.surfaces):
            self.surfaces[index] = pygame.transform.flip(surface, True, False)
        
    def flip_vertically(self):
        for index, surface in enumerate(self.surfaces) :
            self.surfaces[index] = pygame.transform.flip(surface, False, True)

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

    # updates the animation depending on the time elapsed since the last call to update()
    def update(self, dt: float):
        if not self.isRunning:
            return
        self.timeSinceStart += dt
        timePerFrame = self.infos.animationTime / self.infos.frameCount
        if(self.timeSinceStart > timePerFrame):
            self.goto_next_frame()
            self.timeSinceStart -= timePerFrame

    # goes to next frame or loops if the animation is over
    def goto_next_frame(self):
        self.spriteIndex = (self.spriteIndex + 1) % self.infos.frameCount

    def draw(self, surface, filter = None):
        if filter is None:
            surface.blit(self.surfaces[self.spriteIndex], self.animSprite.rect)
        else:
            imgCopy = self.surfaces[self.spriteIndex].copy()
            imgCopy.blit(filter, (0, 0), special_flags=pygame.BLEND_ADD)
            surface.blit(imgCopy, self.animSprite.rect)

# Animations declarations
ANIM_TIME = 0.3

ANIM_PLAYER_IDLE = SpritesheetAnimInfos("player_idle", vec(32,32), vec(0,0), 4, ANIM_TIME)
ANIM_PLAYER_WALKING = SpritesheetAnimInfos("player_walking", vec(32,32), vec(0,0), 4, ANIM_TIME)

ANIM_PLAYER_JUMPING = SpritesheetAnimInfos("player_jumping", vec(32,32), vec(0,0), 1, ANIM_TIME)

ANIM_PLAYER_PUNCH = SpritesheetAnimInfos("player_punch", vec(32,32), vec(0,0), 1, ANIM_TIME)
ANIM_PLAYER_KICK = SpritesheetAnimInfos("player_kick", vec(32,32), vec(0,0), 1, ANIM_TIME)

ANIM_PLAYER_REIGNITE_FIRE = SpritesheetAnimInfos("player_reignite", vec(32,32), vec(0,0), 4, ANIM_TIME)

ANIM_ENEMY_IDLE = SpritesheetAnimInfos("enemy_idle", vec(32,32), vec(0,0), 4, ANIM_TIME)
ANIM_ENEMY_WALKING = SpritesheetAnimInfos("enemy_walking", vec(32,32), vec(0,0), 4, ANIM_TIME)
ANIM_ENEMY_JUMPING = SpritesheetAnimInfos("enemy_jumping", vec(32,32), vec(0,0), 1, ANIM_TIME)
ANIM_ENEMY_WATER_BUCKET = SpritesheetAnimInfos("enemy_water_bucket", vec(32,32), vec(0,0), 4, ANIM_TIME)

ANIM_FIRE_BIG = SpritesheetAnimInfos("fire_big", vec(32,32), vec(0,0), 4, ANIM_TIME)
ANIM_FIRE_MEDIUM = SpritesheetAnimInfos("fire_medium", vec(32,32), vec(0,0), 4, ANIM_TIME)
ANIM_FIRE_SMALL = SpritesheetAnimInfos("fire_small", vec(32,32), vec(0,0), 4, ANIM_TIME)
ANIM_FIRE_VERY_SMALL = SpritesheetAnimInfos("fire_very_small", vec(32,32),
                                            vec(0,0), 4, ANIM_TIME)