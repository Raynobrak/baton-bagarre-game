import pygame

class PauseMenu:
    def __init__(self, display_surface, options=None):
        self.option_rects = None
        self.display_surface = display_surface
        self.font = pygame.font.Font('./assets/font/upheavtt.ttf', 50)
        self.options = options if options else ['Resume', 'Options', 'Main Menu', 'Quit']
        self.selected_option = 0
        self.hovered_option = None

    def display_menu(self):
        pygame.display.set_caption("Pause Menu")

        # Create a transparent overlay
        overlay = pygame.Surface(self.display_surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 1))

        # Blit the overlay onto the display surface
        self.display_surface.blit(overlay, (0, 0))

        self.option_rects = []
        for i, option in enumerate(self.options):
            if i == self.selected_option:
                color = (255, 255, 255)
            elif i == self.hovered_option:
                color = (150, 150, 150)
            else:
                color = (100, 100, 100)
            text_surface = self.font.render(option, True, color)
            text_rect = text_surface.get_rect(center=(self.display_surface.get_width() // 2, 200 + i * 100))
            self.display_surface.blit(text_surface, text_rect)
            self.option_rects.append(text_rect)
        pygame.display.update()

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    return self.options[self.selected_option]
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return self.handle_mouse_click(event.pos)
            elif event.type == pygame.MOUSEMOTION:
                self.handle_mouse_hover(event.pos)
            elif event.type == pygame.QUIT:
                pygame.quit()
                exit()
        return None

    def handle_mouse_click(self, mouse_pos):
        for i, rect in enumerate(self.option_rects):
            if rect.collidepoint(mouse_pos):
                return self.options[i]
        return None

    def handle_mouse_hover(self, mouse_pos):
        for i, rect in enumerate(self.option_rects):
            if rect.collidepoint(mouse_pos):
                self.hovered_option = i
                return
        self.hovered_option = None