"""
 1: win
-1: lose
 0: draw
"""

def Search(state):
	"""
	Input:
		state: current SimpleGoBoard class
		contains information about the current board state
	Return:
		 1: win
		-1: lose
		 0: draw
	Call negamax to find out the result 
	"""
    result = negamaxBoolean(state)
    if result == 0:
    	# result is draw
    	pass
    elif result == -1:
    	# result is lose
    	pass
    elif result == 1:
    	# result is win
    	pass


def negamaxBoolean(state):
	"""
	 1: win
	-1: lose
	 0: draw
	"""
    # end game with one of the player win first
    endGame, winner = state.check_game_end_gomoku() 
    if endGame:
    	if winner == state.current_player:
    		return 1
    	else:
    		return -1
    # empty points at that board stat are the legal possible moves
    allPossibleMove = state.get_empty_points()
    # check if draw condition
    if len(allPossibleMove) == 0:
    	# draw condition
    	return 0
    # game not ended yet continue to search (go deeper level in the game tree)
    for m in allPossibleMove:
        state.play_move_gomoku(m)
        success = -negamaxBoolean(state)
        state.undoMove()
        if success:
            return 1
    return -1
