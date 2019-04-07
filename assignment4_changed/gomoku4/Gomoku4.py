#!/usr/bin/env python
#/usr/local/bin/python3
# Set the path to your python3 above

from gtp_connection import GtpConnection
from board_util import GoBoardUtil, EMPTY
from simple_board import SimpleGoBoard

import random
import numpy as np
import pickle

def undo(board,move):
    board.board[move]=EMPTY
    board.current_player=GoBoardUtil.opponent(board.current_player)

def play_move(board, move, color):
    board.play_move_gomoku(move, color)

def game_result(board):
    game_end, winner = board.check_game_end_gomoku()
    moves = board.get_empty_points()
    board_full = (len(moves) == 0)
    if game_end:
        #return 1 if winner == board.current_player else -1
        return winner
    if board_full:
        return 'draw'
    return None

class GomokuSimulationPlayer(object):
    """
    For each move do `n_simualtions_per_move` playouts,
    then select the one with best win-rate.
    playout could be either random or rule_based (i.e., uses pre-defined patterns) 
    """
    def __init__(self, n_simualtions_per_move=10, playout_policy='rule_based', board_size=7):
        assert(playout_policy in ['random', 'rule_based'])
        self.n_simualtions_per_move=n_simualtions_per_move
        self.board_size=board_size
        self.playout_policy=playout_policy

        #NOTE: pattern has preference, later pattern is ignored if an earlier pattern is found
        self.pattern_list=['Win', 'BlockWin', 'OpenFour', 'BlockOpenFour', 'Random']

        self.name="Gomoku4"
        self.version = 3.0
        self.best_move=None
        self.path = "/".join(__file__.split("/")[:-1] + ["exp.dat"])
        try:
            with open(self.path, 'rb') as f:
                self.exp = pickle.load(f)
        except Exception:
            self.exp = {}

    def save_exp(self):
        with open(self.path, 'wb') as f:
            pickle.dump(self.exp,f)
        
    def set_playout_policy(self, playout_policy='random'):
        assert(playout_policy in ['random', 'rule_based'])
        self.playout_policy=playout_policy

    def _random_moves(self, board, color_to_play):
        return GoBoardUtil.generate_legal_moves_gomoku(board)
    
    def policy_moves(self, board, color_to_play):
        if(self.playout_policy=='random'):
            return "Random", self._random_moves(board, color_to_play)
        else:
            assert(self.playout_policy=='rule_based')
            assert(isinstance(board, SimpleGoBoard))
            ret=board.get_pattern_moves()
            if ret is None:
                return "Random", self._random_moves(board, color_to_play)
            movetype_id, moves=ret
            return self.pattern_list[movetype_id], moves
    
    def _do_playout(self, board, color_to_play):
        res=game_result(board)
        simulation_moves=[]
        while(res is None):
            _ , candidate_moves = self.policy_moves(board, board.current_player)
            playout_move=random.choice(candidate_moves)
            play_move(board, playout_move, board.current_player)
            simulation_moves.append(playout_move)
            res=game_result(board)
        for m in simulation_moves[::-1]:
            undo(board, m)
        if res == color_to_play:
            return 1.0
        elif res == 'draw':
            return 0.0
        else:
            assert(res == GoBoardUtil.opponent(color_to_play))
            return -1.0

    def get_move(self, board, color_to_play):
        """
        The genmove function called by gtp_connection
        """
        if len(board.get_current_player_points()) <= 6:
            # first 6 steps use score-based strategy
            all_possible_moves = board.get_empty_points()
            moves = board.ScanBoard(all_possible_moves)
            # add simulation
            
            return moves[0]
        else:
            # use ruled-based simulation
            pattern,moves=self.policy_moves(board, board.current_player)
            if pattern == self.pattern_list[0] or pattern == self.pattern_list[1]:
                self.save_exp()
            toplay=board.current_player
            h = hash(board.board.tostring()) # hashing the current board state
            if h not in self.exp:
                self.exp[h] = ([-1.1,None],{},{})
            best,wins,visits = self.exp[h]
            self.best_move = moves[0]
            while True:
                for move in moves:
                    play_move(board, move, toplay)
                    res=game_result(board)
                    if res == toplay:
                        undo(board, move)
                        #This move is a immediate win
                        self.best_move=move
                        return move
                    ret=self._do_playout(board, toplay)
                    wins[move] = wins.get(move,0)+ret
                    visits[move] = visits.get(move,0)+1
                    win_rate = wins[move] / visits[move]
                    if win_rate > best[0]:
                        best[0]=win_rate
                        best[1]=move
                        self.best_move=move
                    undo(board, move)
            assert(best[1] is not None)
            return best[1]

def run():
    """
    start the gtp connection and wait for commands.
    """
    board = SimpleGoBoard(7)
    con = GtpConnection(GomokuSimulationPlayer(), board)
    con.start_connection()

if __name__=='__main__':
    run()
