import sys

import pygame
from pygame import Vector2

from src.AudioManager import AudioManager
from src.Button import Button
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
        if slider.button_rect.collidepoint(mouse_pos) \
                and pygame.mouse.get_pressed()[0] == 1:
            slider.start_grabbing()


class OptionView:
    def __init__(self, display_surface: pygame.Surface):
        self.display_surface = display_surface
        #self.save_button = Button('play_button')
        self.back_button = Button('play_button', (Constant.WINDOW_WIDTH / 2, 0), scale=(150,75))
        self.volume_slider = Slider(vec(300,300), vec(100,20))
        self.music_slider = Slider(vec(300,350), vec(100,20))
        self.bruitage_slider = Slider(vec(300,400), vec(100,20))
        self.main_text = Text(vec(Constant.WINDOW_WIDTH / 2, 50), "Option menu", color=pygame.Color("White"))

    def display_option(self):
        AudioManager().play_music()
        pygame.display.set_caption("Option")
        while True:
            self.display_surface.fill((0,0,0))
            option_mouse_pos = pygame.mouse.get_pos()
            self.back_button.draw(self.display_surface)
            self.volume_slider.render(self.display_surface)
            self.music_slider.render(self.display_surface)
            self.bruitage_slider.render(self.display_surface)
            self.main_text.draw_center(self.display_surface)

            handle_slider(self.volume_slider)
            handle_slider(self.music_slider)
            handle_slider(self.bruitage_slider)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.volume_slider.update_slider(vec(option_mouse_pos))
                    self.music_slider.update_slider(vec(option_mouse_pos))
                    self.bruitage_slider.update_slider(vec(option_mouse_pos))
                    if self.back_button.is_clicked(option_mouse_pos):
                        return

            print(self.volume_slider.value)
            VolumeManager().update_general_volume(self.volume_slider.value)
            AudioManager().update_music_volume()
            pygame.display.update()

