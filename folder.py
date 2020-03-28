#!/bin/env python3
from configparser import ConfigParser
import getopt, sys
import cProfile
import copy

orients = ['N','S','E','W']
folded = 0

def score(protein):
    seen = set()
    score = 0
    for i in range(1, len(protein)):
        amino = protein[i]
        cardinal = (amino[2][0], amino[2][1])
        if amino[0] == "H":
            x = cardinal[0]
            y = cardinal[1]
            all_neighbors = [(x+1,y), (x-1,y), (x,y+1), (x,y-1)]
            for neighbor in all_neighbors:
                if neighbor in seen:
                    score += 1
            seen.add(cardinal)
    return score

def parse_protein(protein_string):
    protein_struct = []
    protein_struct.append(['X','X',['x','x']])
    protein_struct.append([protein_string[0],'',[0,0]])
    for i in range(1,len(protein_string)-1):
        protein_struct.append([protein_string[i],'',['x','x']])
    protein_struct.append([protein_string[i+1],'X',['x','x']])
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

def is_protein_valid(protein):
    seen = set()
    for i in range(1, len(protein)):
        x = protein[i][2][0]
        y = protein[i][2][1]
        cardinal = (x,y)
        if cardinal in seen:
            return False
        seen.add(cardinal)
    return True

def check_new_fold(new_fold, best_score, best_protein):
    if new_fold[0] > best_score:
        best_score = new_fold[0]
        best_protein = new_fold[1]
    return best_score, best_protein

def complete_protein(protein, hide, best_score):
    global folded
    if is_protein_valid(protein):
        if hide == 0:
            draw_protein(protein)
        folded += 1
        current_score = score(protein)
        if current_score > best_score:
            if hide == 1:
                draw_protein(protein)
                print("Score:",str(current_score)+"\n")
            return current_score, copy.deepcopy(protein)
    return 0,[]

def oposite(orientation):
    if orientation == "N":
        return "S"
    if orientation == "S":
        return "N"
    if orientation == "E":
        return "W"
    if orientation == "W":
        return "E"

def symbol_preprocess_check(protein, symbol, depth):
    symbol_oposite = oposite(symbol)
    if symbol_oposite  == protein[depth-1][1]:
        return False
    if depth > 3:
        a = protein[depth-1][1]
        b = protein[depth-2][1]
        c = protein[depth-3][1]
        if symbol_oposite == b and oposite(a) == c:
            return False

    return True

def partial_protein(protein, depth, length, hide, max_folds,\
                                                best_score, best_protein):
    global orients
    for symbol in orients: 
        if symbol_preprocess_check(protein, symbol, depth):
            protein[depth][1] = symbol
            offset = card_offset(symbol) # Improvement here
            protein[depth+1][2][0] = protein[depth][2][0]+offset[0]
            protein[depth+1][2][1] = protein[depth][2][1]+offset[1]
            if is_protein_valid(protein[:depth+1]):
                new_fold =  fold_rec(protein,depth+1,\
                        length,hide,max_folds, best_score)
                best_score, best_protein =  check_new_fold(new_fold,best_score,\
                                                           best_protein)
    return best_score, best_protein
    
def fold_rec(protein, depth, length, hide, max_folds, best_score=-1):
    if max_folds != 0 and folded >= max_folds:
        return 0,[]
    if depth == length-1:
        score,new_protein = complete_protein(protein, hide, best_score)
        return score, new_protein
    best_protein = None
    best_score, best_protein = partial_protein(protein, depth, \
                        length, hide, max_folds, best_score, best_protein)
    return best_score, best_protein


def fold(protein, max_folds, hide):
    best_fold = fold_rec(protein, 1, len(protein), hide, max_folds)
    return best_fold 

def print_protein(protein):
    protein = protein[1:]
    for i, aminoacid in enumerate(protein):
        print(i, aminoacid[0], aminoacid[1],
              "("+str(aminoacid[2][0])+","+str(aminoacid[2][1])+")")
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

def card_offset(orientation):
    if orientation == 'N':
        offset = (0,1)
    elif orientation == 'S':
        offset = (0,-1)
    elif orientation == 'E':
        offset = (1,0)
    else:
        offset = (-1,0)
    return offset



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
            "protein=", "best"]
    help_text = "You asked for help?"
    bench = False
    max_folds = 0
    protein_string = ""
    hide = 0
    # 0 show all
    # 1 show if one better pops up
    # 2 show better of all
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
        if current_arg in ("-n","--not_show","--best"):
            hide = 2
            if current_arg == "--best":
                hide = 1
            
    return bench, hide, max_folds, protein_string

def handle_parameters():
    bench, hide, max_folds, protein_string = parse_arguments()
    max_folds_conf, seed,  protein_string_conf = read_config_file("params.conf") 
    if max_folds == 0:
        max_folds = max_folds_conf
    if protein_string == "":
        protein_string = protein_string_conf
    if len(protein_string) < 3:
        print("Protein must have at least 3 aminoacids")
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
    max_folds = 350000
    protein_string_complex = "HPHPHHPHPHHPPHHPHPH"
    protein_string_simple = "HPHPHH"
    
    protein = parse_protein(protein_string_complex)
    fold(protein, max_folds, hide)

def main():
    bench, hide, seed, max_folds, protein = handle_parameters()
    if bench == True:
        if hide == 0:
            cProfile.run("profile( 0 )")
        elif hide == 1:
            cProfile.run("profile( 1 )")
        else:
            cProfile.run("profile( 2 )")
        sys.exit(0)

    best_fold = fold(protein, max_folds, hide)
    protein = best_fold[1]
    score = best_fold[0]
    draw_protein(protein)
    print("Score",score)


if __name__=="__main__":
    main()



