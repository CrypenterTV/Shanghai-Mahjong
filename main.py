import pygame
from enum import Enum
from images import Images
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

        pygame.display.set_caption("Shanghai Mahjong")

        self.images = Images(self, "assets/images/")

        self.clock = pygame.time.Clock()

        self.main_menu = MainMenu(self)
        self.board = None
        self.pause_menu = PauseMenu(self)
        self.end_menu = EndMenu(self)

        pygame.display.set_icon(self.images.icon)



    def run(self):

        running = True

        while running:

            dt = self.clock.tick(180) / 1000

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    
                    match self.state:
                        case GameState.MAIN_MENU:
                            self.main_menu.handle_click()
                        case GameState.GAME:
                            self.board.handle_click()
                        case GameState.PAUSE_MENU:
                            self.pause_menu.handle_click()
                        case GameState.END_MENU:
                            self.end_menu.handle_click()

                elif event.type == pygame.KEYDOWN:

                    match self.state:
                        case GameState.MAIN_MENU:
                            self.main_menu.handle_keyboard(event.key)
                        case GameState.GAME:
                            self.board.handle_keyboard(event.key)
                        case GameState.PAUSE_MENU:
                            self.pause_menu.handle_keyboard(event.key)
                        case GameState.END_MENU:
                            self.end_menu.handle_keyboard(event.key)


            match self.state:
                case GameState.MAIN_MENU:
                    self.main_menu.update()
                    self.main_menu.draw()
                case GameState.GAME:
                    self.board.update()
                    self.board.draw()
                case GameState.PAUSE_MENU:
                    self.pause_menu.update()
                    self.pause_menu.draw()
                case GameState.END_MENU:
                    self.end_menu.update()
                    self.end_menu.draw()

            pygame.display.flip()

            
        
        pygame.quit()

    
    def switch_to_game(self):
        self.state = GameState.GAME
        self.board.buttons[0].image = self.images.pause_icon
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def switch_to_pause(self):
        self.state = GameState.PAUSE_MENU
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    
    def switch_to_main(self):
        self.state = GameState.MAIN_MENU
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    
    def switch_to_end(self):
        self.board.update()
        self.board.draw()
        self.state = GameState.END_MENU
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            



if __name__ == "__main__":

    game = Game()
    game.run()