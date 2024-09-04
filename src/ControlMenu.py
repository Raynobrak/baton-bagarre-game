import pygame


class ControlMenu:
    def __init__(self, display_surface, options=None):
        self.option_rects = None
        self.display_surface = display_surface
        self.title_font = pygame.font.Font('./assets/font/upheavtt.ttf',
                                           50)  # Larger font for title
        self.controls_font = pygame.font.Font('./assets/font/upheavtt.ttf',
                                              30)  # Smaller font for controls text
        self.options = options if options else ['Back']
        self.selected_option = 0
        self.hovered_option = None

    def display_controls(self):
        pygame.display.set_caption("Controls")

        running = True
        while running:
            # Create a transparent overlay
            overlay = pygame.Surface(self.display_surface.get_size(),
                                     pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 1))

            # Blit the overlay onto the display surface
            self.display_surface.blit(overlay, (0, 0))

            # Render the title
            title_surface = self.title_font.render("Controls:", True,
                                                   (255, 255, 255))
            title_rect = title_surface.get_rect(
                center=(self.display_surface.get_width() // 2, 100))
            self.display_surface.blit(title_surface, title_rect)

            # Render the controls text
            controls_text = [
                "Jump: W",
                "Move Left: A",
                "Move Right: D",
                "Punch: Space",
                "Kick: K",
                "Shockwave: Q",
                "Pause: ESC",
                "Select: Enter",
            ]

            for i, line in enumerate(controls_text):
                text_surface = self.controls_font.render(line, True,
                                                         (255, 255, 255))
                text_rect = text_surface.get_rect(center=(
                self.display_surface.get_width() // 2, 150 + i * 50))
                self.display_surface.blit(text_surface, text_rect)

            # Render the 'Back' option
            back_surface = self.title_font.render("Back", True, (255, 255, 255))
            back_rect = back_surface.get_rect(center=(
            self.display_surface.get_width() // 2,
            150 + len(controls_text) * 50))
            self.display_surface.blit(back_surface, back_rect)
            self.option_rects = [back_rect]

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_b or (
                            event.key == pygame.K_RETURN and self.selected_option == 0):
                        running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if back_rect.collidepoint(event.pos):
                        running = False
                elif event.type == pygame.MOUSEMOTION:
                    self.handle_mouse_hover(event.pos)

    def handle_mouse_hover(self, mouse_pos):
        for i, rect in enumerate(self.option_rects):
            if rect.collidepoint(mouse_pos):
                self.hovered_option = i
                return
        self.hovered_option = None