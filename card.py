import pygame
from matplotlib.path import Path

class Card:

    def __init__(self, board, c_type, level, cell_x, cell_y, fake_card=False):
        
        self.is_expired = False

        self.board = board
        self.c_type = c_type
        self.level = level
        self.cell_x = cell_x
        self.cell_y = cell_y
        self.offset = self.board.game.level_offset
        
        self.points = []

        self.is_hovered = False
        self.inside_card = False
        self.inside_card_side = False

        self.is_highlighted = False

        self.is_selected = False

        self.fake_card = fake_card

        self.is_top_level = self.level == len(self.board.grid) - 1

        self.coord_x = self.board.width_start + self.cell_x * self.board.card_width + self.level * self.offset
        self.coord_y = self.board.height_start + self.cell_y * self.board.card_height - self.level * self.offset

        if self.is_top_level:
            self.coord_x += self.board.card_width / 2
            self.coord_y += self.board.card_height / 2
        
        # Polygone des contours de la carte (le relief)
        self.points = [ (self.coord_x - self.offset, self.coord_y + self.offset),
                    (self.coord_x, self.coord_y),
                    (self.coord_x, self.coord_y + self.board.card_height), 
                    (self.coord_x + self.board.card_width, self.coord_y + self.board.card_height), 
                    (self.coord_x + self.board.card_width - self.offset, self.coord_y + self.board.card_height + self.offset), 
                    (self.coord_x - self.offset, self.coord_y + self.board.card_height + self.offset) ]
        
        self.polygon_path = Path(self.points)

        self.card_rect = pygame.Rect(self.coord_x, self.coord_y, self.board.card_width, self.board.card_height)

        self.should_be_drawn = True

        self.gradient_cache = {}

    

    def update(self):

        if self.is_expired:
            return
        
        mouse_x, mouse_y = pygame.mouse.get_pos()

        self.inside_card = self.coord_x <= mouse_x <= self.coord_x + self.board.card_width and self.coord_y <= mouse_y <= self.coord_y + self.board.card_height # Si le curseur est au milieu de la carte

        self.inside_card_side = self.polygon_path.contains_point((mouse_x, mouse_y)) # Si le curseur est sur les contours

        self.is_hovered = self.inside_card or self.inside_card_side


    def draw(self):

        if self.is_expired: 
            return

        shadow_color = (175, 138, 106)
        
        screen = self.board.game.screen

        # On dessine la bonne couleur des contours en fonction des critères
        if not self.is_selected:

            if not self.is_removable() and not self.fake_card:
                pygame.draw.polygon(screen, shadow_color, self.points, width=0)
            else:
                if self.is_hovered:
                    pygame.draw.polygon(screen, (235, 153, 14), self.points, width=0)
                else:
                    if self.is_highlighted:
                        pygame.draw.polygon(screen, (86, 63, 112), self.points, width=0)
                    else:
                        pygame.draw.polygon(screen, shadow_color, self.points, width=0)
        else:
            pygame.draw.polygon(screen, (40, 96, 19), self.points, width=0)

        
        # On dessine la bonne couleur de carte en fonction des critères
        if not self.is_selected:
            if (self.is_hovered and self.is_removable()) or (self.is_hovered and self.fake_card):
                self.draw_gradient_horizontal((255, 242, 150), (235, 153, 14), self.card_rect)
            else:
                if self.is_highlighted:
                    self.draw_gradient_horizontal((220, 186, 248), (86, 63, 112), self.card_rect)
                else:
                    self.draw_gradient_horizontal((253, 223, 188), (175, 138, 106), self.card_rect)
        else:
            self.draw_gradient_horizontal((113, 210, 89), (40, 96, 19), self.card_rect)

        if not self.fake_card:
            self.board.game.screen.blit(self.board.game.images.cards[self.c_type - 1], (self.coord_x, self.coord_y))

        # Lignes noires des contours
        pygame.draw.line(screen, "black", self.card_rect.topleft, self.card_rect.topright, width = 1)
        pygame.draw.line(screen, "black", self.card_rect.topright, self.card_rect.bottomright, width = 1)

        pygame.draw.line(screen, "black", self.points[0], self.points[1], width = 1)
        pygame.draw.line(screen, "black", self.points[3], self.points[4], width = 1)
        pygame.draw.line(screen, "black", self.points[4], self.points[5], width = 1)
        pygame.draw.line(screen, "black", self.points[5], self.points[0], width = 1)
    
    
    
    def delete(self):
        # Suppression de la carte
        self.is_expired = True
        self.board.cards.remove(self)
        self.board.grid[self.level][self.cell_y][self.cell_x] = 0


    def draw_gradient_horizontal(self, color2, color1, rect):
        
        x, y, width, height = rect

        # On construit une clé unique pour identifier ce dégradé dans le cache :
        # elle dépend des deux couleurs et des dimensions du rectangle
        key = (color1, color2, width, height)

        if key not in self.gradient_cache: # Si le dégradé correspondant n'a pas encore généré

            gradient_surface = pygame.Surface((width, height + 1))
            pixels = pygame.surfarray.pixels3d(gradient_surface)

            for i in range(height + 1):

                ratio = i / height

                # Interpolation linéaire de la couleur : du haut (color1) vers le bas (color2)
                r = int(color2[0] + (color1[0] - color2[0]) * ratio)
                g = int(color2[1] + (color1[1] - color2[1]) * ratio)
                b = int(color2[2] + (color1[2] - color2[2]) * ratio)

                pixels[:, i] = [r, g, b]

            del pixels
            gradient_surface = gradient_surface.convert()

            # On stocke le résultat pour ne pas avoir à recalculer à chaque appel
            self.gradient_cache[key] = gradient_surface

        self.board.game.screen.blit(self.gradient_cache[key], (x, y))



    def is_removable(self):
        
        side_removable = False

        if self.cell_x == 0: # Si la carte est toute à gauche
            side_removable = True
        elif self.cell_x == (self.board.n_cells_X - 2 if self.is_top_level else self.board.n_cells_X - 1): # Si la carte est toute à droite
            side_removable = True
        elif self.board.grid[self.level][self.cell_y][self.cell_x - 1] == 0: # S'il n'y a pas de carte à gauche
            side_removable = True
        elif self.board.grid[self.level][self.cell_y][self.cell_x + 1] == 0: # S'il n'y a pas de carte à gauche
            side_removable = True
            
        top_removable = True

        if self.is_top_level:
            pass
        
        else:

            for card in self.board.cards:

                if not card.is_top_level:
                    continue
                    
                if self.cell_x == card.cell_x and self.cell_y == card.cell_y:
                    top_removable = False
                elif self.cell_x == card.cell_x + 1 and self.cell_y == card.cell_y:
                    top_removable = False
                elif self.cell_x == card.cell_x and self.cell_y == card.cell_y + 1:
                    top_removable = False
                elif self.cell_x == card.cell_x + 1 and self.cell_y == card.cell_y + 1:
                    top_removable = False
                
                if not top_removable:
                    break
            
            if self.level < len(self.board.grid) - 2:

                for level in range(self.level + 1, len(self.board.grid) - 1):

                    if self.board.grid[level][self.cell_y][self.cell_x] != 0:
                        top_removable = False
        
        return top_removable and side_removable