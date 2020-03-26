#!/bin/env python3
from configparser import ConfigParser
import getopt, sys
import cProfile
import copy

folded = 0

def score(protein):
    cardinals = cardinalize(protein)
    h_protein, h_cardinals = destroy_polar_aminoacids(protein)
    score = 0
    for cardinal in h_cardinals:
        all_neighbors = neighbors(cardinal[0], cardinal[1])
        for neighbor in all_neighbors:
            if neighbor in h_cardinals:
                score += 1
    return score/2

def neighbors(x,y):
    return (x+1,y),(x-1,y),(x,y+1),(x,y-1)

def destroy_polar_aminoacids(current_protein):
    current_cardinals = cardinalize(current_protein)
    new_cardinals = []
    new_protein =  []
    for i, aminoacid in enumerate(current_protein):
        if aminoacid[0] == 'H':
            new_protein.append((copy.copy(aminoacid)))
            new_cardinals.append(copy.copy(current_cardinals[i]))
    return new_protein, new_cardinals
        
            
def parse_protein(protein_string):
    protein_struct = []
    protein_struct.append(['X','X'])
    for i in range(len(protein_string)-1):
        protein_struct.append([protein_string[i],''])
    protein_struct.append([protein_string[i+1],'X'])
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
    seen = set()
    for i in cardinals:
        if i in seen:
            return True
        seen.add(i)
    return False


def is_protein_valid(protein):
    #permutation = ""
    #for i in range(1,len(protein)-1):
    #    permutation += protein[i][1]
    #    #print(protein[i])
    #print(permutation)
        
    cardinals = cardinalize(protein)[1:]
    return not is_cardinal_repeated(cardinals)


def fold_rec(protein, depth, length, hide, max_folds):
    orients = ['N','S','E','W']
    global folded
    if max_folds != 0 and folded >= max_folds:
        return 0,[]
    if depth == length-1:
        if is_protein_valid(protein):
            if hide == False:
                draw_protein(protein)
            folded += 1
            return score(protein), copy.deepcopy(protein)
        return 0,[]
    best_score = -1
    best_protein = None
    for symbol in orients:
        protein[depth][1] = symbol 
        new_fold =  fold_rec(protein,depth+1,\
                length,hide,max_folds)
        if new_fold[0] > best_score:
            best_score = new_fold[0]
            best_protein = new_fold[1] 

    return best_score, best_protein

def fold(protein, max_folds, hide):
    best_fold = fold_rec(protein, 1, len(protein), hide, max_folds)
    return best_fold 

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



def parse_arguments():
    argument_list = sys.argv[1:]
    short_options = "hbf:p:n"
    long_options = ["help","bench","max_folds=",\
            "protein="]
    help_text = "You asked for help?"
    bench = False
    max_folds = 0
    protein_string = ""
    hide = False
    try:
        arguments, value = getopt.getopt(argument_list, short_options,\
                                         long_options)
    except getopt.error as err:
        print(help_text)
        sys.exit(1)
    for current_arg, current_val in arguments:
        if current_arg in ("-h","--help"):
            print(help_text)
            sys.exit(1)
        if current_arg in ("-b","--bench"):
            bench = True
        if current_arg in ("-f","-max_folds"):
            max_folds = int(current_val[1:])
        if current_arg in ("-p","--protein"):
            protein_string = current_val[1:]
        if current_arg in ("-n","--not_show"):
            hide = True
    return bench, hide, max_folds, protein_string

def handle_parameters():
    bench, hide, max_folds, protein_string = parse_arguments()
    max_folds_conf, seed,  protein_string_conf = read_config_file("params.conf") 
    if max_folds == 0:
        max_folds = max_folds_conf
    if protein_string == "":
        protein_string = protein_string_conf
    if len(protein_string) < 2:
        print("Protein must have at least 2 aminoacids")
        sys.exit(-1)
    protein = parse_protein(protein_string)
    return bench, hide, seed, max_folds, protein
    
def read_config_file(file_path):
    config_object = ConfigParser()
    config_object.read(file_path)
    program_params = config_object["PROGRAM_PARAMS"]
    max_folds = program_params["max_folds"]
    seed = program_params["seed"]
    protein = config_object["PROTEIN"]
    protein_string = protein["string"]
    return int(max_folds), seed, protein_string

def profile(hide):
    max_folds = 30000
    protein_string_complex = "HPHPHHPHPHHPPHHPHPH"
    protein_string_simple = "HPHPHH"
    
    protein = parse_protein(protein_string_complex)
    fold(protein, max_folds, hide)

def main():
    bench, hide, seed, max_folds, protein = handle_parameters()
    if bench == True:
        if hide:
            cProfile.run("profile( True )")
        else:
            cProfile.run("profile( False )")
        sys.exit(0)

    best_fold = fold(protein, max_folds, hide)
    protein = best_fold[1]
    score = best_fold[0]
    draw_protein(protein)
    print("Score",score)


if __name__=="__main__":
    main()



