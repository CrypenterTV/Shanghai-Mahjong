import pygame

class Images:

    def __init__(self, folder):

        self.folder = folder
        self.cards = []

        self.load_cards()
    
    def load_cards(self):

        for i in range(1, 39):

            self.cards.append(pygame.image.load(self.folder + f"card{i}.png"))

    def resize_cards(self, width, height):

        for i in range(len(self.cards)):

            self.cards[i] = pygame.transform.scale(self.cards[i], (int(width), int(height)))
            


    
    