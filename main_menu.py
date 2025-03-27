import pygame
import sys
from button import Button
from board import Board
from tkinter import filedialog

from round_button import RoundButton

class MainMenu:

    def __init__(self, game):
        self.game = game
        self.buttons = []

        self.game.images.resize_main_title(self.game.width // 2, self.game.height // 4)

        start_buttons_height = int(0.45 * self.game.height)
        button_width = self.game.width // 3
        button_height = self.game.height // 7
        button_spacing = self.game.height // 25
        font_size = self.game.width // 33 #50 #25
        font = pygame.font.Font("assets/fonts/font2_test.ttf", font_size)

        self.logo_x = (self.game.width - self.game.images.main_title.get_width()) // 2
        self.logo_y = self.game.height // 11

        self.buttons.append(Button(self.game, 
                                   "NOUVELLE PARTIE",
                                   (234, 161, 14),
                                   self.game.width // 2, 
                                   start_buttons_height, 
                                   button_width, 
                                   button_height,
                                   font,
                                   self.play_button_action))
        
        self.buttons.append(Button(self.game, 
                                   "CHARGER NIVEAU", 
                                   (234, 161, 14),
                                   self.game.width // 2, 
                                   start_buttons_height + button_height + button_spacing, 
                                   button_width, 
                                   button_height,
                                   font,
                                   self.selection_level_button_action))
        
        self.buttons.append(Button(self.game, 
                                   "QUITTER",
                                   (234, 161, 14),
                                   self.game.width // 2, 
                                   start_buttons_height + 2 * (button_height + button_spacing), 
                                   button_width, 
                                   button_height,
                                   font,
                                   self.exit_button_action))
        
        self.buttons.append(RoundButton(self.game, 
                                        int(self.game.width * 0.035), 
                                        int(self.game.height - self.game.width * 0.035), 
                                        self.game.width // 40, 
                                        self.game.images.sound_off_icon if self.game.is_muted else self.game.images.sound_on_icon, 
                                        self.sound_button_action))


    def sound_button_action(self, button):
        self.game.mute_button_action()
        self.buttons[3].image = self.game.images.sound_off_icon if self.game.is_muted else self.game.images.sound_on_icon

    def exit_button_action(self, button):
        sys.exit()

    def play_button_action(self, button):
        self.game.board = Board(self.game)
        self.game.images.resize_cards(self.game.board.card_width, self.game.board.card_height)
        self.game.switch_to_game()

    def selection_level_button_action(self, button):

        file_path = filedialog.askopenfilename(title="Sélectionnez un niveau", 
                                               filetypes=[("Fichiers texte", "*.txt")])
        
        if file_path:

            self.game.board = Board(self.game, file_path)
            self.game.images.resize_cards(self.game.board.card_width, self.game.board.card_height)
            self.game.switch_to_game()


    
    def update(self):
        for button in self.buttons:
            button.update()

    def draw(self):

        self.game.screen.blit(self.game.images.game_background, (0,0))

        self.game.screen.blit(self.game.images.main_title, (self.logo_x, self.logo_y))

        for button in self.buttons:
            button.draw()

    def handle_click(self):
        for button in self.buttons:
            if button.is_hovered:
                button.handle_click()
    
    def handle_keyboard(self, keyPressed):
        print(keyPressed)

