import pygame

from enum import IntEnum

from src.UnmovablePlatform import UnmovablePlatform
from src.Stickman import Stickman
from src.Player import Player

vec = pygame.math.Vector2  # 2 for two dimensional
UP_VEC = vec(0,-1)
DOWN_VEC = vec(0,1)
LEFT_VEC = vec(-1,0)
RIGHT_VEC = vec(1,0)

class RectCollisionInfo():
    def __init__(self, normal, delta):
        self.normal = normal
        self.delta = delta

    def absolutePenetrationDepthAlongNormal(self) -> float:
        return abs(self.normal.dot(self.delta))
    
NO_COLLISION = RectCollisionInfo(vec(0,0), vec(0,0))

class Corner(IntEnum):
    TOP_LEFT = 0
    TOP_RIGHT = 1
    BOTTOM_RIGHT = 2
    BOTTOM_LEFT = 3

def opposite_corner(corner: Corner) -> Corner:
    match corner:
        case Corner.TOP_LEFT: return Corner.BOTTOM_RIGHT
        case Corner.TOP_RIGHT: return Corner.BOTTOM_LEFT
        case Corner.BOTTOM_RIGHT: return Corner.TOP_LEFT
        case Corner.BOTTOM_LEFT: return Corner.TOP_RIGHT
    raise Exception('error', 'invalid corner')
    
def get_corner_of(rect: pygame.Rect, corner: Corner):
    match corner:
        case Corner.TOP_LEFT: return vec(rect.topleft)
        case Corner.TOP_RIGHT: return vec(rect.topright)
        case Corner.BOTTOM_RIGHT: return vec(rect.bottomright)
        case Corner.BOTTOM_LEFT: return vec(rect.bottomleft)
    raise Exception('error', 'invalid corner')

def get_corners(rect: pygame.Rect):
    return [vec(rect.topleft), vec(rect.topright), vec(rect.bottomright), vec(rect.bottomleft)]

def rect_contains_point(rect : pygame.Rect, point : vec):
    return point.x >= rect.left and point.y >= rect.top and point.x <= rect.left + rect.width and point.y <= rect.top + rect.height

def rects_intersect(r1 : pygame.Rect, r2 : pygame.Rect):
    size = vec(r2.size) + vec(r1.size)
    pos = vec(r2.topleft) - vec(r1.size)
    extended = pygame.Rect(pos, size)
    return rect_contains_point(extended, vec(r1.topleft))

def rect_collision_info(first: pygame.Rect, other: pygame.Rect) -> RectCollisionInfo:
    if not rects_intersect(first, other):
        return NO_COLLISION
    
    firstCorners = get_corners(first)
    otherCorners = get_corners(other)
    otherCenter = other.center
    
    closestCornerDistanceSquared = 999999;
    closestCorner = None

    for corner in Corner:
        dist_squared = firstCorners[corner].distance_squared_to(otherCenter)
        if dist_squared < closestCornerDistanceSquared:
            closestCornerDistanceSquared = dist_squared
            closestCorner = corner

    c1 = firstCorners[closestCorner];
    c2 = otherCorners[opposite_corner(closestCorner)]

    delta = c1 - c2
    delta.x = abs(delta.x)
    delta.y = abs(delta.y)

    collisionNormal = vec(0,0)

    if delta.x > delta.y:
        if closestCorner == Corner.TOP_LEFT or closestCorner == Corner.TOP_RIGHT:
            collisionNormal = UP_VEC
        else:
            collisionNormal = DOWN_VEC
    else:
        if closestCorner == Corner.TOP_LEFT or closestCorner == Corner.BOTTOM_LEFT:
            collisionNormal = LEFT_VEC
        else:
            collisionNormal = RIGHT_VEC

    return RectCollisionInfo(collisionNormal, delta)

def handle_collision_player_vs_platform(player: Player, platform: UnmovablePlatform):
    platformRect = pygame.Rect(platform.position, platform.size)
    stickRect = pygame.Rect(player.position, player.size)

    collisionInfos = rect_collision_info(platformRect, stickRect)
    if collisionInfos == NO_COLLISION:
        return False
    
    if collisionInfos.normal == UP_VEC:
        player.position.y = platform.position.y - player.size.y # set pos en dur
        player.velocity.y = 0
        player.reset_jump()
    else:
        correction = collisionInfos.normal * collisionInfos.absolutePenetrationDepthAlongNormal()
        player.move(correction)
        if collisionInfos.normal == UP_VEC or collisionInfos.normal == DOWN_VEC:
            player.velocity.y = 0
        else:
            player.velocity.x = 0
    return True

    


    