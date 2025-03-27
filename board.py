import os
import pygame
from card import Card
import time
import random
from round_button import RoundButton
from particle_effect import ParticleEffect
from score_popup import ScorePopup

class Board:

    def __init__(self, game, filename=None):

        self.game = game

        self.score = 0
        self.timer = 0
        self.remaining_shuffles = 3
        self.last_score_update = time.time()
        self.last_removed_time = 0

        self.filename = filename
        self.grid = []
        self.cards = []
        self.selected_cards = []
        self.n_cells_X = 0
        self.n_cells_Y = 0

        self.width_start = 0.1 * game.width
        self.width_end = 0.9 * game.width
        self.height_start = 0.1 * game.height
        self.height_end = 0.9 * game.height

        self.buttons = []

        self.play_mat_rect = pygame.Rect(self.width_start - 3*self.game.level_offset, self.height_start - 2*self.game.level_offset, self.width_end - self.width_start + 5*self.game.level_offset, self.height_end - self.height_start + 4*self.game.level_offset)
        self.game.images.resize_play_mat_bg(self.width_end - self.width_start + 5*self.game.level_offset, self.height_end - self.height_start + 4*self.game.level_offset)

        self.current_card = None


        if filename == None:
            self.generate_grid(4, 13, 8)
        else:
            self.load_from_file()
        self.analyse_board()

        self.card_width = (self.width_end + self.game.level_offset - self.width_start) / self.n_cells_X
        self.card_height = (self.height_end - self.game.level_offset - self.height_start) / self.n_cells_Y

        self.game.level_offset = int(self.card_width / 10)

        self.load_game_elements()

        print(f"n_cells_X: {self.n_cells_X}, n_cells_Y: {self.n_cells_Y}")
        print(f"card_width: {self.card_width}, card_height: {self.card_height}")
        print(f"window_width: {self.game.width}, window_height: {self.game.height}")

        pygame.font.init()
        self.font = pygame.font.Font(None, 40)

        self.init_buttons()

        self.shuffle_animation = 10
        self.current_animation = False
        self.last_time_shuffle_animation = time.time()

        self.particle_effects = []
        self.score_popups = []

        self.current_combo = 1


    def init_buttons(self):


        self.buttons.append(RoundButton(self.game, 
                                        int(self.game.width * 0.035), 
                                        int(self.game.width * 0.035), 
                                        self.game.width // 40, 
                                        self.game.images.pause_icon, 
                                        self.pause_button_action))
    

        self.buttons.append(RoundButton(self.game, 
                                        int(self.game.width * 0.035), 
                                        int(self.game.height / 2), 
                                        self.game.width // 40, 
                                        self.game.images.shuffle_icon, 
                                        self.shuffle_button_action))
        

        self.buttons.append(RoundButton(self.game, 
                                        int(self.game.width * 0.035), 
                                        int(self.game.height - self.game.width * 0.035), 
                                        self.game.width // 40, 
                                        self.game.images.sound_off_icon if self.game.is_muted else self.game.images.sound_on_icon, 
                                        self.sound_button_action))


        self.buttons.append(RoundButton(self.game, 
                                        int(self.game.width - self.game.width * 0.035), 
                                        int(self.game.height / 2), 
                                        self.game.width // 40, 
                                        self.game.images.idea_icon, 
                                        self.idea_button_action))


    def sound_button_action(self, button):
        self.game.mute_button_action()
        self.buttons[2].image = self.game.images.sound_off_icon if self.game.is_muted else self.game.images.sound_on_icon
        self.game.main_menu.buttons[3].image = self.game.images.sound_off_icon if self.game.is_muted else self.game.images.sound_on_icon

    def pause_button_action(self, button):
        self.buttons[0].image = self.game.images.resume_icon
        self.buttons[0].draw()
        self.game.switch_to_pause()

    def shuffle_button_action(self, button):

        if self.remaining_shuffles == 0:
            return
        
        self.shuffle_board()
        self.remaining_shuffles -= 1
        self.current_animation = True

    
    def idea_button_action(self, button):

        for card in self.cards:
            if card.is_highlighted:
                return
        
        pairs = self.get_removable_pairs()

        if len(pairs) > 0:
            pair = random.choice(pairs)
            pair[0].is_highlighted = True
            pair[1].is_highlighted = True

                
    def get_removable_pairs(self):
        
        removable_pairs = []

        for c1 in self.cards:
            if not c1.is_removable():
                continue
            for c2 in self.cards:
                if c1 == c2:
                    continue
                if not c2.is_removable():
                    continue
                if c1.c_type == c2.c_type:
                    removable_pairs.append((c1, c2))
        
        return removable_pairs

    def update(self):

        if self.current_animation:

            current_time = time.time()

            if current_time - self.last_time_shuffle_animation > 0.1:
                self.shuffle_board()
            

        max_level_selected_card = None
        cards_to_unhover = []

        for card in self.cards:
            
            card.update()

            if card.is_hovered:
                
                if max_level_selected_card == None:
                    max_level_selected_card = card
                else:

                    if max_level_selected_card.level < card.level:
                        cards_to_unhover.append(max_level_selected_card)
                        max_level_selected_card = card

                    elif max_level_selected_card.level == card.level:

                        if max_level_selected_card.inside_card_side and card.inside_card:

                            cards_to_unhover.append(max_level_selected_card)
                            max_level_selected_card = card
                        else:
                            card.is_hovered = False

                    else:
                        card.is_hovered = False
        
        for card in cards_to_unhover:
            card.is_hovered = False
        
        self.current_card = max_level_selected_card

        for button in self.buttons:
            button.update()

        self.particle_effects = [p for p in self.particle_effects if p.update()]
        self.score_popups = [s for s in self.score_popups if s.update()]


        current_time = time.time()

        if current_time - self.last_score_update >= 1:
            self.timer += 1
            self.last_score_update = current_time

    def format_timer(self):

        m = self.timer // 60
        s = self.timer % 60

        m_str = str(m)
        if m < 10:
            m_str = "0" + m_str
        
        s_str = str(s)
        if s < 10:
            s_str = "0" + s_str
        
        return f"{m_str}:{s_str}"



    def draw_score_popup(self, surface):
        popup_width, popup_height = 190, 100
        popup_x, popup_y = self.game.width - popup_width - 20, 10

        popup_surface = pygame.Surface((popup_width, popup_height), pygame.SRCALPHA)
        popup_surface.fill((0, 0, 0, 150))

        m = self.timer // 60
        s = self.timer % 60

        m_str = str(m)
        if m < 10:
            m_str = "0" + m_str
        
        s_str = str(s)
        if s < 10:
            s_str = "0" + s_str

        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))

        time_text = self.font.render(f"Timer: {self.format_timer()}", True, (255, 255, 255))

        popup_surface.blit(score_text, (10, 10))
        popup_surface.blit(time_text, (10, 50))

        surface.blit(popup_surface, (popup_x, popup_y))

    
    
    def draw(self):

        self.game.screen.blit(self.game.images.game_background, (0,0))

        self.game.screen.blit(self.game.images.play_mat_background, self.play_mat_rect.topleft)

        pygame.draw.rect(self.game.screen, "black", self.play_mat_rect, width=10, border_radius=10)

        for card in self.cards:
            card.draw()

        self.draw_score_popup(self.game.screen)

        for button in self.buttons:
            button.draw()

        for effect in self.particle_effects:
            effect.draw(self.game.screen)
        for popup in self.score_popups:
            popup.draw(self.game.screen, self.font)

        text_surface = self.font.render(f"{self.remaining_shuffles}/3", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(int(self.game.width * 0.035), int(self.game.height / 2 + self.game.pause_icon_size)))
        self.game.screen.blit(text_surface, text_rect) 



    def handle_click(self):

        for button in self.buttons:
            if button.is_hovered:
                button.handle_click()

        if self.current_card == None:
            return
        
        
        if self.current_card.is_removable():

            if self.current_card.is_selected and self.selected_cards.__contains__(self.current_card):
                self.current_card.is_selected = False
                self.selected_cards.remove(self.current_card)
            else:

                if len(self.selected_cards) >= 2:
                    return

                self.current_card.is_selected = True
                self.selected_cards.append(self.current_card)

                if len(self.selected_cards) == 2:

                    if self.selected_cards[0].c_type == self.selected_cards[1].c_type:

                        # Paire de cartes à retirer

                        x1, y1 = self.selected_cards[0].card_rect.center
                        x2, y2 = self.selected_cards[1].card_rect.center

                        self.particle_effects.append(ParticleEffect(x1, y1))
                        self.particle_effects.append(ParticleEffect(x2, y2))

  
                        self.selected_cards[0].delete()
                        self.selected_cards[1].delete()
                        self.selected_cards.clear()
                        
                        self.game.sounds.click_sound.play()

                        actual_time = time.time()

                        score_gain = 10

                        if actual_time - self.last_removed_time < 3:
                            self.current_combo += 1
                            score_gain *= self.current_combo
                        else:
                            self.current_combo = 1

                        self.score += score_gain

                        self.score_popups.append(ScorePopup(x1, y1, score_gain))
                        self.score_popups.append(ScorePopup(x2, y2, score_gain))

                        self.last_removed_time = actual_time

                        removable_pairs = self.get_removable_pairs()

                        if len(self.cards) == 0:
                            self.game.switch_to_end()
                            return

                        if len(removable_pairs) == 0:
                            
                            if self.remaining_shuffles == 0:
                                self.game.switch_to_end()
                                return
                            
                            self.shuffle_board()
                            self.current_animation = True

                    else:
                        self.selected_cards.pop(0).is_selected = False


    def handle_keyboard(self, keyPressed):
        if keyPressed == pygame.K_ESCAPE:
            self.pause_button_action(None)



    def analyse_board(self):

        assert len(self.grid) > 2 and len(self.grid[0]) > 0 and len(self.grid[0][0]) > 0

        self.n_cells_X = len(self.grid[0][0])
        self.n_cells_Y = len(self.grid[0])

        for i in range(len(self.grid)):

            current_2d = self.grid[i]

            x_to_check = self.n_cells_X
            y_to_check = self.n_cells_Y

            if i == len(self.grid) - 1:
                x_to_check -= 1
                y_to_check -= 1

            if len(current_2d) != y_to_check:
                raise Exception("La taille de la grille est incorrecte.")
            
            for line in current_2d:
                if len(line) != x_to_check:
                    raise Exception("La taille de la grille est incorrecte")
    


    def load_game_elements(self):


        for level in range(len(self.grid)):

            for i in range(len(self.grid[level])):

                for j in range(len(self.grid[level][i]) - 1, -1, -1):

                    if self.grid[level][i][j] == 0:
                        continue
                   
                    self.cards.append(Card(self, self.grid[level][i][j], level, j, i))

    
    def load_from_file(self):

        self.grid = []

        if not os.path.isfile(self.filename):
            raise Exception(f"Le fichier du niveau {self.filename} est introuvable.")
        
        with open(self.filename, "r") as file:

            current_2d = []

            for line in file:

                line = line.strip()

                if line == "":

                    if len(current_2d) > 0:
                        self.grid.append(current_2d)
                        current_2d = []
                
                else:

                    line = line.split(" ")

                    current_line = []

                    for char in line:
                        
                        current_line.append(int(char))
                    
                    current_2d.append(current_line)

            if len(current_2d) > 0:
                self.grid.append(current_2d)




    def export_to_file(self, filename : str):

        with open(filename, "w+") as file:

            for i in range(len(self.grid)):

                current_2d = self.grid[i]

                for j in range(len(current_2d)):
                    
                    line = current_2d[j]

                    sb = ""
                    
                    for k in range(len(line)):

                        space = " "

                        if k == len(line) - 1:
                            space = ""

                        sb += str(line[k]) + space

                    return_char = "\n"

                    if i == len(self.grid) - 1 and j == len(current_2d) - 1:
                        return_char = ""

                    file.write(sb + return_char)

                if i == len(self.grid) - 1:
                    continue

                file.write("\n")

    
    def generate_grid(self, n_levels, n_cells_X, n_cells_Y):

        self.grid = []
        base_fill_ratio = 0.9
        top_fill_ratio = 0.4
        
        for level in range(n_levels):
            level_width = n_cells_X - 1 if level == n_levels - 1 else n_cells_X
            level_height = n_cells_Y - 1 if level == n_levels - 1 else n_cells_Y
            self.grid.append([[0 for _ in range(level_width)] for _ in range(level_height)])
        
        max_card_types = min(38, len(self.game.images.cards))
        card_type = 1
        
        for level in range(n_levels):
            fill_ratio = base_fill_ratio - ((base_fill_ratio - top_fill_ratio) * (level / (n_levels - 1)))
            num_cells = sum(len(row) for row in self.grid[level])
            num_pairs = int((num_cells * fill_ratio) // 2)
            available_positions = []
            

            for y in range(len(self.grid[level])):
                for x in range(len(self.grid[level][y])):
                    if level == 0 or self.grid[level - 1][y][x] != 0:
                        available_positions.append((level, y, x))
            
            random.shuffle(available_positions)
            
            while len(available_positions) >= 2 and num_pairs > 0:
                pos1 = available_positions.pop()
                pos2 = available_positions.pop()
                
                self.grid[pos1[0]][pos1[1]][pos1[2]] = card_type
                self.grid[pos2[0]][pos2[1]][pos2[2]] = card_type
                
                card_type += 1
                if card_type > max_card_types:
                    card_type = 1
                
                num_pairs -= 1
    

    def shuffle_board(self):

    
        self.shuffle_animation -= 1

        if self.shuffle_animation == 0:
            self.shuffle_animation = 10
            self.current_animation = False
            return
        

        cards = []
        positions = []

        for level in range(len(self.grid)):
            for y in range(self.n_cells_Y - 1 if level == len(self.grid) - 1 else self.n_cells_Y):
                for x in range(self.n_cells_X - 1 if level == len(self.grid) - 1 else self.n_cells_X):
                    
                    card = self.grid[level][y][x]

                    if card == 0:
                        continue

                    cards.append(card)
                    positions.append((level, y, x))

        random.shuffle(cards)

        for i in range(len(positions)):
            position = positions[i]
            self.grid[position[0]][position[1]][position[2]] = cards[i]

        self.cards = []
        self.load_game_elements()

        self.last_time_shuffle_animation = time.time()

        removable_pairs = self.get_removable_pairs()
        if len(removable_pairs) == 0 and len(self.cards) > 0:
            self.shuffle_board()

