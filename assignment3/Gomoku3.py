#!/usr/bin/python3
# Set the path to your python3 above

from gtp_connection import GtpConnection
from board_util import GoBoardUtil
from simple_board import SimpleGoBoard
import Gomoku

class Gomoku3():
    def __init__(self):
        """
        Gomoku player that selects moves randomly 
        from the set of legal moves.
        Passe/resigns only at the end of game.

        """
        self.name = "GomokuAssignment3"
        self.version = 1.0
        
    def get_move(self, board, color):
        return GoBoardUtil.generate_random_move_gomoku(board)
    
def run():
    """
    start the gtp connection and wait for commands.
    """
    board = SimpleGoBoard(7)
    con = GtpConnection(Gomoku3(), board)
    con.start_connection()

if __name__=='__main__':
    Gomoku.run()
