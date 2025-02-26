import pygame
from matplotlib.path import Path

class Card:

    def __init__(self, board, c_type, level, cell_x, cell_y):
        
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

        self.is_selected = False

        self.is_top_level = self.level == len(self.board.grid) - 1

        self.coord_x = self.board.width_start + self.cell_x * self.board.card_width + self.level * self.offset
        self.coord_y = self.board.height_start + self.cell_y * self.board.card_height - self.level * self.offset

        if self.is_top_level:
            self.coord_x += self.board.card_width / 2
            self.coord_y += self.board.card_height / 2
        
        self.points = [ (self.coord_x - self.offset, self.coord_y + self.offset),
                    (self.coord_x, self.coord_y),
                    (self.coord_x, self.coord_y + self.board.card_height), 
                    (self.coord_x + self.board.card_width, self.coord_y + self.board.card_height), 
                    (self.coord_x + self.board.card_width - self.offset, self.coord_y + self.board.card_height + self.offset), 
                    (self.coord_x - self.offset, self.coord_y + self.board.card_height + self.offset) ]
        
        self.polygon_path = Path(self.points)
    

    def update(self):

        if self.is_expired:
            return
        
        mouse_x, mouse_y = pygame.mouse.get_pos()

        self.inside_card = self.coord_x <= mouse_x <= self.coord_x + self.board.card_width and self.coord_y <= mouse_y <= self.coord_y + self.board.card_height

        self.inside_card_side = self.polygon_path.contains_point((mouse_x, mouse_y))

        self.is_hovered = self.inside_card or self.inside_card_side


    def draw(self):

        if self.is_expired: 
            return

        #shadow_color = (219, 219, 219)
        shadow_color = (175, 138, 106)
        
        screen = self.board.game.screen


        card_rect = pygame.Rect(self.coord_x, self.coord_y, self.board.card_width, self.board.card_height)

        
        if not self.is_selected:
            pygame.draw.polygon(screen, (235, 153, 14) if self.is_hovered else shadow_color, self.points, width=0)
        else:
            pygame.draw.polygon(screen, (40, 96, 19), self.points, width=0)


        if not self.is_selected:
            if self.is_hovered:
                self.draw_gradient_horizontal((255, 242, 150), (235, 153, 14), card_rect)
            else:
                self.draw_gradient_horizontal((253, 223, 188), (175, 138, 106), card_rect)
        else:
            self.draw_gradient_horizontal((113, 210, 89), (40, 96, 19), card_rect)

        self.board.game.screen.blit(self.board.game.images.cards[self.c_type - 1], (self.coord_x, self.coord_y))

        pygame.draw.line(screen, "black", card_rect.topleft, card_rect.topright, width = 1)
        pygame.draw.line(screen, "black", card_rect.topright, card_rect.bottomright, width = 1)


        pygame.draw.line(screen, "black", self.points[0], self.points[1], width = 1)
        pygame.draw.line(screen, "black", self.points[3], self.points[4], width = 1)
        pygame.draw.line(screen, "black", self.points[4], self.points[5], width = 1)
        pygame.draw.line(screen, "black", self.points[5], self.points[0], width = 1)
    
    
    
    def delete(self):
        self.is_expired = True
        self.board.cards.remove(self)
        self.board.grid[self.level][self.cell_y][self.cell_x] = 0



    def draw_gradient_horizontal(self, color1, color2, rect):
        x, y, width, height = rect
        for i in range(height):
            r = color2[0] + (color1[0] - color2[0]) * i // height
            g = color2[1] + (color1[1] - color2[1]) * i // height
            b = color2[2] + (color1[2] - color2[2]) * i // height
            pygame.draw.line(self.board.game.screen, (r, g, b), (x, y + height - i), (x + width, y + height - i))



    def is_removable(self):
        
        side_removable = False

        if self.cell_x == 0:
            side_removable = True
        elif self.cell_x == (self.board.n_cells_X - 2 if self.is_top_level else self.board.n_cells_X - 1):
            side_removable = True
        elif self.board.grid[self.level][self.cell_y][self.cell_x - 1] == 0:
            side_removable = True
        elif self.board.grid[self.level][self.cell_y][self.cell_x + 1] == 0:
            side_removable = True
            
        top_removable = True

        if self.is_top_level:
            pass
        
        elif self.level == len(self.board.grid) - 2:

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
            
        else:
            
            for level in range(self.level + 1, len(self.board.grid) - 1):

                if self.board.grid[level][self.cell_y][self.cell_x] != 0:
                    top_removable = False

        
        return top_removable and side_removable

    
    