from random import random, randint

from src.AudioManager import AudioManager
from src.CooldownVariable import CooldownVariable
from src.Entity import Entity
from src.Enemy import Enemy
from src.SpawnPoint import SpawnPoint


class WaveManager:

    def __init__(self, spawn_points: list[SpawnPoint], enemies: list[Enemy], target: Entity):
        self.spawn_points = spawn_points
        self.enemies = enemies
        self.target = target
        self.normal_cooldown = CooldownVariable(4.5)
        self.wave_cooldown = CooldownVariable(10)
        self.wave_started = False
        self.wave_ennemy_cooldown = CooldownVariable(1)
        self.enemy_per_wave = 10
        self.enemy_in_wave = 0
        self.wave_count = 0

    def update_wave(self, dt):
        if not self.wave_started : self.normal_cooldown.update_cooldown(dt)
        if not self.wave_started :self.wave_cooldown.update_cooldown(dt)

        if not self.wave_started and self.wave_cooldown.ready():
            print("Wave started")
            AudioManager().play_sound_random(["New_Wave1", "New_Wave2", "New_Wave3"])
            self.wave_started = True

        if not self.wave_started and  self.normal_cooldown.try_reset():
            self.spawn_enemy()

        if self.wave_started:
            self.wave_ennemy_cooldown.update_cooldown(dt)

            if self.wave_ennemy_cooldown.try_reset():
                self.enemy_in_wave += 1
                self.spawn_enemy()
                if self.enemy_in_wave >= self.enemy_per_wave:
                    self.wave_started = False
                    self.wave_cooldown.reset()
                    self.enemy_in_wave = 0
                    self.wave_count += 1
                    print("Wave ended")

        if self.wave_count % 5:
            self.enemy_per_wave += 1

        if self.wave_count % 10:
            self.wave_cooldown.max -= 0.5

    def spawn_enemy(self):
        spawn = randint(0, len(self.spawn_points) - 1)
        self.spawn_points[spawn].spawn_enemy(self.enemies, self.target)
