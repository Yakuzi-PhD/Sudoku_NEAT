#Sudoku solver. Python 3.6.0


### TODO ###
'''
- Stop recursive function in solver module

'''

import os, sys
import time
import random
import copy
import neat
import cell
import sudoku
import solver
import output
from pygame import mixer


# Specify the name of the sudoku input file here.
file_name = 'dif-1.php'
local_dir = os.path.dirname(__file__)
sudoku_dir = os.path.join(local_dir, 'sudokus')
cohort_size = 25

mixer.init()


digits = '123456789'
rows = 'ABCDEFGHI'
columns = digits
digit_list = []

for digit in digits:
    digit_list.append(digit)
#--------------------------------------------------------------------------------------#
# Load puzzles in file ### MOVE TO SEPARATE FILE
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
#--------------------------------------------------------------------------------------#

def generate_options(cell):
    options = list(digit_list)
    for peer in cell.get_peers():
        if peer.get_value() in options:
            options.remove(peer.get_value())
    return options

def eval_fitness(genomes, config):
    eval_fitness.organism = 0
    sudokus = load_sudokus(cohort_size)
    inputs = []
    solution = []

    # Generate a list of sudoku init and corresponding solution values.
    ###CHANGE TO SEPARATE FUNCTION AND CALL ABOVE @ inputs = []
    for sudoku in sudokus:
        inputs.append(list(map(int,sudoku.get_values())))
        solution.append(list(map(int, solver.solve(sudoku))))

    
    for genome_id, genome in genomes:
        eval_fitness.organism += 1
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)

        for i in range(cohort_size):
            partial_solution = inputs[i]
            sudoku_fitness = 0
            ###print(partial_solution)
            ###print(solution[i])
            ###print(solution[i][0])
            
            while 0 in partial_solution:
                sudoku_cells = sudokus[i].get_cells()
                outputs = net.activate(partial_solution)
                cell_ID = int(outputs[0]*82)
                cell_value = int(outputs[1]*10)
                
                ### INSERT VALID VALUE LOGIC BASED ON CELL PEERS
                if cell_ID < 1 or cell_ID > 81:
                    #print('invalid cell')
                    sudoku_fitness -= 100
                    break
                if cell_value < 1 or cell_value > 9:
                    #print('invalid value')
                    sudoku_fitness -= 100
                    break
                if partial_solution[cell_ID-1] != 0:
                    #print('We already know that answer Einstein')
                    sudoku_fitness -= 50
                    break

                cell = sudoku_cells[cell_ID-1]
                options = list(map(int, generate_options(cell)))
                ###print('cell index', cell_ID, '\tvalid options', options)

                
                if solution[i][cell_ID-1] == cell_value:
                    #print('Awesome!!!!', solution[i][cell_ID-1], cell_value)
                    cell.set_value(cell_value)
                    partial_solution[cell_ID-1] = cell_value
                    sudoku_fitness += 10
                    
                elif cell_value in options:
                    #print('Valid number... but not the correct number.', solution[i][cell_ID-1], cell_value)
                    partial_solution[cell_ID-1] = cell_value
                    cell.set_value(cell_value)
                    partial_solution[cell_ID-1] = cell_value
                    sudoku_fitness += 2
                else:
                    sudoku_fitness -= 10
                    #print('Valid cell, but invalid answer', solution[i][cell_ID-1], cell_value)
                    break

            if 0 not in partial_solution:
                sudoku_fitness *= 10
            sol = []
            for cell in sudoku_cells:
                sol.append(cell.get_value())
            #output.print_grid(sol)
            #output.print_grid(partial_solution)
            #output.print_grid(solution[i])
            genome.fitness += sudoku_fitness
        
        #print ('Organism: %s\tFitness: %s' % (eval_fitness.organism, genome.fitness))

def run(config_file):
    #Load configuration file parameters.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    #Create or load a population.
    last_checkpoint = ''
    for file in os.listdir(local_dir):
        if 'neat-checkpoint' in file:
            last_checkpoint = file
    try:
        pop = neat.Checkpointer.restore_checkpoint(last_checkpoint)
        print('Loading last population save state.')
        time.sleep(2)
    except:
        pop = neat.Population(config)
        print('No previous save state found. Generating new population.')
        time.sleep(2)

    # Add reporter modules.
    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)

    #Create a checkpoint every x generations or y seconds.
    pop.add_reporter(neat.Checkpointer(1000, 1800))

    # Run for 100 generations.
    winner = pop.run(eval_fitness, 1000)
    print('\nBest genome:\n{!s}'.format(winner))
    
    # Display output of the most fit genome against overall population fitness (install and import visualize module).
    #visualize.draw_net(config, winner, True)
    #visualize.plot_stats(stats, ylog=False, view=True)
    #visualize.plot_species(stats, view=True)
    mixer.music.load('assets/sound/radar.mp3')
    mixer.music.play()
    print('\nRun finished.')

# Main function.
if __name__ == '__main__':
    config_path = os.path.join(local_dir, 'config')
    mixer.music.load('assets/sound/radar.mp3')
    mixer.music.play()
    run(config_path)
       
    #print('\nDeep solution time of %s sudokus:\t%.3f sec.' % (cohort_size,end_time-start_time))
    #print('Sudokus with multiple solutions:\t%s' % invalid_sudokus)

   
