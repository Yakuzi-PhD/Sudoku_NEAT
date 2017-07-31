#Sudoku solver. Output Class. Python 3.6.0

rows = 'ABCDEFGHI'

# Print cell values in grid layout
def print_grid(grid):
    line = ''
    for i in range(len(grid)):
        line += str(grid[i])
        if (i+1)%9 == 0:
            print(line)
            line = ''
    print('')


