from transposition_table_simple import TranspositionTable
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
	# begin the search the result for current state
	tt = TranspositionTable() # use separate table for each color
    result = negamaxBoolean(state, tt)
    if result == 0:
    	pass
    elif result == -1:
    	pass
    elif result == 1:
    	pass

def storeResult(tt, state, result):
    tt.store(state.code(), result)
    return result


def negamaxBoolean(state, tt):
	# if the state has previous computed 
	# by checking the transposition table
	# avoid computed again 
	result = tt.lookup(state.code())
	if result != None:
		# directly return
        return result
    # end game with one of the player win
    endGame, winner = state.check_game_end_gomoku() 
    if endGame:
    	if winner == state.current_player:
    		return storeResult(tt, state, 1)
    	else:
    		return storeResult(tt, state, -1)
    # check if draw condition
    allPossibleMove = state.get_empty_points()
    if len(allPossibleMove) == 0:
    	# draw condition
    	return storeResult(tt, state, 0)
    # game not ended yet continue to search (go deeper level in the game tree)
    for m in allPossibleMove:
        state.play_move_gomoku(m)
        success = not negamaxBoolean(state, tt)
        state.undoMove()
        if success:
            return storeResult(tt, state, 1)
    return storeResult(tt, state, -1)
