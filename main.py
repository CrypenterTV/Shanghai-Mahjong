import pygame
from enum import Enum
from images import Images
from sounds import Sounds
from main_menu import MainMenu
from pause_menu import PauseMenu
from end_menu import EndMenu


class GameState(Enum):
    MAIN_MENU = 1
    GAME = 2
    PAUSE_MENU = 3
    END_MENU = 4


class Game:

    def __init__(self):

        pygame.init()

        info = pygame.display.Info()

        self.width = int(0.8 * info.current_w)
        self.height = int(0.8 * info.current_h)
        #self.level_offset = 16;
        self.level_offset = 12
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.state = GameState.MAIN_MENU
        

        self.is_muted = False
        self.music_pos = 0

        pygame.mixer.music.load('assets/music/music.mp3')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

        pygame.display.set_caption("Shanghai Mahjong")

        self.images = Images(self, "assets/images/")
        self.sounds = Sounds(self, "assets/music/")

        self.clock = pygame.time.Clock()

        self.main_menu = MainMenu(self)
        self.board = None
        self.pause_menu = PauseMenu(self)
        self.end_menu = EndMenu(self)

        pygame.display.set_icon(self.images.icon)

        self.current_scene = self.main_menu



    def run(self):

        running = True

        while running:

            dt = self.clock.tick(180) / 1000

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.MOUSEBUTTONDOWN:

                    self.current_scene.update()
                    self.current_scene.handle_click()

                elif event.type == pygame.KEYDOWN:

                    self.current_scene.handle_keyboard(event.key)

            self.current_scene.update()
            self.current_scene.draw()

            pygame.display.flip()

            
        
        pygame.quit()

    
    def switch_to_game(self):
        self.state = GameState.GAME
        self.board.buttons[0].image = self.images.pause_icon
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        self.current_scene = self.board

    def switch_to_pause(self):
        self.state = GameState.PAUSE_MENU
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        self.current_scene = self.pause_menu
    
    def switch_to_main(self):
        self.state = GameState.MAIN_MENU
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        self.current_scene = self.main_menu
    
    def switch_to_end(self):
        self.board.update()
        self.board.draw()
        self.state = GameState.END_MENU
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        self.current_scene = self.end_menu


    def mute_button_action(self):
        if self.is_muted:
            pygame.mixer.music.play(-1, start=self.music_pos)
            self.is_muted = False
        else:
            self.music_pos = pygame.mixer.music.get_pos() / 1000
            pygame.mixer.music.pause()
            self.is_muted = True

            



if __name__ == "__main__":

    game = Game()
    game.run()