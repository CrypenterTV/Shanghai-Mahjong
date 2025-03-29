import pygame
from card import Card
from button import Button
from round_button import RoundButton
from tkinter import messagebox
from tkinter import filedialog
import board_helper

class LevelEditor:

    def __init__(self, game, levels, n_cells_X, n_cells_Y):
        
        self.game = game

        self.cards = []

        self.buttons = []

        self.levels = levels
        self.n_cells_X = n_cells_X
        self.n_cells_Y = n_cells_Y

        self.grid = []
        self.init_grid()

        self.width_start = 0.1 * game.width
        self.width_end = 0.9 * game.width
        self.height_start = 0.05 * game.height
        self.height_end = 0.85 * game.height

        self.play_mat_rect = pygame.Rect(self.width_start - 3*self.game.level_offset, self.height_start - 2*self.game.level_offset, self.width_end - self.width_start + 5*self.game.level_offset, self.height_end - self.height_start + 4*self.game.level_offset)
        self.game.images.resize_play_mat_bg(self.width_end - self.width_start + 5*self.game.level_offset, self.height_end - self.height_start + 4*self.game.level_offset)

        self.card_width = (self.width_end + self.game.level_offset - self.width_start) / self.n_cells_X
        self.card_height = (self.height_end - self.game.level_offset - self.height_start) / self.n_cells_Y

        self.game.level_offset = int(self.card_width / 10)

        self.current_card = None

        self.font_size = self.game.width // 40
        self.font = pygame.font.Font("assets/fonts/font2_test.ttf", self.font_size)

        self.init_buttons()


    def init_buttons(self):


        self.buttons.append(RoundButton(self.game, 
                                        int(self.game.width * 0.035), 
                                        (self.height_start + self.height_end) // 2, 
                                        self.game.width // 40, 
                                        self.game.images.reset_icon, 
                                        self.reset_button_action))
        
        self.buttons.append(RoundButton(self.game, 
                                        int(self.game.width * 0.035), 
                                        int(self.game.height - self.game.width * 0.035), 
                                        self.game.width // 40, 
                                        self.game.images.sound_off_icon if self.game.is_muted else self.game.images.sound_on_icon, 
                                        self.sound_button_action))
        
        self.buttons.append(Button(self.game,
                                   "QUITTER",
                                   (234, 161, 14),
                                   (self.width_start + self.width_end) // 4,
                                   (self.game.height + self.height_end) // 2,
                                   self.game.width // 4,
                                   self.game.height // 20,
                                   self.font,
                                   self.main_menu_action_button))
        

        self.buttons.append(Button(self.game,
                                   "ENREGISTRER",
                                   (234, 161, 14),
                                   3 * (self.width_start + self.width_end) // 4,
                                   (self.game.height + self.height_end) // 2,
                                   self.game.width // 4,
                                   self.game.height // 20,
                                   self.font,
                                   self.save_button_action))
    
    def init_grid(self):
        self.grid = [[[0 for i in range(self.n_cells_X)] for j in range(self.n_cells_Y)] for k in range(self.levels - 1)]
        self.grid.append([[0 for i in range(self.n_cells_X - 1)] for j in range(self.n_cells_Y - 1)])

    def update(self):
        
        board_helper.sort_cards(self)

        board_helper.update_current_card(self)

        for button in self.buttons:
            button.update()

    def draw(self):

        self.game.screen.blit(self.game.images.game_background, (0,0))

        self.game.screen.blit(self.game.images.play_mat_background, self.play_mat_rect.topleft)

        pygame.draw.rect(self.game.screen, "black", self.play_mat_rect, width=10, border_radius=10)

        self.draw_floor()

        for card in self.cards:
            card.draw()
        
        for button in self.buttons:
            button.draw()

        text_surface = self.font.render(f"{len(self.cards)} tuiles", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.game.width // 2, (self.game.height + self.height_end) // 2))
        self.game.screen.blit(text_surface, text_rect) 

    
    def main_menu_action_button(self, button):
        if messagebox.askokcancel("Retour au Menu", "Voulez-vous quitter l'éditeur de niveau et revenir au menu principal ?\nAttention: Les modifications non sauvegardées seront perdues. Pensez à enregistrer votre niveau dans un fichier via le bouton 'enregistrer'."):
            self.game.switch_to_main()


    def save_button_action(self, button):

        if len(self.cards) < 4 != 0:
            messagebox.showerror("Erreur", "Votre niveau ne contient pas assez de cartes.")
            return
        
        if len(self.cards) % 2 != 0:
            messagebox.showerror("Erreur", "Vous devez avoir un nombre de cartes pair pour avoir un niveau valide.")
            return
        
        
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", 
                                                 filetypes=[("Fichier de sauvegarde", "*.txt"), ("Tous les fichiers", "*.*")],
                                                 title="Sélectionnez l'emplacement de sauvegarde du niveau.")
        if file_path:
            board_helper.export_to_file(self, file_path)

            messagebox.showinfo("Enregistrement", f"Votre niveau a été sauvegardé avec succès à l'emplacement : ${file_path} !")
    

    def reset_button_action(self, button):

        if len(self.cards) == 0:
            return 

        if messagebox.askokcancel("Réinitialisation", "Voulez-vous vider le plateau de jeu ?\nAttention: Les modifications non sauvegardées seront perdues."):
            self.cards.clear()
            self.init_grid()


    def sound_button_action(self, button):
        self.game.mute_button_action()
        self.buttons[1].image = self.game.images.sound_off_icon if self.game.is_muted else self.game.images.sound_on_icon
        self.game.main_menu.buttons[3].image = self.game.images.sound_off_icon if self.game.is_muted else self.game.images.sound_on_icon

    def draw_floor(self):

        for y in range(self.n_cells_Y):
            for x in range(self.n_cells_X):

                coord_x = self.width_start + x * self.card_width - self.game.level_offset
                coord_y = self.height_start + y * self.card_height + self.game.level_offset
                
                rect = pygame.Rect(coord_x, coord_y, self.card_width, self.card_height)

                pygame.draw.rect(self.game.screen, (0,0,0), rect, 2)


    
    def handle_click(self):

        for button in self.buttons:
            if button.is_hovered:
                button.handle_click()

        buttons = pygame.mouse.get_pressed()

        if buttons[0] and buttons[1]:
            return
        
        if buttons[0]:
            
            if self.current_card == None:
                return
            
            self.current_card.delete()

            
        if buttons[2]:

            if self.current_card == None:
                
                mouse_x, mouse_y = pygame.mouse.get_pos()
                cell_x = int((mouse_x - self.width_start) / self.card_width)
                cell_y = int((mouse_y - self.height_start) / self.card_height)

                if 0 <= cell_x < self.n_cells_X and 0 <= cell_y < self.n_cells_Y:
                    self.cards.append(Card(self, -1, 0, cell_x, cell_y, True))
                    self.grid[0][cell_y][cell_x] = -1

                return

            if self.current_card.level + 1 >= self.levels:
                return
            
            if self.current_card.cell_y >= len(self.grid[self.current_card.level + 1]):
                return
            
            if self.current_card.cell_x >= len(self.grid[self.current_card.level + 1][0]):
                return
            
            if self.grid[self.current_card.level + 1][self.current_card.cell_y][self.current_card.cell_x] != 0:
                return
            
            self.cards.append(Card(self, -1, self.current_card.level + 1, self.current_card.cell_x, self.current_card.cell_y, True))
            self.grid[self.current_card.level + 1][self.current_card.cell_y][self.current_card.cell_x] = -1



    def handle_keyboard(self, keyPressed):
        pass


