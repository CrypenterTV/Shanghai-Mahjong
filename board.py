import os
import pygame
from card import Card

class Board:

    def __init__(self, game, filename):

        self.game = game
        self.filename = filename
        self.grid = []
        self.cards = []
        self.n_cells_X = 0
        self.n_cells_Y = 0

        self.width_start = 0.1 * game.width
        self.width_end = 0.9 * game.width
        self.height_start = 0.1 * game.height
        self.height_end = 0.9 * game.height 

        self.load_from_file()
        self.analyse_board()

        self.card_width = (self.width_end - self.width_start) / self.n_cells_X
        self.card_height = (self.height_end - self.height_start) / self.n_cells_Y

        self.load_game_elemtents()

        print(f"n_cells_X: {self.n_cells_X}, n_cells_Y: {self.n_cells_Y}")
        print(f"card_width: {self.card_width}, card_height: {self.card_height}")





    def update(self):
        pass

    
    def draw(self):

        for card in self.cards:
            card.draw()


    def analyse_board(self):

        assert len(self.grid) > 0 and len(self.grid[0]) > 0 and len(self.grid[0][0]) > 0

        self.n_cells_X = len(self.grid[0][0])
        self.n_cells_Y = len(self.grid[0])

        for i in range(len(self.grid)):

            current_2d = self.grid[i]

            x_to_check = self.n_cells_X
            y_to_check = self.n_cells_Y

            if i == len(self.grid) - 1:
                x_to_check -= 1
                y_to_check -= 1

            if len(current_2d) != y_to_check:
                raise Exception("La taille de la grille est incorrecte.")
            
            for line in current_2d:
                if len(line) != x_to_check:
                    raise Exception("La taille de la grille est incorrecte")
    

    def load_game_elemtents(self):


        for level in range(len(self.grid)):

            for i in range(len(self.grid[level])):

                for j in range(len(self.grid[level][i]) - 1, -1, -1):

                    if self.grid[level][i][j] == 0:
                        continue
                   
                    self.cards.append(Card(self, level, j, i))

    
    def load_from_file(self):

        self.grid = []

        if not os.path.isfile(self.filename):
            raise Exception(f"Le fichier du niveau {self.filename} est introuvable.")
        
        with open(self.filename, "r") as file:

            current_2d = []

            for line in file:

                line = line.strip()
                line = line.replace(" ", "")

                if line == "":

                    if len(current_2d) > 0:
                        self.grid.append(current_2d)
                        current_2d = []
                
                else:

                    current_line = []

                    for char in line:
                        
                        current_line.append(int(char))
                    
                    current_2d.append(current_line)

            if len(current_2d) > 0:
                self.grid.append(current_2d)



    def export_to_file(self, filename : str):

        with open(filename, "w+") as file:

            for i in range(len(self.grid)):

                current_2d = self.grid[i]

                for j in range(len(current_2d)):
                    
                    line = current_2d[j]

                    sb = ""
                    
                    for k in range(len(line)):

                        space = " "

                        if k == len(line) - 1:
                            space = ""

                        sb += str(line[k]) + space

                    return_char = "\n"

                    if i == len(self.grid) - 1 and j == len(current_2d) - 1:
                        return_char = ""

                    file.write(sb + return_char)

                if i == len(self.grid) - 1:
                    continue

                file.write("\n")