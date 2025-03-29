import pygame

class SettingsMenu:

    def __init__(self, game):

        self.game = game

        self.top_left_corner_x = self.game.width // 4
        self.top_left_corner_y = self.game.height // 4

        self.buttons = []

        self.font_size = self.game.width // 33
        self.font = pygame.font.Font("assets/fonts/font2_test.ttf", self.font_size)
        self.font_2 = pygame.font.Font("assets/fonts/font2_test.ttf", int(0.8 * self.font_size))


    def update(self):
        for button in self.buttons:
            button.update()

    def draw(self):

        background_surface = pygame.Surface((self.game.width // 2, self.game.height // 2), pygame.SRCALPHA)
        pygame.draw.rect(background_surface, (45, 44, 40, 200), background_surface.get_rect(), border_radius=20)
        self.game.screen.blit(background_surface, (self.top_left_corner_x, self.top_left_corner_y))
        
        text_surface = self.font.render("PARAMETRES", True, (234, 161, 14))
        text_rect = text_surface.get_rect(center=(self.game.width // 2, 13 * self.game.height // 36))
        self.game.screen.blit(text_surface, text_rect)

        for button in self.buttons:
            button.draw()

    def handle_click(self):
        for button in self.buttons:
            if button.is_hovered:
                button.handle_click()

    def handle_keyboard(self, keyPressed):
        self.game.switch_to_main()