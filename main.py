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
cohort_size = 10
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
            sudoku_fitness = 0
            correct_values = 0
            ###print(partial_solution)
            ###print(solution[i])
            ###print(solution[i][0])
            
            #sudoku_cells = sudokus[i].get_cells()
            outputs = list(map(int, net.activate(inputs[i])))
            
            for cell in outputs:
                if cell < 1:
                    #print('invalid value')
                    sudoku_fitness -= 10000000
                elif cell > 9:
                    sudoku_fitness -= 10000
                elif cell == solution[i][cell]:
                    #print('Great stuff mate!')
                    correct_values += 1
                    sudoku_fitness += 50*correct_values

                ### check for peers in given values: reward for selecting a valid value

                
                '''if solution[i][cell_ID-1] == cell_value:
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
                    break'''
                
            '''print('Attempt:')
            output.print_grid(outputs)    
            print('Solution:')
            output.print_grid(solution[i])'''
            
            ###print(eval_fitness.organism, correct_values, sudoku_fitness)
            genome.fitness += sudoku_fitness
        
        #print ('Organism: %s\tFitness: %s\n' % (eval_fitness.organism, genome.fitness))

def run(config_file):
    #Load configuration file parameters.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    #Create or load a population.
    last_checkpoint = ''
    mixer.music.load('assets/sound/bleep.mp3')
    mixer.music.play()
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
    pop.add_reporter(neat.Checkpointer(5000, 9000))

    # Run for 100 generations.
    winner = pop.run(eval_fitness, 25001)
    #print('\nBest genome:\n{!s}'.format(winner))
    
    # Display output of the most fit genome against overall population fitness (install and import visualize module).
    #visualize.draw_net(config, winner, True)
    #visualize.plot_stats(stats, ylog=False, view=True)
    #visualize.plot_species(stats, view=True)
    mixer.music.load('assets/sound/bleep.mp3')
    mixer.music.play()
    print('\nRun finished.')

# Main function.
if __name__ == '__main__':
    config_path = os.path.join(local_dir, 'config')
    run(config_path)
       
    #print('\nDeep solution time of %s sudokus:\t%.3f sec.' % (cohort_size,end_time-start_time))
    #print('Sudokus with multiple solutions:\t%s' % invalid_sudokus)

   
