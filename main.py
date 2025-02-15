import pygame
from enum import Enum


class GameState(Enum):
    MAIN_MENU = 1
    GAME = 2
    PAUSE_MENU = 3
    END_MENU = 4


class Game:

    def __init__(self):

        pygame.init()

        self.width = 1000;
        self.height = 1000;
        
        self.screen = pygame.display.set_mode((self.width, self.height))

        self.state = GameState.MAIN_MENU

        pygame.display.set_caption("Shanghai Mahjong")

        self.clock = pygame.time.Clock()

    def run(self):

        while True:

            dt = self.clock.tick() / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            



if __name__ == "__main__":
    game = Game()
    game.run()

                    
        