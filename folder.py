#!/bin/env python3
from configparser import ConfigParser
import copy
import sys

folded = 0

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
    for i in range(len(protein_string)):
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


def fold_rec(protein, depth, length, p=0, fold_max=0):
    orients = ['N','S','E','W']
    proteins =  []
    global folded
    if fold_max != 0 and folded >= fold_max:
        return proteins
    if depth == length-1:
        if is_protein_valid(protein):
            if p == 1:
                draw_protein(protein)
            folded += 1
            proteins.append(protein)
        return proteins
    for symbol in orients:
        new_prot = copy.deepcopy(protein)
        new_prot[depth][1] = symbol 
        new_folds =  fold_rec(new_prot,depth+1,length,p,fold_max)
        for prot in new_folds:
            proteins.append(prot)
    return proteins

def fold_along(protein, fold_max=0):
    fold_rec(protein, 1, len(protein), 1,fold_max)

def fold(protein, fold_max = 0):
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

def create_base_grid(cardinals, length):
    grid = []
    for i in range(length):
        row = []
        for j in range(length):
            row.append(" ")
        grid.append(row)
    return grid

def card_offset_f_orientation(orientation):
    if orientation == 'N':
        offset = (0,1)
        padding_char = '|'
    elif orientation == 'S':
        offset = (0,-1)
        padding_char = '|'
    elif orientation == 'E':
        offset = (1,0)
        padding_char = '-'
    else:
        offset = (-1,0)
        padding_char = '-'
    return offset, padding_char

def insert_protein_in_grid(grid, protein, cardinals):
    for i in range(1, len(protein)):
        bond_orientation = protein[i][1]
        x = cardinals[i][0]*2
        y = cardinals[i][1]*2
        grid[y][x] = protein[i][0]
        if bond_orientation != 'X':
            offset, padding_char =\
                    card_offset_f_orientation(bond_orientation)
            grid[y+offset[1]][x+offset[0]] = padding_char
    return grid

def draw_protein(protein):
    cardinals = cardinalize(protein)
    normalized_card = normalize_cardinals(cardinals)
    grid = create_base_grid(normalized_card, len(protein)*2)
    grid = insert_protein_in_grid(grid, protein, normalized_card)
    print_grid(grid)

def get_initial_protein():
    steps, seed, protein_string = \
            read_config_file_configparser("params.conf")
    return parse_protein(protein_string)

def main_fold_x_times():
    times = 10
    if len(sys.argv) == 2:
        times = int(sys.argv[1])

    protein_struct = get_initial_protein() 
    proteins = fold_along(protein_struct,times)
    
def main():
    protein_struct = get_initial_protein() 
    print_protein(protein_struct)
    proteins = fold(protein_struct)
    for i in range(len(proteins)):
        draw_protein(proteins[i])


if __name__=="__main__":
    #main()
    main_fold_x_times()


