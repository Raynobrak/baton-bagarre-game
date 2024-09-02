from random import random, randint

from src.CooldownVariable import CooldownVariable
from src.Entity import Entity
from src.Enemy import Enemy
from src.SpawnPoint import SpawnPoint

class WaveManager:

    def __init__(self, spawn_points: list[SpawnPoint], enemies: list[Enemy], target: Entity):
        self.spawn_points = spawn_points
        self.enemies = enemies
        self.target = target
        self.coolDown = CooldownVariable(1)

    def create_wave(self):
        pass



    def update_wave(self, dt):
        self.coolDown.update_cooldown(dt)

        if self.coolDown.try_reset():
            spawn = randint(0, len(self.spawn_points) - 1)
            self.spawn_points[spawn].spawn_enemy(self.enemies, self.target)






