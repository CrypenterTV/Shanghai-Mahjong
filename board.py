import os
import pygame
from card import Card
import time
import random
from round_button import RoundButton
from particle_effect import ParticleEffect
from score_popup import ScorePopup
import board_helper

class Board:

    def __init__(self, game, filename=None):

        self.game = game

        self.score = 0
        self.timer = 0
        self.current_combo = 1
        self.remaining_shuffles = 3

        self.last_score_update_time = time.time()
        self.last_removed_time = 0
        self.last_shuffle_animation_time = 0
        self.last_idea_button_time = 0
        self.last_solver_used_time = 0

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

        self.shuffle_animation = 10
        self.removables_cards = 0

        self.ending = False
        self.current_animation = False
        self.auto_solving = False
        self.auto_solving_deleting = False

        self.buttons = []
        self.particle_effects = []
        self.score_popups = []
        self.current_removables = []

        self.play_mat_rect = pygame.Rect(self.width_start - 3*self.game.level_offset, self.height_start - 2*self.game.level_offset, self.width_end - self.width_start + 5*self.game.level_offset, self.height_end - self.height_start + 4*self.game.level_offset)
        self.game.images.resize_play_mat_bg(self.width_end - self.width_start + 5*self.game.level_offset, self.height_end - self.height_start + 4*self.game.level_offset)

        self.current_card = None


        if filename == None:
            self.generate_grid(4, 13, 8)
        else:
            board_helper.load_from_file(self, self.filename)
            
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
                                        int(self.game.height / 2 - self.game.width // 20), 
                                        self.game.width // 40, 
                                        self.game.images.idea_icon, 
                                        self.idea_button_action))


        self.buttons.append(RoundButton(self.game, 
                                        int(self.game.width - self.game.width * 0.035), 
                                        int(self.game.height / 2 + self.game.width // 20), 
                                        self.game.width // 40, 
                                        self.game.images.robot_icon, 
                                        self.auto_solver_button_action))
        

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

        current_time = time.time()

        if current_time - self.last_idea_button_time < 5:
            return
        
        self.last_idea_button_time = current_time

        self.score_popups.append(ScorePopup(int(self.game.width - self.game.width * 0.035), 
                                            int(self.game.height / 2 - self.game.width // 20), 
                                            "-100", 
                                            (255,0,0)))

        self.current_combo = 1
        self.score -= 100

        for card in self.cards:
            if card.is_highlighted:
                return
        
        pairs = self.get_removable_pairs()

        if len(pairs) > 0:
            pair = random.choice(pairs)
            pair[0].is_highlighted = True
            pair[1].is_highlighted = True

    
    def auto_solver_button_action(self, button):

        self.auto_solving = not self.auto_solving
        

    
    def auto_solver(self):

        if not self.auto_solving:
            return
        
        if len(self.current_removables) == 0:
            self.current_removables = self.get_removable_pairs()


        if len(self.current_removables) == 0:
            self.auto_solving = False
            return


        if self.auto_solving_deleting:
            self.remove_cards()
            self.auto_solving_deleting = False
        else:

            pair = self.current_removables.pop(0)

            self.selected_cards = [pair[0], pair[1]]

            pair[0].is_selected = True
            pair[1].is_selected = True

            self.auto_solving_deleting = True


                
    def get_removable_pairs(self):
        
        removable_pairs = []
        self.removables_cards = 0

        for c1 in self.cards:
            if not c1.is_removable():
                continue
            self.removables_cards += 1
            for c2 in self.cards:
                if c1 == c2:
                    continue
                if not c2.is_removable():
                    continue
                if c1.c_type == c2.c_type:
                    
                    if removable_pairs.__contains__((c2, c1)):
                        continue

                    removable_pairs.append((c1, c2))
        
        return removable_pairs


    def update(self):

        if self.current_animation:

            current_time = time.time()

            if current_time - self.last_shuffle_animation_time > 0.1:
                self.shuffle_board()
            

        board_helper.update_current_card(self)

        for button in self.buttons:
            button.update()

        self.particle_effects = [p for p in self.particle_effects if p.update()]
        self.score_popups = [s for s in self.score_popups if s.update()]

        current_time = time.time()

        if current_time - self.last_score_update_time >= 1:
            self.timer += 1
            self.last_score_update_time = current_time


        if not self.current_animation:
            if current_time - self.last_solver_used_time >= 0.1:
                self.auto_solver()
                self.last_solver_used_time = time.time()

        if self.ending:

            if len(self.particle_effects) == 0 and len(self.score_popups) == 0:
                self.ending = False
                self.game.switch_to_end()
                


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
        #score_text = self.font.render(f"FPS: {self.game.clock.get_fps()}", True, (255, 255, 255))

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

                        self.remove_cards()

                    else:
                        self.selected_cards.pop(0).is_selected = False


    def remove_cards(self):
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

        if self.auto_solving:
            score_gain = 0

        if actual_time - self.last_removed_time < 3:
            self.current_combo += 1
            score_gain *= self.current_combo
        else:
            self.current_combo = 1

        self.score += 2 * score_gain

        self.score_popups.append(ScorePopup(x1, y1, f"+{score_gain}", (255, 255, 0)))
        self.score_popups.append(ScorePopup(x2, y2, f"+{score_gain}", (255, 255, 0)))

        self.last_removed_time = actual_time

        self.current_removables = self.get_removable_pairs()

        if len(self.cards) == 0:
            self.ending = True
            return

        if len(self.current_removables) == 0:
                        
            self.shuffle_board()
            self.current_animation = True
        


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

        positions = []
        cards_types = []

        for level in range(len(self.grid)):

            for i in range(len(self.grid[level])):

                for j in range(len(self.grid[level][i]) - 1, -1, -1):

                    if self.grid[level][i][j] == 0:
                        continue

                    if self.grid[level][i][j] == -1:
                        positions.append((level, i, j))
                        continue
                    
                   
                    self.cards.append(Card(self, self.grid[level][i][j], level, j, i))
        

        if len(positions) == 0:
            return

        for i in range(len(positions) // 2):

            card_type = random.randint(1, 38)
            cards_types.append(card_type)
            cards_types.append(card_type)
        
        random.shuffle(cards_types)

        for i in range(len(positions)):

            position = positions[i]

            self.grid[position[0]][position[1]][position[2]] = cards_types[i]

            self.cards.append(Card(self, cards_types[i], position[0], position[2], position[1]))
        
        board_helper.sort_cards(self)



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

        self.last_shuffle_animation_time = time.time()

        removable_pairs = self.get_removable_pairs()

        if self.removables_cards <= 1:
            self.current_animation = False
            self.ending = True

        # On relance un shuffle
        if len(removable_pairs) == 0 and len(self.cards) > 0:
            self.shuffle_board()
            self.current_animation = True