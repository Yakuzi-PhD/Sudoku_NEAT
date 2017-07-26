#Sudoku solver. Python 3.6.0


### TODO ###
'''
- Stop recursive function in solver module

'''

import os, sys
import time
import random
import neat
import cell
import sudoku
import solver
import output


# Specify the name of the puzzle input file here.
file_name = 'dif-1.php'
local_dir = os.path.dirname(__file__)
sudoku_dir = os.path.join(local_dir, 'sudokus')
cohort_size = 1

digits = '123456789'
rows = 'ABCDEFGHI'
columns = digits


# Load puzzles in file
def load_sudokus(number):
    selected_sudokus = []
    input_file = os.path.join(sudoku_dir, file_name)
    raw_list = parse_file(input_file)
    selection = random.sample(raw_list, number)
    for puzzle in selection:
        selected_sudokus.append(sudoku.Sudoku(puzzle))
    return selected_sudokus

# Parse the input file and return a list of valid sudokus in raw text format
def parse_file(input_file):
    sudoku_list=[]
    with open(input_file) as file: 
        for line in file:
            parsed_line = parse_line(line)
            if len(parsed_line) == 81 : sudoku_list.append(parsed_line)
    return sudoku_list

# Parse individual sudoku values
def parse_line(input_string):
    parsed_string = []
    for char in input_string:
        if char in digits or char in '0': parsed_string.extend(char)
        elif char in '.*xX': parsed_string.extend('0')
    return parsed_string


# Main function.
if __name__ == '__main__':
    sudokus = load_sudokus(cohort_size)
    start_time = time.time()
    for sudoku in sudokus:
        output.print_grid(sudoku.get_values())
        solution = solver.solve(sudoku)
        output.print_grid(solution)
    end_time = time.time()
       
    print('\nDeep solution time of %s sudokus:\t%.3f sec.' % (cohort_size,end_time-start_time))
    #print('Sudokus with multiple solutions:\t%s' % invalid_sudokus)

