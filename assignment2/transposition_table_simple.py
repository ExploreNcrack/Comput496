# Cmput 496 sample code
# Simple transposition table for TicTacToe solver
# This is much slower than an array-based table
# which is used in competitive programs
# Written by Martin Mueller

class TranspositionTable(object):
# Table is stored in a dictionary, with board code as key, 
# and minimax score as the value

    # Empty dictionary
    def __init__(self):
        self.table = {}

    # Used to print the whole table with print(tt)
    def __repr__(self):
        return self.table.__repr__()
        
    def store(self, code, score):
        self.table[code] = score
    
    # Python dictionary returns 'None' if key not found by get()
    def lookup(self, code):
        return self.table.get(code)
