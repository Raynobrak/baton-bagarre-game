import pygame


class EndMenu:
    def __init__(self, display_surface, score, player, enemies):
        self.display_surface = display_surface
        self.score = score
        self.player = player
        self.enemies = enemies
        self.font = pygame.font.Font('./assets/font/upheavtt.ttf', 50)
        self.button_font = pygame.font.Font('./assets/font/upheavtt.ttf', 30)

        # Play Again button
        self.play_again_button_rect = pygame.Rect(0, 0, 200, 50)
        self.play_again_button_rect.center = (display_surface.get_width() //
                                              2, display_surface.get_height()
                                              // 2 + 50)

        # Main Menu button
        self.main_menu_button_rect = pygame.Rect(0, 0, 200, 50)
        self.main_menu_button_rect.center = (display_surface.get_width() //
                                             2, display_surface.get_height()
                                             // 2 + 150)

        self.background_surface = pygame.Surface(display_surface.get_size())

    def display(self):
        # Display score
        score_text = self.font.render(f'Score: {self.score}', True, (0, 0, 0))
        score_rect = score_text.get_rect(center=(
            self.display_surface.get_width() // 2,
            self.display_surface.get_height() // 2 - 50))
        self.display_surface.blit(score_text, score_rect)

        # Display "Play Again" button
        play_again_text = self.button_font.render('Play Again', True,
                                                  (255, 255, 255))
        play_again_text_rect = play_again_text.get_rect(
            center=self.play_again_button_rect.center)
        pygame.draw.rect(self.display_surface, (255, 0, 0),
                         self.play_again_button_rect)
        self.display_surface.blit(play_again_text, play_again_text_rect)

        # Display "Main Menu" button
        main_menu_text = self.button_font.render('Main Menu', True,
                                                 (255, 255, 255))
        main_menu_text_rect = main_menu_text.get_rect(
            center=self.main_menu_button_rect.center)
        pygame.draw.rect(self.display_surface, (0, 0, 255),
                         self.main_menu_button_rect)
        self.display_surface.blit(main_menu_text, main_menu_text_rect)

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
                if self.play_again_button_rect.collidepoint(event.pos):
                    return 'play_again'
                elif self.main_menu_button_rect.collidepoint(event.pos):
                    return 'main_menu'
        return None
