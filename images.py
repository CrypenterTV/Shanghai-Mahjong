import pygame

class Images:

    def __init__(self, game, folder):

        self.folder = folder
        self.cards = []
        self.play_mat_background = pygame.image.load(self.folder + "tapis.jpg").convert_alpha()
        self.game_background = pygame.transform.scale(pygame.image.load(self.folder + "background.jpg").convert_alpha(), (game.width, game.height))
        self.icon = pygame.image.load(self.folder + "icon.png").convert_alpha()
        self.main_title = pygame.image.load(self.folder + "main_title.png").convert_alpha()

        self.pause_icon = pygame.image.load(self.folder + "pause.png").convert_alpha()
        self.resume_icon = pygame.image.load(self.folder + "resume.png").convert_alpha()
        self.shuffle_icon = pygame.image.load(self.folder + "shuffle_icon.png").convert_alpha()

        self.sound_on_icon = pygame.image.load(self.folder + "sound_on.png").convert_alpha()
        self.sound_off_icon = pygame.image.load(self.folder + "sound_off.png").convert_alpha()

        self.idea_icon = pygame.image.load(self.folder + "idea.png").convert_alpha()
    
        self.load_cards()
    
    def load_cards(self):
        
        for i in range(1, 39):

            self.cards.append(pygame.image.load(self.folder + f"card{i}.png").convert_alpha())
    

    def resize_cards(self, width, height):

        for i in range(len(self.cards)):

            self.cards[i] = pygame.transform.scale(self.cards[i], (int(width), int(height)))

    def resize_play_mat_bg(self, width, height):
        self.play_mat_background = pygame.transform.scale(self.play_mat_background, (int(width), int(height)))

    def resize_main_title(self, width, height):
        self.main_title = pygame.transform.scale(self.main_title, (int(width), int(height)))

    def resize_pause_icon(self, width, height):
        self.pause_icon = pygame.transform.scale(self.pause_icon, (int(width), int(height)))
            
    def resize_resume_icon(self, width, height):
        self.resume_icon = pygame.transform.scale(self.resume_icon, (int(width), int(height)))

    def resize_shuffle_icon(self, width, height):
        self.shuffle_icon = pygame.transform.scale(self.shuffle_icon, (int(width), int(height)))
    
    def resize_sound_on_icon(self, width, height):
        self.sound_on_icon = pygame.transform.scale(self.sound_on_icon, (int(width), int(height)))

    def resize_sound_off_icon(self, width, height):
        self.sound_off_icon = pygame.transform.scale(self.sound_off_icon, (int(width), int(height)))

    def resize_idea_icon(self, width, height):
        self.idea_icon = pygame.transform.scale(self.idea_icon, (int(width), int(height)))   