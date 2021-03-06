import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 100         # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 2.0   # Score for squares played by the other player
    
# Add your functions here.

def mc_trial(board, player):
    """
    This function takes a current board and the next player to move. 
    The function should play a game starting with the given player 
    by making random moves, alternating between players. 
    The function should return when the game is over. 
    The modified board will contain the state of the game, 
    so the function does not return anything. 
    In other words, the function should modify the board input.
    """
    while True:
        empties = board.get_empty_squares()
        randommove = empties[random.randrange(len(empties))]
        board.move(randommove[0], randommove[1], player)
        if board.check_win() is not None:
            return None
        player = provided.switch_player(player)

def mc_update_scores(scores, board, player):
    """
    This function takes a grid of scores (a list of lists) 
    with the same dimensions as the Tic-Tac-Toe board, 
    a board from a completed game, and which player 
    the machine player is. The function should score 
    the completed board and update the scores grid. 
    As the function updates the scores grid directly, 
    it does not return anything
    """
    won = board.check_win()
    if won == player:
        pos = 1
    elif won == provided.switch_player(player):
        pos = -1
    else: 
        return

    for i__ in range(board.get_dim()):
        for j__ in range(board.get_dim()):
            state = board.square(i__, j__)
            if state == provided.EMPTY or state == provided.DRAW:
                continue
            elif state == player:
                scores[i__][j__] += pos * SCORE_CURRENT
            elif state == provided.switch_player(player):
                scores[i__][j__] -= pos * SCORE_OTHER
                
    
    return None

def get_best_move(board, scores): 
    """
    This function takes a current board and a grid of scores. 
    The function should find all of the empty squares with 
    the maximum score and randomly return one of them as a 
    (row, column) tuple. It is an error to call this function 
    with a board that has no empty squares (there is no 
    possible next move), so your function may do whatever i
    it wants in that case. The case where the board is full 
    will not be tested.
    """
    best = [None,-1,-1]
    for i__ in range(board.get_dim()):
        for j__ in range(board.get_dim()):
            if board.square(i__, j__) == provided.EMPTY:
                if best[0] == None:
                    best = [scores[i__][j__], i__, j__]
                elif best[0] < scores[i__][j__]:
                    best = [scores[i__][j__], i__, j__]
    return (best[1],best[2])               
            
def mc_move(board, player, trials):
    """
    This function takes a current board, which player the 
    machine player is, and the number of trials to run. 
    The function should use the Monte Carlo simulation 
    described above to return a move for the machine 
    player in the form of a (row, column) tuple. Be sure 
    to use the other functions you have written!
    """
    scores = [[ 0 for _ in range(board.get_dim())] 
                  for _ in range(board.get_dim())]
    for _ in range(trials):
        tempboard = board.clone()
        mc_trial(tempboard, player)
        mc_update_scores(scores, tempboard, player)
    return get_best_move(board, scores)
        
        
    

# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.

#provided.play_game(mc_move, NTRIALS, False)        
poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)


A = ''' # comment out this line and the one at the end to reenable tests.
def testttt():
    import poc_simpletest
    suite = poc_simpletest.TestSuite()
    board = provided.TTTBoard(3)
    suite.run_test(get_best_move(board,
                                 [[0,1,0],[0,0,0],[0,0,0]]),
                                 (0,1),"test1")

    
testttt()
'''
