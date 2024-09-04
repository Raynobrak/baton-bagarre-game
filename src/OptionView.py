import sys
import pygame
from pygame import Vector2
from src.AudioManager import AudioManager
from src.Constant import Constant
from src.Slider import Slider
from src.VolumeManager import VolumeManager
from src.Text import Text

vec = pygame.math.Vector2


def handle_slider(slider: Slider):
    mouse_pos = pygame.mouse.get_pos()
    if slider.is_grabbing:
        if pygame.mouse.get_pressed()[0] == 0:
            slider.stop_grabbing()
        else:
            slider.update_grabing_position(vec(mouse_pos))
    else:
        if slider.button_rect.collidepoint(mouse_pos) and \
                pygame.mouse.get_pressed()[0] == 1:
            slider.start_grabbing()


class OptionView:
    def __init__(self, display_surface: pygame.Surface):
        self.display_surface = display_surface
        self.font = pygame.font.Font('./assets/font/upheavtt.ttf', 50)
        self.back_text = self.font.render('Back', True, (255, 255, 255))
        self.back_rect = self.back_text.get_rect(
            center=(Constant.WINDOW_WIDTH / 2, Constant.WINDOW_HEIGHT - 100))
        self.volume_slider = Slider(vec(Constant.WINDOW_WIDTH / 2, 200),
                                    vec(300, 20), VolumeManager().generalVolume)
        self.music_slider = Slider(vec(Constant.WINDOW_WIDTH / 2, 250),
                                   vec(300, 20), VolumeManager().musicVolume)
        self.bruitage_slider = Slider(vec(Constant.WINDOW_WIDTH / 2, 300),
                                      vec(300, 20), VolumeManager().soundVolume)
        self.main_text = Text(vec(Constant.WINDOW_WIDTH / 2, 100),
                              "Option menu", color=pygame.Color("White"),
                              font='menu')
        self.volume_text = Text(vec(200, 200), "General Volume",
                                color=pygame.Color("White"))
        self.music_text = Text(vec(200, 250), "Music",
                               color=pygame.Color("White"))
        self.bruitage_text = Text((200, 300), "Sound effects",
                                  color=pygame.Color(
                                      "White"))
        self.hovered_option = None
        self.selected_option = 0  # 0 for 'Back'

    def display_option(self):
        pygame.display.set_caption("Option")
        while True:
            self.display_surface.fill((0, 0, 0))
            option_mouse_pos = pygame.mouse.get_pos()

            self.handle_mouse_hover(option_mouse_pos)

            back_color = (255, 255,
                          255) if self.hovered_option == 'back' or self.selected_option == 0 else (
            100, 100, 100)
            self.back_text = self.font.render('Back', True, back_color)

            self.display_surface.blit(self.back_text, self.back_rect)
            self.volume_slider.render(self.display_surface)
            self.music_slider.render(self.display_surface)
            self.bruitage_slider.render(self.display_surface)
            self.volume_text.draw(self.display_surface)
            self.main_text.draw_center(self.display_surface)
            self.music_text.draw(self.display_surface)
            self.bruitage_text.draw(self.display_surface)

            handle_slider(self.volume_slider)
            handle_slider(self.music_slider)
            handle_slider(self.bruitage_slider)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.back_rect.collidepoint(option_mouse_pos):
                        return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        self.selected_option = (
                                                           self.selected_option + 1) % 1 if event.key == pygame.K_DOWN else (
                                                                                                                                        self.selected_option - 1) % 1
                    if event.key == pygame.K_RETURN:
                        return

            VolumeManager().update_general_volume(self.volume_slider.value)
            VolumeManager().update_music_volume(self.music_slider.value)
            VolumeManager().update_sound_volume(self.bruitage_slider.value)
            AudioManager().update_music_volume()
            pygame.display.update()

    def handle_mouse_hover(self, mouse_pos):
        if self.back_rect.collidepoint(mouse_pos):
            self.hovered_option = 'back'
        else:
            self.hovered_option = None
