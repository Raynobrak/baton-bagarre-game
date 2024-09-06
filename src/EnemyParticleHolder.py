import pygame

from src.ImageManager import ImageManager
from src.EnemyParticle import EnemyParticle
from src.Enemy import Enemy
from src.CollisionUtils import *

vec = pygame.math.Vector2  # 2 for two dimensional


class EnemyParticleHolder():
    def __init__(self, mapSize, platforms):
        self.particles = list()
        self.mapSize = mapSize
        self.platforms = platforms

    def generate_destruction_particles_for_enemy(self, enemy):
        LINES = 3
        COLUMNS = 4

        enemyImage = enemy.get_current_frame()
        enemyImage = pygame.transform.scale(enemyImage, Enemy.ENEMY_SPRITE_SIZE)
        hitboxLeft = (Enemy.ENEMY_SPRITE_SIZE.x - Enemy.ENEMY_HITBOX_SIZE.x) / 2
        enemyHitboxSubsurface = enemyImage.subsurface(pygame.Rect(vec(hitboxLeft, 0), Enemy.ENEMY_HITBOX_SIZE))

        enemyHitbox = enemy.get_hitbox()
        enemySize = vec(enemyHitbox.size)
        enemyCenter = vec(enemyHitbox.center)
        enemyPos = vec(enemyHitbox.topleft)

        subrectSize = vec(enemySize.x / COLUMNS, enemySize.y / LINES)

        for line in range(LINES):
            for col in range(COLUMNS):
                imgXPos = col * subrectSize.x
                imgYPos = line * subrectSize.y

                subsurf = enemyHitboxSubsurface.subsurface(pygame.Rect(vec(imgXPos, imgYPos), subrectSize))

                particleTopleft = vec(imgXPos, imgYPos) + enemyPos

                dir = enemyCenter - particleTopleft + subrectSize / 2
                if dir != vec(0,0):
                    dir.normalize_ip()
                else:
                    dir = UP_VEC
                impulse = enemy.velocity + -dir * 100

                newParticle = EnemyParticle(particleTopleft, subrectSize, impulse, subsurf)
                self.particles.append(newParticle)

    def update(self, dt: float):
        for p in self.particles:
            p.update(dt)

        self.check_for_collisions()
        self.remove_destroyed_particles()
    
    def check_for_collisions(self):
        for particle in self.particles:
            handle_particle_vs_map_collision(particle, self.mapSize)
            for platform in self.platforms:
                handle_particle_vs_platform_collision(particle, platform)
    
    def remove_destroyed_particles(self):
        for p in self.particles:
            if p.needs_to_disappear():
                self.particles.remove(p)
    
    def draw(self, surface):
        for p in self.particles:
            p.draw(surface)
