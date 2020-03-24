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
    score = 0
    for aminoacid in protein_string:
        if aminoacid[0] == 'H':
            neighbor_1 = protein_string[aminoacid[1]][0]
            neighbor_2 = protein_string[aminoacid[2]][0]
            if neighbor_1 == "H":
                score += 1
            if neighbor_2 == "H":
                score += 1
    return score
            
def parse_protein(protein_string):
    protein_struct = []
    protein_struct.append(['N',0,0])
    for aminoacid in protein_string:
        protein_struct.append([aminoacid,0,0])
    return protein_struct

def main():
    steps, seed, protein_string = \
            read_config_file_configparser("params.conf")
    print(steps, seed, protein_string)
    protein_struct = parse_protein(protein_string)
    for i, aminoacid in enumerate(protein_struct):
        print(i, aminoacid)
    print(score(protein_struct))

if __name__=="__main__":
    main()
