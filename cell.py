#Sudoku solver. Cell Class. Python 3.6.0


class Cell:
    
    def __init__ (self, row, column):
        self.__name = row + column
        self.__value = ''
        self.__peers = []
        self.__is_constant = False
        
        
    def get_name(self):
        return self.__name
    def get_value(self):
        return self.__value
    def get_peers(self):
        return self.__peers
    def get_is_constant(self):
        return self.__is_constant


    def set_value(self, value):
        self.__value = value
    def set_peers(self, peers):
        self.__peers = peers
    def set_is_constant(self, boolean):
        self.__is_constant = boolean


