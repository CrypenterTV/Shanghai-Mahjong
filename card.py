import pygame

class Card:

    def __init__(self, board, level, cell_x, cell_y):
        
        self.board = board
        self.level = level
        self.cell_x = cell_x
        self.cell_y = cell_y
        self.offset = self.board.game.level_offset

        self.is_top_level = self.level == len(board.grid) - 1

        self.coord_x = self.board.width_start + self.cell_x * self.board.card_width + self.level * self.offset
        self.coord_y = self.board.height_start + self.cell_y * self.board.card_height - self.level * self.offset

        if self.is_top_level:
            self.coord_x += self.board.card_width / 2
            self.coord_y += self.board.card_height / 2

    
    def update(self):
        pass


    def draw(self):
        shadow_color = (219, 219, 219)

        x = self.coord_x
        y = self.coord_y
        s_offset = self.offset
        card_height = self.board.card_height
        card_width = self.board.card_width
        screen = self.board.game.screen

        points = [  (x - s_offset, y + s_offset),
                    (x, y),
                    (x, y + card_height), 
                    (x + card_width, y + card_height), 
                    (x + card_width - s_offset, y + card_height + s_offset), 
                    (x - s_offset, y + card_height + s_offset)]
        
        pygame.draw.polygon(screen, shadow_color, points, width=0)


        card_rect = pygame.Rect(x, y, card_width, card_height)
        pygame.draw.rect(screen, "white", card_rect, width=0, border_radius=2);

        pygame.draw.line(screen, "black", card_rect.topleft, card_rect.topright, width = 1);
        pygame.draw.line(screen, "black", card_rect.topright, card_rect.bottomright, width = 1);


        pygame.draw.line(screen, "black", points[0], points[1], width = 1);
        pygame.draw.line(screen, "black", points[3], points[4], width = 1);
        pygame.draw.line(screen, "black", points[4], points[5], width = 1);
        pygame.draw.line(screen, "black", points[5], points[0], width = 1);