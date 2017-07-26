#Sudoku solver. Solver Module. Python 3.6.0

import time
import copy
import sudoku
import output

digits = '123456789'
digit_list = []
timestamp = []
solution = []

for digit in digits:
    digit_list.append(digit)


def solve(sudoku):
    sudoku_cells = sudoku.get_cells()
    del timestamp[:]
    del solution[:]
    start_time = time.time()
    timestamp.append(start_time)
    evaluate_cells(sudoku_cells)
    end_time = time.time()
    recursion_time = end_time - start_time
    print('Time to finish recursive function:\t%.3f sec.' % recursion_time)
    return solution


def generate_options(cell):
    options = list(digit_list)
    for peer in cell.get_peers():
        if peer.get_value() in options:
            options.remove(peer.get_value())
    return options

# Recursive function brute forcing solutions. Change to return function to
# cancel deep evaluation (i.e. whether there is more than one solution)
def evaluate_cells(sudoku_cells,iteration = 0):
    cell = sudoku_cells[iteration]
    if cell.get_is_constant():
        if iteration == len(sudoku_cells)-1:
            process_solution(sudoku_cells)
        else: iterate_cell(sudoku_cells,iteration)
    else:
        options = list(generate_options(cell))
        if len(options) > 0:
            for option in options:
                cell.set_value(option)
                if iteration == len(sudoku_cells)-1:
                    process_solution(sudoku_cells)
                else:
                    iterate_cell(sudoku_cells,iteration)
                    cell.set_value('0')
        else: cell.set_value('0')

def iterate_cell(sudoku_cells,iteration):
    if iteration < len(sudoku_cells)-1:
        iteration += 1
    evaluate_cells(sudoku_cells,iteration)

def process_solution(sudoku_cells):
    end_time = time.time()
    solve_time = end_time - timestamp[0]
    for cell in sudoku_cells:
        solution.append(cell.get_value())
    print('Time for solution:\t\t\t%.3f sec.' % solve_time)

    
