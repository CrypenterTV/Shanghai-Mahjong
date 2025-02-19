import pygame
from enum import Enum
from board import Board

class GameState(Enum):
    MAIN_MENU = 1
    GAME = 2
    PAUSE_MENU = 3
    END_MENU = 4


class Game:

    def __init__(self):

        pygame.init()

        info = pygame.display.Info()

        self.width = 0.7 * info.current_w;
        self.height = 0.7 * info.current_h;
        self.level_offset = 15;
        
        self.screen = pygame.display.set_mode((self.width, self.height))

        self.state = GameState.MAIN_MENU

        pygame.display.set_caption("Shanghai Mahjong")

        self.clock = pygame.time.Clock()

        self.board = Board(self, "levels/level1.txt")



    def run(self):

        running = True

        while running:

            dt = self.clock.tick() / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill((75, 89, 216))

            self.board.draw()

            pygame.display.flip()
        
        pygame.quit()
            



if __name__ == "__main__":

    game = Game()
    game.run()