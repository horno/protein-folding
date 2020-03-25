#!/bin/env python3
from configparser import ConfigParser


def read_config_file_configparser(file_path):
    config_object = ConfigParser()
    config_object.read(file_path)
    program_params = config_object["PROGRAM_PARAMS"]
    steps = program_params["steps"]
    seed = program_params["seed"]
    protein = config_object["PROTEIN"]
    protein_string = protein["string"]
    return steps, seed, protein_string

def score(protein_string):
   # score = 0
   # for aminoacid in protein_string:
   #     if aminoacid[0] == 'H':
   #         neighbor_1 = protein_string[aminoacid[1]][0]
   #         neighbor_2 = protein_string[aminoacid[2]][0]
   #         if neighbor_1 == "H":
   #             score += 1
   #         if neighbor_2 == "H":
   #             score += 1
   # return score
   pass
            
def parse_protein(protein_string):
    protein_struct = []
    protein_struct.append(['X','X'])
    for i in range(1,len(protein_string)):
        protein_struct.append([protein_string[i],''])
    protein_struct.append([protein_string[i],'X'])
    return protein_struct

def cardinalize(protein):
    cardinals = []
    cardinals.append((0,0))
    cardinals.append((0,0))
    for i in range(2, len(protein)):
        orientation = protein[i-1][1]
        if orientation == 'N':
            new_cards = (cardinals[i-1][0],cardinals[i-1][1]+1)
        elif orientation == 'S':
            new_cards = (cardinals[i-1][0],cardinals[i-1][1]-1)
        elif orientation == 'E':
            new_cards = (cardinals[i-1][0]+1,cardinals[i-1][1])
        else:
            new_cards = (cardinals[i-1][0]-1,cardinals[i-1][1])
        cardinals.append(new_cards)
    return cardinals

def is_cardinal_repeated(cardinals):
    for cardinal_1 in cardinals:
        add = 0
        for cardinal_2 in cardinals:
            if cardinal_1 == cardinal_2:
                add += 1
            if add > 1:
                return True
    return False

def is_protein_valid(protein):
    cardinals = cardinalize(protein)[1:]
    return not is_cardinal_repeated(cardinals)


def fold_rec(protein, depth, length):
    orients = ['N','S','E','W']
    proteins =  []
    if depth == length-1:
        if is_protein_valid(protein):
            proteins.append(protein)
        return proteins
    for symbol in orients:
        protein[depth][1] = symbol 
        new_folds =  fold_rec(protein, depth + 1, length)
        for prot in new_folds:
            proteins.append(prot)
    return proteins


def fold(protein):
    proteins = fold_rec(protein, 1, len(protein))
    return proteins


def print_protein(protein):
    for i, aminoacid in enumerate(protein):
        print(i, aminoacid)
    print()

def normalize_cardinals(cardinals):
    minimum_1 = len(cardinals)*2
    minimum_2 = len(cardinals)*2
    for cardinal in cardinals:
        if cardinal[0] < minimum_1:
            minimum_1 = cardinal[0]
        if cardinal[1] < minimum_2:
            minimum_2 = cardinal[1]

    if minimum_1 < 0 and minimum_2 < 0:
        for i in range(len(cardinals)):
            new_card = (cardinals[i][0]+minimum_1*-1, 
                        cardinals[i][1]+minimum_2*-1)
            cardinals[i] = new_card
    elif minimum_1 < 0:
        for i in range(len(cardinals)):
            new_card = (cardinals[i][0]+minimum_1*-1, 
                        cardinals[i][1])
            cardinals[i] = new_card
    elif minimum_2 < 0:
        for i in range(len(cardinals)):
            new_card = (cardinals[i][0], 
                        cardinals[i][1]+minimum_2*-1)
            cardinals[i] = new_card
    return cardinals

def print_grid(grid):
    for row in grid:
        for col in row:
            print(col, end="")
        print()

def draw_protein(protein):
    grid = []
    cardinals = cardinalize(protein)[1:]
    normalized_card = normalize_cardinals(cardinals)
    for i in range(len(protein)*2):
        row = []
        for j in range(len(protein)*2):
            row.append("X ")
        grid.append(row)

    print_grid(grid)
    
def main():
    steps, seed, protein_string = \
            read_config_file_configparser("params.conf")
    print("Input:")
    print(steps, seed, protein_string)
    protein_struct = parse_protein(protein_string)
    print_protein(protein_struct)
    proteins = fold(protein_struct)
    draw_protein(proteins[0])


if __name__=="__main__":
    main()

