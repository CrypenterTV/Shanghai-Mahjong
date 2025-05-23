import pygame

class RoundButton:

    def __init__(self, game, x, y, radius, image, button_action):

        self.game = game
        self.x = x
        self.y = y
        self.radius = radius
        self.image = image
        self.button_action = button_action

        self.is_hovered = False

    
    def update(self):

        mouse_x, mouse_y = pygame.mouse.get_pos()
        # On vérifie que la souris soit dans le bouton
        distance = (mouse_x - self.x) ** 2 + (mouse_y - self.y) ** 2
        next_hover = distance <= self.radius ** 2

        if not self.is_hovered and next_hover:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        elif self.is_hovered and not next_hover:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        self.is_hovered = next_hover
    

    def draw(self):

        base_color = (100, 100, 100)
        hover_color = (150, 150, 150)
        border_color = (255, 255, 255) 

        pygame.draw.circle(self.game.screen, hover_color if self.is_hovered else base_color,
                           (self.x, self.y), self.radius)
        
        if self.is_hovered:
            pygame.draw.circle(self.game.screen, border_color,
                               (self.x, self.y), self.radius, 5)


        image_rect = self.image.get_rect(center=(self.x, self.y))
        self.game.screen.blit(self.image, image_rect)


    def handle_click(self):
        self.button_action(self)