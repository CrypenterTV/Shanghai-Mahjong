import pygame

class Button:

    def __init__(self, game, label, text_color, x, y, width, height, font, button_action):

        self.game = game
        self.text_color = text_color
        self.label = label
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = font
        self.button_action = button_action

        self.is_hovered = False

        self.top_left_corner_x = self.x - self.width // 2
        self.top_left_corner_y = self.y - self.height // 2

    

    def update(self):

        mouse_x, mouse_y = pygame.mouse.get_pos()

        self.is_hovered = (self.x - self.width / 2 <= mouse_x <= self.x + self.width / 2) and (self.y - self.height / 2 <= mouse_y <= self.y + self.height / 2)


    def draw(self):
        
        base_color = (100, 100, 100)
        hover_color = (150, 150, 150)

        pygame.draw.rect(self.game.screen, hover_color if self.is_hovered else base_color,
                         (self.top_left_corner_x, self.top_left_corner_y, self.width, self.height), border_radius=10)
        
        text_surface = self.font.render(self.label, True, self.text_color)
        text_rect = text_surface.get_rect(center=(self.x, self.y))
        self.game.screen.blit(text_surface, text_rect)

        # Chevrons de sélection
        if self.is_hovered:
            chevron_color = (234, 161, 14)
            chevron_size = self.height // 3  
            padding = self.width / 10

            left_chevron = [(self.top_left_corner_x - padding + chevron_size, self.y),
                            (self.top_left_corner_x - padding, self.y - chevron_size),
                            (self.top_left_corner_x - padding, self.y + chevron_size)]
            
            right_chevron = [(self.top_left_corner_x + self.width + padding - chevron_size, self.y),
                             (self.top_left_corner_x + self.width + padding, self.y - chevron_size),
                             (self.top_left_corner_x + self.width + padding, self.y + chevron_size)]
            
            pygame.draw.polygon(self.game.screen, chevron_color, left_chevron)
            pygame.draw.polygon(self.game.screen, chevron_color, right_chevron)
    

    def handle_click(self):
        self.button_action(self)