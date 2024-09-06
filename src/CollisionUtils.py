import pygame

from enum import IntEnum

from src.UnmovablePlatform import UnmovablePlatform
from src.Stickman import Stickman
from src.EnemyParticle import EnemyParticle

vec = pygame.math.Vector2  # 2 for two dimensional
UP_VEC = vec(0,-1)
DOWN_VEC = vec(0,1)
LEFT_VEC = vec(-1,0)
RIGHT_VEC = vec(1,0)


class RectCollisionInfo:
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

def rect_contains_rect(container : pygame.Rect, r : pygame.Rect):
    extended = pygame.Rect(container.left, container.top, container.width + r.width, container.height + r.height)
    return rect_contains_point(extended, vec(r.topleft))

def rect_collision_info(first: pygame.Rect, other: pygame.Rect) -> RectCollisionInfo:
    if not rects_intersect(first, other):
        return NO_COLLISION
    
    firstCorners = get_corners(first)
    otherCorners = get_corners(other)
    otherCenter = other.center
    
    closestCornerDistanceSquared = 999999
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

def handle_particle_vs_platform_collision(particle: EnemyParticle, platform: UnmovablePlatform):
    platformRect = platform.get_hitbox()
    particleRect = particle.get_hitbox()

    collisionInfos = rect_collision_info(platformRect, particleRect)
    if collisionInfos == NO_COLLISION:
        return False
    
    correction = collisionInfos.normal * collisionInfos.absolutePenetrationDepthAlongNormal()

    velocityAlongNormal = abs(particle.velocity.dot(collisionInfos.normal))

    impulse = 0.9 * velocityAlongNormal * collisionInfos.normal

    if collisionInfos.normal == UP_VEC or collisionInfos.normal == DOWN_VEC:
        particle.velocity.y = 0
    else:
        particle.velocity.x = 0

    particle.accelerate(impulse)

    return True

def handle_particle_vs_map_collision(particle: EnemyParticle, mapSize: vec):
    mapRect = pygame.Rect(vec(0,0), mapSize)
    particleRect = particle.get_hitbox()

    particleSize = vec(particleRect.size)
    particlePos = vec(particleRect.topleft)
    shrunkRect = pygame.Rect(vec(0,0), mapSize - particleSize)

    if rect_contains_point(shrunkRect, particlePos):
        return False
    
    dir = vec(0,0)
    depth = 0
    if particlePos.x < shrunkRect.left:
        depth = particlePos.x
        dir = LEFT_VEC
    elif particlePos.x > shrunkRect.width:
        depth = particlePos.x - shrunkRect.width
        dir = RIGHT_VEC
    elif particlePos.y > shrunkRect.height:
        depth = particlePos.y - shrunkRect.height
        dir = DOWN_VEC
    
    if depth == 0:
        return False
    
    correction = abs(depth) * -dir
    particle.move(correction)

    velocityAlongNormal = abs(particle.velocity.dot(dir))
    impulse = 0.5 * velocityAlongNormal * -dir
    particle.accelerate(impulse + velocityAlongNormal * -dir)


def handle_collision_stickman_vs_platform(stickman: Stickman, platform: UnmovablePlatform):
    platformRect = pygame.Rect(platform.position, platform.size)
    stickRect = pygame.Rect(stickman.position, stickman.size)

    collisionInfos = rect_collision_info(platformRect, stickRect)
    if collisionInfos == NO_COLLISION:
        return False
    
    if collisionInfos.normal == UP_VEC:
        stickman.position.y = platform.position.y - stickman.size.y # set pos en dur
        stickman.velocity.y = 0
        stickman.reset_jump()
    else:
        correction = collisionInfos.normal * collisionInfos.absolutePenetrationDepthAlongNormal()
        stickman.move(correction)
        if collisionInfos.normal == UP_VEC or collisionInfos.normal == DOWN_VEC:
            stickman.velocity.y = 0
        else:
            stickman.velocity.x = 0
    return True

    


    