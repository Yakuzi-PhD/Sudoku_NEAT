#Sudoku solver. Cell Class. Python 3.6.0

import cell

digits = '123456789'
rows = 'ABCDEFGHI'
columns = digits


class Sudoku:

    def __init__ (self, input_string):
        self.__cells = generate_grid(input_string)
        
    def get_cells(self):
        return self.__cells

    def get_values(self):
        values = []
        for cell in self.__cells:
            values.append(cell.get_value())
        return values



# Generate a 9x9 grid of cells.
def generate_grid(input_string):
    cells=[]
    for r in rows:
        for c in columns:
            cells.append(cell.Cell(r, c))
    assign_peers(cells)
    seed_grid(cells,input_string)
    return cells

def cross (rows, columns):
    return [r+c for r in rows for c in columns]

def seed_grid(cells,input_string):
    for i in range(len(input_string)):
        cells[i].set_value(input_string[i])
        if input_string[i] != '0': cells[i].set_is_constant(True)

# Assign peers in the row, column and region of each cell.
def assign_peers(cells): 
    sections = ([cross(rows, c) for c in columns] +
                [cross(r, columns) for r in rows] +
                [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')])
    for c in cells:
        peer_names = []
        for s in sections:
            if c.get_name() in s: peer_names.extend(s)
        peer_list = set(find_cells(cells,peer_names))
        peer_list.remove(c)
        c.set_peers(peer_list)

def find_cells(cells,peers):
    cell_list = []
    for c in cells:
        if c.get_name() in peers: cell_list.append(c)
    return cell_list







