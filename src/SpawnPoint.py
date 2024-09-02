from src.Entity import Entity
from src.Animation import *
from src.Enemy import Enemy


vec = pygame.math.Vector2  # 2 for two dimensional


class SpawnPoint(Entity):
    def __init__(self, pos: vec, size: vec):
        super().__init__(pos, size)

    def spawn_enemy(self, enemies, target):
        new_enemy = Enemy(vec(self.position))
        new_enemy.set_target(target)
        enemies.append(new_enemy)

