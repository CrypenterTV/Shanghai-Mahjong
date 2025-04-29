import os

def update_current_card(board):

    max_level_selected_card = None
    cards_to_unhover = []

    # On surligne uniquement la bonne carte parmi toutes les cartes en dessous du curseur
    for card in board.cards:
        
        card.update()

        if card.is_hovered:
                
            if max_level_selected_card == None:
                max_level_selected_card = card
            else:

                if max_level_selected_card.level < card.level: # On trouve une carte plus haute
                    cards_to_unhover.append(max_level_selected_card)
                    max_level_selected_card = card

                elif max_level_selected_card.level == card.level:

                    if max_level_selected_card.inside_card_side and card.inside_card: # Le curseur est au milieu de la carte (et pas sur les côtés)

                        cards_to_unhover.append(max_level_selected_card)
                        max_level_selected_card = card

                    else:
                        card.is_hovered = False

                else:
                    card.is_hovered = False
    
    # Retrait du surlignage pour les autres cartes
    for card in cards_to_unhover:
        card.is_hovered = False
        
    board.current_card = max_level_selected_card



def export_to_file(board, filename):

    # Export vers un fichier texte depuis l'état du board

    with open(filename, "w+") as file:

        for i in range(len(board.grid)):

            current_2d = board.grid[i]

            for j in range(len(current_2d)):
                    
                line = current_2d[j]

                sb = ""
                    
                for k in range(len(line)):

                    space = " "

                    if k == len(line) - 1:
                        space = ""

                    sb += str(line[k]) + space

                return_char = "\n"

                if i == len(board.grid) - 1 and j == len(current_2d) - 1:
                    return_char = ""

                file.write(sb + return_char)

            if i == len(board.grid) - 1:
                continue

            file.write("\n") # Retour à la ligne entre chaque étage du board



def load_from_file(board, filename):

    # Chargement d'un board depuis un fichier texte

    board.grid = []

    if not os.path.isfile(filename):
        raise Exception(f"Le fichier du niveau {filename} est introuvable.")
        
    with open(filename, "r") as file:

        current_2d = []

        for line in file:

            line = line.strip() # Retrait des espaces inutiles s'il y en a

            if line == "":

                if len(current_2d) > 0:
                    board.grid.append(current_2d)
                    current_2d = []
                
            else:

                line = line.split(" ")

                current_line = []

                for char in line:
                        
                    current_line.append(int(char))
                    
                current_2d.append(current_line)

        if len(current_2d) > 0:
            board.grid.append(current_2d)


def sort_cards(board):

    n = len(board.cards)

    # Tri par sélection des cartes du board selon plusieurs critères :
    #   de niveau en niveau, de gauche vers la droite et de haut en bas
    
    for i in range(1, n):

        key_card = board.cards[i]
        j = i - 1

        while j >= 0:
            swap = False

            # Tri des niveaux par ordre croissant
            if board.cards[j].level > key_card.level:
                swap = True

            elif board.cards[j].level == key_card.level:
                
                # Tri des coordonnées y par ordre croissant
                if board.cards[j].cell_y > key_card.cell_y:
                    swap = True

                # Tri des coordonnées x par odre décroissant
                elif board.cards[j].cell_y == key_card.cell_y:
                    if board.cards[j].cell_x < key_card.cell_x:
                        swap = True
            
            if swap:
                board.cards[j + 1] = board.cards[j]
                j -= 1
            else:
                break

        board.cards[j + 1] = key_card 