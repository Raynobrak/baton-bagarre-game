from enum import Enum

from pygame.locals import *

from src.CollisionUtils import *
from src.Entity import Entity
from src.Enemy import Enemy
from src.Animation import *
from src.CooldownVariable import CooldownVariable
from src.Fire import Fire
from src.ImageManager import ImageManager
from src.Stickman import Stickman, StickmanState, Direction

from pygame.locals import *

vec = pygame.math.Vector2  # 2 for two dimensional


class Hit(Entity):
    IMPULSE_ANGLE = 45

    def __init__(self, position: vec, size: vec, hitter: Stickman, lifetime: float, damage: int,
                 impulse_acceleration: int):
        super().__init__(position, size, vec(0, 0))

        self.timeLeft = lifetime
        self.hitter = hitter
        self.damage = damage
        self.impulse_acceleration = impulse_acceleration

    def update(self, dt):
        self.timeLeft -= dt

    def is_active(self):
        return self.timeLeft > 0

    def check_for_collision(self, enemy: Enemy):
        hitbox = self.get_hitbox()
        entity_hitbox = enemy.get_hitbox()

        if rects_intersect(hitbox, entity_hitbox):
            self.timeLeft = 0
            enemy.take_damage(self.damage)

            impulse = vec(1, 0)
            impulse.rotate_ip(self.IMPULSE_ANGLE)
            impulse *= self.impulse_acceleration
            impulse.y = -impulse.y
            dir = vec(entity_hitbox.center) - vec(self.hitter.get_hitbox().center)
            if dir.x < 0:
                impulse.x = -impulse.x

            enemy.accelerate(impulse)


class PunchHit(Hit):
    DAMAGE = 30
    IMPULSE_ACCELERATION = 200

    def __init__(self, hitter: Stickman):
        playerHitbox = hitter.get_hitbox()
        punchHitboxSize = vec(playerHitbox.size)

        punchOffset = playerHitbox.width / 2

        punchDirection = hitter.lookingDirection
        punchHitboxXPos = playerHitbox.left + punchOffset
        if punchDirection is Direction.LEFT:
            punchHitboxXPos -= punchHitboxSize.x

        super().__init__(vec(punchHitboxXPos, playerHitbox.top), punchHitboxSize, hitter, 0.01, self.DAMAGE, self.IMPULSE_ACCELERATION)


class KickHit(Hit):
    DAMAGE = 50
    IMPULSE_ACCELERATION = 400

    def __init__(self, hitter: Stickman):
        playerHitbox = hitter.get_hitbox()
        kickHitboxSize = vec(playerHitbox.size) * 1.5

        kickOffset = playerHitbox.width / 2

        kickDirection = hitter.lookingDirection
        kickHitboxXPos = playerHitbox.left + kickOffset
        if kickDirection is Direction.LEFT:
            kickHitboxXPos -= kickHitboxSize.x

        super().__init__(vec(kickHitboxXPos, playerHitbox.top), kickHitboxSize, hitter, 0.01, self.DAMAGE, self.IMPULSE_ACCELERATION)
