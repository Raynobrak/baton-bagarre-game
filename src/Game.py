import pygame
from pygame.locals import *

from src.AudioManager import AudioManager
from src.FontManager import FontManager
from src.LevelGenerator import LevelGenerator
from src.OptionView import OptionView
from src.Player import Player
from src.Enemy import Enemy
from src.CollisionUtils import *
from src.ImageManager import ImageManager
from src.Constant import Constant
from src.MainMenu import MainMenu
from src.PauseMenu import PauseMenu
from src.EndMenu import EndMenu
from src.LightManager import LightManager
from src.Fire import Fire
from src.WaveManager import WaveManager

from src.EnemyParticleHolder import EnemyParticleHolder

vec = pygame.math.Vector2  # 2 for two dimensional
FramePerSec = pygame.time.Clock()


class Game:
    DELTA_TIME = 1 / Constant.FPS

    def __init__(self):
        pygame.init()
        self.enemies: list[Enemy] = []
        self.__displaysurface = pygame.display.set_mode((Constant.WINDOW_WIDTH, Constant.WINDOW_HEIGHT))
        pygame.display.set_caption("Game")
        self.load_all_images()

        self.visibility = 1

        self.score = 0

        self.platforms, self.fire, self.spawn_points = LevelGenerator().load_level_infos('./assets/levels/level1.png')

        self.particleHolder = EnemyParticleHolder(vec(Constant.WINDOW_WIDTH, Constant.WINDOW_HEIGHT), self.platforms)

        self.__player = Player(vec(100, 100))
        self.wave_manager = WaveManager(self.spawn_points, self.enemies, self.fire)
        self.light_manager = LightManager(self.fire)

        self.main_menu()

    def load_all_images(self):
        ImageManager().load_image('./assets/textures/player_default.png', 'player')

        ImageManager().load_image('./assets/textures/background.png', 'background')
        ImageManager().load_image('./assets/textures/background2.png', 'background2')
        ImageManager().load_image('./assets/textures/background3.png', 'background3')
        ImageManager().load_image('./assets/textures/platform_left.png', 'platform_left')
        ImageManager().load_image('./assets/textures/platform_mid_1.png', 'platform_mid_1')
        ImageManager().load_image('./assets/textures/platform_mid_2.png', 'platform_mid_2')
        ImageManager().load_image('./assets/textures/platform_right.png', 'platform_right')

        ImageManager().load_image('./assets/textures/player_idle.png', 'player_idle')
        ImageManager().load_image('./assets/textures/player_move.png', 'player_walking')

        ImageManager().load_image('./assets/textures/player_jump.png', 'player_jumping')
        ImageManager().load_image('./assets/textures/player_attack.png', 'player_punch')
        ImageManager().load_image('./assets/textures/player_kick.png', 'player_kick')

        ImageManager().load_image('./assets/textures/player_yoga.png', 'player_reignite')

        ImageManager().load_image('./assets/textures/enemy_idle.png', 'enemy_idle')
        ImageManager().load_image('./assets/textures/enemy_move.png', 'enemy_walking')
        ImageManager().load_image('./assets/textures/enemy_jump.png', 'enemy_jumping')
        ImageManager().load_image('./assets/textures/enemy_water_bucket.png', 'enemy_water_bucket')

        ImageManager().load_image('./assets/textures/fire_big.png', 'fire_big')
        ImageManager().load_image('./assets/textures/fire_medium.png', 'fire_medium')
        ImageManager().load_image('./assets/textures/fire_small.png', 'fire_small')
        ImageManager().load_image('./assets/textures/fire_very_small.png', 'fire_very_small')
        ImageManager().load_image('./assets/textures/fire_dead.png', 'fire_dead')

        ImageManager().load_image('./assets/textures/play_button.png', 'play_button')
        ImageManager().load_image('./assets/textures/options_button.png', 'options_button')
        ImageManager().load_image('./assets/textures/logo.png', 'logo')

        ImageManager().load_image('./assets/textures/circle.png', 'circle')

        AudioManager().load_sound('./assets/audio/BatonBagarre.mp3', 'music')

        FontManager().load_font('./assets/font/upheavtt.ttf', 'default')
        FontManager().load_font('./assets/font/upheavtt.ttf', 'menu', font_size=50)

    def check_player_interaction(self, player: Player, fire: Fire):
        # Check if player is in range of fire and press E to interact
        if (player.position + player.size / 2).distance_to(fire.position + fire.size / 2) <= player.size.x:
            if pygame.key.get_pressed()[pygame.K_e] and player.isLevitating is False:
                player.go_levitate()

            # Check if player has finished reigniting the fire
            has_finished_reigniting = player.try_stop_levitate()
            if has_finished_reigniting:
                fire.reignite()

    def check_enemies_interaction(self, enemies: list[Enemy], fire: Fire):
        # Check if an enemy is in range of fire
        for enemy in enemies:
            if (enemy.position + enemy.size / 2).distance_to(fire.position + fire.size / 2) <= enemy.size.x:
                enemy.go_water_bucket()

            # Check if enemy has finished throwing water bucket
            has_finished_water_bucket = enemy.try_stop_water_bucket()
            if has_finished_water_bucket:
                fire.splash()

    def make_enemy_explode(self, enemy: Enemy):
        self.particleHolder.generate_destruction_particles_for_enemy(enemy)

    def run(self):
        # Load level
        bg = pygame.transform.smoothscale(ImageManager().get_image('background2'),
                                          (Constant.WINDOW_WIDTH, Constant.WINDOW_HEIGHT))

        self.light_manager.update()
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.pause_menu()

            # Update Player
            self.wave_manager.update_wave(self.DELTA_TIME)
            self.__player.update(self.DELTA_TIME)
            self.__player.check_collision_with_walls(vec(Constant.WINDOW_WIDTH, Constant.WINDOW_HEIGHT))

            # Update Fire
            self.fire.update(self.DELTA_TIME)
            self.check_player_interaction(self.__player, self.fire)
            self.check_enemies_interaction(self.enemies, self.fire)

            # Update Enemies
            for enemy in self.enemies:
                enemy.update(self.DELTA_TIME)
                enemy.check_collision_with_walls(vec(Constant.WINDOW_WIDTH, Constant.WINDOW_HEIGHT))

            # Check fighting behavior
            for enemy in self.enemies:
                self.__player.check_if_entity_is_hit(enemy)
            self.particleHolder.update(self.DELTA_TIME)
            for enemy in self.enemies:
                if enemy.is_dead():
                    self.make_enemy_explode(enemy)
                    self.enemies.remove(enemy)
                    self.score += 100

            # Check collision
            for platform in self.platforms:
                handle_collision_stickman_vs_platform(self.__player, platform)
                for enemy in self.enemies:
                    handle_collision_stickman_vs_platform(enemy, platform)

            # Draw Level
            self.__displaysurface.blit(bg, (0, 0))
            for platform in self.platforms:
                platform.draw(self.__displaysurface)

            # Draw fire
            self.fire.draw(self.__displaysurface)

            # Check game over
            if self.fire.is_dead():
                self.end_menu()
                break

            # Draw Player and Enemies
            self.__player.draw(self.__displaysurface)
            for enemy in self.enemies:
                enemy.draw(self.__displaysurface)
            self.particleHolder.draw(self.__displaysurface)

            # Update and draw light
            if self.fire.has_life_points_changed():
                self.light_manager.update()
            self.light_manager.draw(self.__displaysurface)

            pygame.display.update()
            FramePerSec.tick(Constant.FPS)

    def main_menu(self):
        main_menu = MainMenu(self.__displaysurface)
        option_menu = OptionView(self.__displaysurface)
        while True:

            action = main_menu.display_menu()
            if action == 'play':
                AudioManager().play_music()
                self.run()
            elif action == 'options':
                option_menu.display_option()

    def pause_menu(self):
        pause_menu = PauseMenu(self.__displaysurface, options=['Resume', 'Options', 'Quit'])
        option_menu = OptionView(self.__displaysurface)

        while True:
            pause_menu.display_menu()
            action = pause_menu.handle_input()
            if action == 'Resume':
                break
            elif action == 'Options':
                option_menu.display_option()
                pass
            elif action == 'Quit':
                pygame.quit()
                exit()

    def end_menu(self):
        end_menu = EndMenu(self.__displaysurface, self.score,
                           self.__player, self.enemies)
        end_menu.display()
        while True:
            action = end_menu.handle_input()

            if action == 'play_again':
                self.reset_game()
                self.run()

            pygame.display.update()

            FramePerSec.tick(Constant.FPS)

    def reset_game(self):
        self.score = 0
        self.__player = Player(vec(100, 100))
        self.enemies = []
        self.fire.set_life_points(Fire.MAX_HEALTH)
        self.wave_manager = WaveManager(self.spawn_points, self.enemies, self.fire)


if __name__ == "__main__":
    Game()
