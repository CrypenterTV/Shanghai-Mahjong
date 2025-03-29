import pygame
from button import Button
from tkinter import filedialog
from tkinter import messagebox
import board_helper


class PauseMenu:

    def __init__(self, game):

        self.game = game

        self.top_left_corner_x = self.game.width // 4
        self.top_left_corner_y = self.game.height // 4

        self.buttons = []

        self.font_size = self.game.width // 33
        self.font = pygame.font.Font("assets/fonts/font2_test.ttf", self.font_size)
        self.font_2 = pygame.font.Font("assets/fonts/font2_test.ttf", int(0.8 * self.font_size))

        button_spacing = self.game.height // 25
        button_height = self.game.height // 18
        start_buttons_height = self.game.height // 2.20


        self.buttons.append(Button(self.game,
                                   "REPRENDRE",
                                   (234, 161, 14),
                                   self.game.width // 2,
                                   start_buttons_height,
                                   self.game.width // 4,
                                   button_height,
                                   self.font_2,
                                   self.resume_action_button))
        

        self.buttons.append(Button(self.game,
                                   "SAUVEGARDER",
                                   (234, 161, 14),
                                   self.game.width // 2,
                                   start_buttons_height + button_spacing + button_height,
                                   self.game.width // 4,
                                   button_height,
                                   self.font_2,
                                   self.save_action_button))
        
        self.buttons.append(Button(self.game,
                                   "RETOUR AU MENU",
                                   (234, 161, 14),
                                   self.game.width // 2,
                                   start_buttons_height + 2 * (button_spacing + button_height),
                                   self.game.width // 4,
                                   button_height,
                                   self.font_2,
                                   self.main_menu_action_button))
        

    def resume_action_button(self, button):
        self.handle_keyboard(pygame.K_ESCAPE)


    def save_action_button(self, button):
        
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", 
                                                 filetypes=[("Fichier de sauvegarde", "*.txt"), ("Tous les fichiers", "*.*")],
                                                 title="Sélectionnez l'emplacement de sauvegarde du niveau.")

        if file_path:
            board_helper.export_to_file(self.game.board, file_path)

            messagebox.showinfo("Enregistrement", f"Votre partie a été sauvegardée avec succès à l'emplacement : ${file_path} !")



    def main_menu_action_button(self, button):

        if messagebox.askokcancel("Retour au Menu", "Voulez vous quitter la partie en cours et revenir au menu principal ? \nAttention: Pensez à enregistrer votre partie si vous souhaitez y revenir plus tard."):
            self.game.switch_to_main()


    def update(self):
        for button in self.buttons:
            button.update()


    def draw(self):

        background_surface = pygame.Surface((self.game.width // 2, self.game.height // 2), pygame.SRCALPHA)
        pygame.draw.rect(background_surface, (45, 44, 40, 200), background_surface.get_rect(), border_radius=20)
        self.game.screen.blit(background_surface, (self.top_left_corner_x, self.top_left_corner_y))
        
        text_surface = self.font.render("MENU PAUSE", True, (234, 161, 14))
        text_rect = text_surface.get_rect(center=(self.game.width // 2, 13 * self.game.height // 36))
        self.game.screen.blit(text_surface, text_rect)

        for button in self.buttons:
            button.draw()


    def handle_click(self):
        for button in self.buttons:
            if button.is_hovered:
                button.handle_click()


    def handle_keyboard(self, keyPressed):
        if keyPressed == pygame.K_ESCAPE:
            self.game.switch_to_game()