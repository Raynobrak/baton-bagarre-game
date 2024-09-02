import pygame
from src.Fire import Fire
from src.ImageManager import ImageManager
from src.Constant import Constant

vec = pygame.math.Vector2  # 2 for two dimensional


class LightManager:
    K = 1 / 3  # Chosen ratio of the circle's size to the window's size

    def __init__(self, fire: Fire):
        self.fire = fire
        self.original_circle = ImageManager().get_image('circle')
        self.filter_color = None
        self.light_filter = pygame.surface.Surface((Constant.WINDOW_WIDTH, Constant.WINDOW_HEIGHT))

    def update(self):
        # Calculate the subsurface of the circle needed and then scale it to the size of the window
        fire_pos = self.fire.get_position()
        fire_size = self.fire.size
        fire_life_points = self.fire.life_points
        fire_center = fire_pos + fire_size / 2
        circle_size = vec(self.original_circle.get_width(), self.original_circle.get_height())

        if Constant.WINDOW_WIDTH > Constant.WINDOW_HEIGHT:
            ratio = Constant.WINDOW_WIDTH / circle_size.x
        else:
            ratio = Constant.WINDOW_HEIGHT / circle_size.y

        if fire_life_points == 0:  # Prevent division by zero
            fire_life_points = 1

        new_screen_width = (Constant.WINDOW_WIDTH / ratio) * self.K * (Fire.MAX_HEALTH / fire_life_points)
        new_screen_height = (Constant.WINDOW_HEIGHT / ratio) * self.K * (Fire.MAX_HEALTH / fire_life_points)

        fire_ratio_x = fire_center.x / Constant.WINDOW_WIDTH
        fire_ratio_y = fire_center.y / Constant.WINDOW_HEIGHT
        new_fire_center = vec(new_screen_width * fire_ratio_x, new_screen_height * fire_ratio_y)

        new_screen_pos = circle_size / 2 - new_fire_center

        # Check if the circle is bigger than the window
        if (new_screen_width < circle_size.x and new_screen_height < circle_size.y and
                new_screen_pos.x > 0 and new_screen_pos.y > 0 and
                new_screen_pos.x + new_screen_width < circle_size.x and new_screen_pos.y + new_screen_height < circle_size.y):
            # Get the sub-surface of the circle image to fit in the screen
            circle = self.original_circle.subsurface(pygame.Rect(new_screen_pos, vec(new_screen_width, new_screen_height)))
            circle = pygame.transform.smoothscale(circle, (Constant.WINDOW_WIDTH, Constant.WINDOW_HEIGHT))
            circle_pos = (0, 0)
        else:
            # Calculate the size and position to center the circle with the fire
            new_circle_size = (Constant.WINDOW_WIDTH * (1 / self.K)) * (fire_life_points / Fire.MAX_HEALTH)
            circle = pygame.transform.smoothscale(self.original_circle, (int(new_circle_size), int(new_circle_size)))
            circle_pos = (fire_center.x - circle.get_width() / 2, fire_center.y - circle.get_height() / 2)

        # Create a light filter to darken the screen
        self.filter_color = 255 * (1 - fire_life_points / Fire.MAX_HEALTH)
        self.light_filter.fill((self.filter_color, self.filter_color, self.filter_color))
        self.light_filter.blit(circle, circle_pos)

    def draw(self, display):
        display.blit(self.light_filter, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
