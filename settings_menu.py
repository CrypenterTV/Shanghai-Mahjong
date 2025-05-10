import pygame
from button import Button
from round_button import RoundButton

class SettingsMenu:

    def __init__(self, game):

        self.game = game

        self.top_left_corner_x = self.game.width // 4
        self.top_left_corner_y = self.game.height // 4

        self.buttons = []

        self.font_size = self.game.width // 33
        self.font = pygame.font.Font("assets/fonts/font2_test.ttf", self.font_size)
        self.font_2 = pygame.font.Font("assets/fonts/font2_test.ttf", int(0.8 * self.font_size))

        self.button_height = self.game.height // 18

        self.grid_size_z = self.game.preferences.get_value("grid_size_z", 4)
        self.grid_size_x = self.game.preferences.get_value("grid_size_x", 13)
        self.grid_size_y = self.game.preferences.get_value("grid_size_y", 8)

        self.buttons.append(Button(self.game,
                                   "FERMER",
                                   (234, 161, 14),
                                   self.game.width // 2,
                                   3 * self.top_left_corner_y - int(1.5 * self.button_height),
                                   self.game.width // 4,
                                   self.button_height,
                                   self.font_2,
                                   self.close_button_action))
        

        self.buttons.append(RoundButton(self.game, 
                                        5 * self.game.width // 16, 
                                        int(self.game.height / 2), 
                                        self.game.width // 65, 
                                        self.game.images.minus_icon, 
                                        self.minus_x_button_action))

        self.buttons.append(RoundButton(self.game, 
                                        self.game.width - 5 * self.game.width // 16, 
                                        int(self.game.height / 2), 
                                        self.game.width // 65, 
                                        self.game.images.plus_icon, 
                                        self.plus_x_button_action))

        self.buttons.append(RoundButton(self.game, 
                                        5 * self.game.width // 16, 
                                        self.game.height // 2 - self.game.height // 12, 
                                        self.game.width // 65, 
                                        self.game.images.minus_icon, 
                                        self.minus_z_button_action))
    
        self.buttons.append(RoundButton(self.game, 
                                        self.game.width - 5 * self.game.width // 16, 
                                        self.game.height // 2 - self.game.height // 12, 
                                        self.game.width // 65, 
                                        self.game.images.plus_icon, 
                                        self.plus_z_button_action))

        self.buttons.append(RoundButton(self.game, 
                                        5 * self.game.width // 16, 
                                        self.game.height // 2 + self.game.height // 12, 
                                        self.game.width // 65, 
                                        self.game.images.minus_icon, 
                                        self.minus_y_button_action))

        self.buttons.append(RoundButton(self.game, 
                                        self.game.width - 5 * self.game.width // 16, 
                                        self.game.height // 2 + self.game.height // 12, 
                                        self.game.width // 65, 
                                        self.game.images.plus_icon, 
                                        self.plus_y_button_action))


    # Fonctions d'actions des boutons pour incrémenter / décrémenter les valeurs des paramètres
    def minus_x_button_action(self, button):
        
        if self.grid_size_x <= 5:
            return
        
        self.grid_size_x -= 1

    def plus_x_button_action(self, button):
        
        if self.grid_size_x >= 20:
            return
        
        self.grid_size_x += 1

    def plus_z_button_action(self, button):
        
        if self.grid_size_z >= 7:
            return
        
        self.grid_size_z += 1

    def minus_z_button_action(self, button):

        if self.grid_size_z <= 3:
            return
        
        self.grid_size_z -= 1

    def minus_y_button_action(self, button):

        if self.grid_size_y <= 7:
            return
        
        self.grid_size_y -= 1

    def plus_y_button_action(self, button):

        if self.grid_size_y >= 20:
            return
        
        self.grid_size_y += 1


    def close_button_action(self, button):
        # A la fermeture du menu, on sauvegarde les changements dans le fichier JSON
        self.game.preferences.update_preference("grid_size_z", self.grid_size_z)
        self.game.preferences.update_preference("grid_size_x", self.grid_size_x)
        self.game.preferences.update_preference("grid_size_y", self.grid_size_y)
        self.game.preferences.write_preferences()
        self.game.switch_to_main()

    def update(self):
        for button in self.buttons:
            button.update()

    def draw(self):

        background_surface = pygame.Surface((self.game.width // 2, self.game.height // 2), pygame.SRCALPHA)
        pygame.draw.rect(background_surface, (45, 44, 40, 200), background_surface.get_rect(), border_radius=20)
        self.game.screen.blit(background_surface, (self.top_left_corner_x, self.top_left_corner_y))
        
        text_surface = self.font.render("PARAMETRES", True, (234, 161, 14))
        text_rect = text_surface.get_rect(center=(self.game.width // 2, 12 * self.game.height // 36))
        self.game.screen.blit(text_surface, text_rect)

        text_surface2 = self.font_2.render(f"Hauteur Grille (Z) : {self.grid_size_z}", True, (255, 255, 255))
        text_rect2 = text_surface2.get_rect(center=(self.game.width // 2, self.game.height // 2 - self.game.height // 12))
        self.game.screen.blit(text_surface2, text_rect2)

        text_surface3 = self.font_2.render(f"Largeur Grille (X) : {self.grid_size_x}", True, (255, 255, 255))
        text_rect3 = text_surface3.get_rect(center=(self.game.width // 2, self.game.height // 2))
        self.game.screen.blit(text_surface3, text_rect3)

        text_surface4 = self.font_2.render(f"Longueur Grille (Y) : {self.grid_size_y}", True, (255, 255, 255))
        text_rect4 = text_surface4.get_rect(center=(self.game.width // 2, self.game.height // 2 + self.game.height // 12))
        self.game.screen.blit(text_surface4, text_rect4)

        for button in self.buttons:
            button.draw()

    def handle_click(self):
        for button in self.buttons:
            if button.is_hovered:
                button.handle_click()

    def handle_keyboard(self, keyPressed):
        if keyPressed == pygame.K_ESCAPE:
            self.game.switch_to_main()