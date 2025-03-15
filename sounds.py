import pygame

class Sounds:

    def __init__(self, game, folder):

        self.folder = folder

        self.click_sound = pygame.mixer.Sound(folder + "break_sound.mp3")
        self.click_sound.set_volume(1)
    


