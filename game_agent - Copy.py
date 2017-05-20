"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random
import json

class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")
    
    x, y = game.get_player_location(player)
    w, h = game.width / 2., game.height / 2.
    
    f = open("logfile.txt", "a")
    json.dump(game.get_player_location(game.active_player), f)
    f.write("**")
    json.dump(game.get_player_location(game.inactive_player), f)
    f.write("\n")
    json.dump(game.get_legal_moves(game.active_player), f)  
    f.write("\n")
    json.dump(game.get_legal_moves(game.inactive_player), f)
    f.write("\n")
    
    f.write(str(sum((h - y)**2 + (w - x)**2 for x, y in game.get_legal_moves(player))))
    f.write("************************************\n")
    f.close()
    return float(sum((w-x)*(w-a)*(a-x) + (h-y)*(h-b)*(b-y) for a, b in game.get_legal_moves(player)))
    

def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")
    w, h = game.get_player_location(player)
    
#    f = open("logfile.txt", "a")
#    json.dump(game.get_player_location(game.active_player), f)
#    f.write("**")
#    json.dump(game.get_player_location(game.inactive_player), f)
#    f.write("\n")
#    json.dump(game.get_legal_moves(game.active_player), f)  
#    f.write("\n")
#    json.dump(game.get_legal_moves(game.inactive_player), f)
#    f.write("\n")
#    
#    f.write(str(sum((h - y)**2 + (w - x)**2 for x, y in game.get_legal_moves(player))))
#    f.write("************************************\n")
#    f.close()
    
    return float(sum((h - y)**2 + (w - x)**2 for x, y in game.get_legal_moves(player)))


def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.
    
    Score based on poistion of legal moves relative to the current location and board center
    
    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")
    
    computer_moves = len(game.get_legal_moves(game.active_player))                    
    opponent_moves = len(game.get_legal_moves(game.inactive_player))                      
    if computer_moves == 0 and opponent_moves != 0:       
        return float ('-inf')
    elif computer_moves != 0 and opponent_moves == 0:     
        return float ('inf')
    elif computer_moves == 0 and opponent_moves == 0:
        return -10
    else:
        return float(computer_moves - opponent_moves)


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = 100.
        self.TIMER_THRESHOLD = timeout

class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            legal_moves = game.get_legal_moves(game.active_player)
#            f = open("logfile.txt", "a")
#            #json.dump(game.active_player, f)
#            f.write("\n")
#            json.dump(legal_moves, f)            
#            f.write("\n")
#            f.close()
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            print(self.name)
            best_move = legal_moves[random.randint(0, len(legal_moves))]
            print('==')
            print(best_move)
            print("\n")

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        
        #if self.time_left() < self.TIMER_THRESHOLD:
        #    raise SearchTimeout()
        
        legalMoves = game.get_legal_moves(game.active_player)
#        f = open("logfile.txt", "a")
#        json.dump(game.get_player_location(game.active_player), f)
#        f.write("\n")
#        f.close()
        if len(legalMoves) < 1:
            return (-1,-1)
        elif len(legalMoves) == 1:
            return legalMoves[0]
        
        def max_value (self, game, depth):
            if depth == 0 or self.time_left() < self.TIMER_THRESHOLD: 
                return self.score(game, game.active_player)                                 
            v = float ("-inf")
            for a in game.get_legal_moves(game.active_player):
                v = max (v, min_value (self, game.forecast_move(a), depth - 1))
            return v
                

        def min_value (self, game, depth):
            if depth == 0 or self.time_left() < self.TIMER_THRESHOLD: 
                return self.score(game, game.active_player)
            v = float ("inf")
            for a in game.get_legal_moves(game.active_player):
                v = min (v, max_value (self, game.forecast_move(a), depth - 1))
            return v
        
        return max (legalMoves, key = lambda a: min_value (self, game, depth))


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)
        legal_moves = game.get_legal_moves(game.active_player)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.alphabeta(game, self.search_depth, float ("-inf"), float ("inf"))

        except SearchTimeout:
            best_move = legal_moves[random.randint(0, len(legal_moves))]
            print(self.name)
            print('==')
            print(best_move)
            print("\n")

        # Return the best move from the last completed search iteration
        return best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        legalMoves = game.get_legal_moves(game.active_player)
        
        if len(legalMoves) < 1:
            return (-1,-1)
        elif len(legalMoves) == 1:
            return legalMoves[0]
        
        def max_value (self, game, depth, alpha, beta):
            if depth == 0 or self.time_left() < self.TIMER_THRESHOLD:            #Checks to see if the depth limit has been reached or if time is almost out
                return self.score(game, game.active_player);                                   
            v = float ("-inf")
            for a in game.get_legal_moves(game.active_player):
                v = max (v, min_value (self, game.forecast_move(a), depth - 1, alpha, beta))
                if v >= beta:
                    return v
                alpha = max (alpha, v)
            return v
                

        def min_value (self, game, depth, alpha, beta):
            if depth == 0 or self.time_left() < self.TIMER_THRESHOLD:            #Checks to see if the depth limit has been reached or if time is almost out
                return self.score(game, game.active_player);
            v = float ("inf")
            for a in game.get_legal_moves(game.active_player):
                v = min (v, max_value (self, game.forecast_move(a), depth - 1, alpha, beta))
                if v <= alpha:
                    return v
                beta = min (beta, v)
            return v
        return max (legalMoves, key = lambda a: min_value (self, game, depth, float ("-inf"), float ("inf")))
