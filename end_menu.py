import pygame
from button import Button

class EndMenu:

    def __init__(self, game):

        self.game = game
        self.buttons = []

        self.top_left_corner_x = self.game.width // 4
        self.top_left_corner_y = self.game.height // 4

        self.buttons = []

        self.font_size = self.game.width // 33
        self.font = pygame.font.Font("assets/fonts/font2_test.ttf", self.font_size)
        self.font_2 = pygame.font.Font("assets/fonts/font2_test.ttf", int(0.8 * self.font_size))

        self.button_spacing = self.game.height // 25
        self.button_height = self.game.height // 18
        self.start_buttons_height = self.game.height // 2.20

        self.buttons.append(Button(self.game,
                                   "RETOUR AU MENU",
                                   (234, 161, 14),
                                   self.game.width // 2,
                                   self.start_buttons_height + 2 * (self.button_spacing + self.button_height),
                                   self.game.width // 4,
                                   self.button_height,
                                   self.font_2,
                                   self.main_menu_action_button))
    
    def main_menu_action_button(self, button):
        self.game.switch_to_main()

    def update(self):
        for button in self.buttons:
            button.update()

    def draw(self):

        background_surface = pygame.Surface((self.game.width // 2, self.game.height // 2), pygame.SRCALPHA)
        pygame.draw.rect(background_surface, (45, 44, 40, 200), background_surface.get_rect(), border_radius=20)
        self.game.screen.blit(background_surface, (self.top_left_corner_x, self.top_left_corner_y))
        
        self.background_drawed = True
        text_surface = self.font.render("PARTIE TERMINEE", True, (234, 161, 14))
        text_rect = text_surface.get_rect(center=(self.game.width // 2, 13 * self.game.height // 36))
        self.game.screen.blit(text_surface, text_rect)

        text_surface2 = self.font_2.render(f"SCORE : {self.game.board.score}", True, (234, 161, 14))
        text_rect2 = text_surface2.get_rect(center=(self.game.width // 2, self.start_buttons_height))
        self.game.screen.blit(text_surface2, text_rect2)

        text_surface3 = self.font_2.render(f"TEMPS : {self.game.board.format_timer()}", True, (234, 161, 14))
        text_rect3 = text_surface3.get_rect(center=(self.game.width // 2, self.start_buttons_height + self.button_height))
        self.game.screen.blit(text_surface3, text_rect3)

        for button in self.buttons:
            button.draw()
    
    def handle_click(self):
        for button in self.buttons:
            if button.is_hovered:
                button.handle_click()

    def handle_keyboard(self, keyPressed):
        pass