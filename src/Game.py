import pygame
from pygame.locals import *

from src.AudioManager import AudioManager
from src.FontManager import FontManager
from src.LevelGenerator import LevelGenerator
from src.OptionView import OptionView
from src.Player import Player
from src.Enemy import Enemy
from src.Animation import SpritesheetAnimInfos, Animation
from src.CollisionUtils import *
from src.ImageManager import ImageManager
from src.Constant import Constant
from src.Button import Button
from src.MainMenu import MainMenu
from src.PauseMenu import PauseMenu
from src.ProgressBar import ProgressBar

from src.Fire import Fire
from src.WaveManager import WaveManager

vec = pygame.math.Vector2  # 2 for two dimensional
FramePerSec = pygame.time.Clock()

import src.Constant


class Game():
    DELTA_TIME = 1 / Constant.FPS
    def __init__(self):
        pygame.init()
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, 1)
        self.enemies : list[Enemy] = []
        self.__displaysurface = pygame.display.set_mode((Constant.WINDOW_WIDTH, Constant.WINDOW_HEIGHT))
        pygame.display.set_caption("Game")
        self.load_all_images()

        self.visibility = 1

        self.__player = Player(vec(100,100))
        self.wave_manager = None
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

        ImageManager().load_image('./assets/textures/play_button.png', 'play_button')
        ImageManager().load_image('./assets/textures/options_button.png', 'options_button')
        ImageManager().load_image('./assets/textures/logo.png', 'logo')
        
        ImageManager().load_image('./assets/textures/circle.png', 'circle')

        AudioManager().load_sound('./assets/audio/BatonBagarre.mp3', 'music')

        FontManager().load_font('./assets/font/upheavtt.ttf', 'default')
        FontManager().load_font('./assets/font/upheavtt.ttf', 'menu', font_size=50)
        

    def update_light(self, fire: Fire, original_circle: pygame.Surface):
        # Center the circle with the fire and scale it based on fire's life points
        fire_pos = fire.get_position()
        fire_size = fire.size
        fire_life_points = fire.lifePoints

        circle_size = fire_size.x + (Constant.WINDOW_WIDTH * 3) * (fire_life_points / Constant.FIRE_HEALTH)

        # Scale the circle image
        circle = pygame.transform.smoothscale(original_circle, vec(int(circle_size), int(circle_size)))

        # Calculate position to center the circle with the fire
        circle_pos = (fire_pos.x + fire_size.x / 2 - circle.get_width() / 2,
                      fire_pos.y + fire_size.y / 2 - circle.get_height() / 2)

        # Create a light filter to darken the screen
        light_filter = pygame.surface.Surface((Constant.WINDOW_WIDTH, Constant.WINDOW_HEIGHT))
        color_ratio = 255 * (1 - fire_life_points / Constant.FIRE_HEALTH)
        light_filter.fill((color_ratio, color_ratio, color_ratio))
        light_filter.blit(circle, circle_pos)
        self.__displaysurface.blit(light_filter, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)

    def check_player_interaction(self, player: Player, fire: Fire):
        # Check if player is in range of fire and press E to interact
        if (player.position + player.size / 2).distance_to(fire.position + fire.size / 2) < player.size.x:
            if pygame.key.get_pressed()[pygame.K_e] and player.isLevitating is False:
                player.go_levitate()

            # Check if player has finished reigniting the fire
            has_finished_reigniting = player.try_stop_levitate()
            if has_finished_reigniting:
                fire.reignite()


    def run(self):
        # Load level
        bg = pygame.transform.smoothscale(ImageManager().get_image('background2'), (Constant.WINDOW_WIDTH, Constant.WINDOW_HEIGHT))
        platforms, fire, spawn_points = LevelGenerator().load_level_infos('./assets/levels/level1.png')
        original_circle = ImageManager().get_image('circle')
        fire_health_bar = ProgressBar(fire.position - vec(0, fire.size.y / 2), vec(fire.size.x, 10), max_value=Constant.FIRE_HEALTH, current_value=fire.lifePoints)

        self.wave_manager = WaveManager(spawn_points,self.enemies, self.__player)
        while True:
            #print("Ennemy size = " + str(len(self.enemies)))
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.pause_menu()
                    
            self.wave_manager.update_wave(self.DELTA_TIME)
            self.__player.update(self.DELTA_TIME)
            for enemy in self.enemies:
                enemy.update(self.DELTA_TIME)
                enemy.check_collision_with_walls(vec(Constant.WINDOW_WIDTH, Constant.WINDOW_HEIGHT))

            self.__player.check_collision_with_walls(vec(Constant.WINDOW_WIDTH, Constant.WINDOW_HEIGHT))
            for enemy in self.enemies:
                self.__player.check_if_entity_is_hit(enemy)

            for enemy in self.enemies:
                if enemy.is_dead():
                    self.enemies.remove(enemy)

            self.check_player_interaction(self.__player, fire)

            for platform in platforms:
                handle_collision_stickman_vs_platform(self.__player, platform)
                for enemy in self.enemies:
                    handle_collision_stickman_vs_platform(enemy, platform)

            # Draw Level
            self.__displaysurface.blit(bg, (0, 0))
            for platform in platforms:
                platform.draw(self.__displaysurface)

            # Update and draw fire object and health bar
            fire.update(self.DELTA_TIME)
            fire.draw(self.__displaysurface)
            fire_health_bar.current_value = fire.lifePoints
            fire_health_bar.draw(self.__displaysurface)

            # Draw Player
            self.__player.draw(self.__displaysurface)
            for enemy in self.enemies:
                enemy.draw(self.__displaysurface)

            # Update and draw light
            self.update_light(fire, original_circle)

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
                print("option")
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


if __name__ == "__main__":
    Game()
