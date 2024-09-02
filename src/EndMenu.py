import pygame

class EndMenu:
    def __init__(self, display_surface, score, player, enemies):
        self.display_surface = display_surface
        self.score = score
        self.player = player
        self.enemies = enemies
        self.font = pygame.font.Font('./assets/font/upheavtt.ttf', 50)
        self.button_font = pygame.font.Font('./assets/font/upheavtt.ttf', 30)
        self.button_rect = pygame.Rect(0, 0, 200, 50)
        self.button_rect.center = (display_surface.get_width() // 2, display_surface.get_height() // 2 + 100)
        self.background_surface = pygame.Surface(display_surface.get_size())

    def display(self):
        # Display score
        score_text = self.font.render(f'Score: {self.score}', True, (0, 0, 0))
        score_rect = score_text.get_rect(center=(self.display_surface.get_width() // 2, self.display_surface.get_height() // 2 - 50))
        self.display_surface.blit(score_text, score_rect)

        # Display "Play Again" button
        button_text = self.button_font.render('Play Again', True, (255, 255, 255))
        button_text_rect = button_text.get_rect(center=self.button_rect.center)
        pygame.draw.rect(self.display_surface, (255, 0, 0), self.button_rect)
        self.display_surface.blit(button_text, button_text_rect)

        # Display player
        self.player.draw(self.display_surface)

        # Display enemies
        for enemy in self.enemies:
            enemy.draw(self.display_surface)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.button_rect.collidepoint(event.pos):
                    return 'play_again'
        return None