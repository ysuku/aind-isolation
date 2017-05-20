"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import itertools
class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
   if game.is_loser(player):
        return float("-inf")

   if game.is_winner(player):
        return float("inf")
    
   x, y = game.get_player_location(player)
   w, h = game.width / 2., game.height / 2.
   movAdv = float(len(game.get_legal_moves(player)) - len(game.get_legal_moves(game.inactive_player)))
    
   return float(sum(((w-x)*(w-a) + (h-y)*(h-b))*movAdv for a, b in game.get_legal_moves(player)))
    

def custom_score_2(game, player):
   if game.is_loser(player):
        return float("-inf")

   if game.is_winner(player):
        return float("inf")
   w, h = game.get_player_location(player)
    
   return float(sum((h - y) + (w - x) for x, y in game.get_legal_moves(player)))


def custom_score_3(game, player):
   if game.is_loser(player):
        return float("-inf")

   if game.is_winner(player):
        return float("inf")
    
   return float(len(game.get_legal_moves(player)) - len(game.get_legal_moves(game.inactive_player)))


class IsolationPlayer:
    
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=25.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

class MinimaxPlayer(IsolationPlayer):
   
    def get_move(self, game, time_left):
       
        self.time_left = time_left
#        best_move = (-1, -1)

        try:
            legal_moves = game.get_legal_moves(game.active_player)  
            return self.minimax(game, self.search_depth)
        except SearchTimeout:
            pass 
            
        return legal_moves[0]

    def minimax(self, game, depth):
        legalMoves = game.get_legal_moves(game.active_player)
        
        if len(legalMoves) < 1:
            return (-1,-1)
        elif len(legalMoves) == 1:
            return legalMoves[0]

        if self.time_left() < self.TIMER_THRESHOLD + 50:
            return legalMoves[0]    
          
        def max_value (self, game, depth):            
            if depth == 0 or self.time_left() < self.TIMER_THRESHOLD + 50: 
                return self.score(game, game.active_player) 
       
            v = float ("-inf")
            for a in game.get_legal_moves(game.active_player):
                v = max (v, min_value (self, game.forecast_move(a), depth - 1))
            return v
                
        def min_value (self, game, depth):            
            if depth == 0 or self.time_left() < self.TIMER_THRESHOLD + 50:
                return self.score(game, game.active_player)
            v = float ("inf")
            for a in game.get_legal_moves(game.active_player):
                v = min (v, max_value (self, game.forecast_move(a), depth - 1))
            return v
        return max (legalMoves, key = lambda a: min_value (self, game.forecast_move(a), depth))


class AlphaBetaPlayer(IsolationPlayer):
   
    def get_move(self, game, time_left):
        
        self.time_left = time_left
        legal_moves = game.get_legal_moves(game.active_player)
        if len(legal_moves) < 1:
            return (-1,-1)
        elif len(legal_moves) == 1:
            return legal_moves[0]
        
        best_move = legal_moves[0]
        
        try:
            for i in itertools.count():
                best_move = self.alphabeta(game, i, float ("-inf"), float ("inf"))
                if self.time_left() < self.TIMER_THRESHOLD+150:
                    break
                
        except SearchTimeout:
            pass           

        return best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
       
        legalMoves = game.get_legal_moves(game.active_player)
        
        if len(legalMoves) < 1:
            return (-1,-1)
        elif len(legalMoves) == 1:
            return legalMoves[0]

        if self.time_left() < self.TIMER_THRESHOLD + 150:
            return legalMoves[0]      
        
        def max_value (self, game, depth, alpha, beta):
            if depth == 0 or self.time_left() < self.TIMER_THRESHOLD+150: 
                return self.score(game, game.active_player);                                   
            v = float ("-inf")
            for a in game.get_legal_moves(game.active_player):
                v = max (v, min_value (self, game.forecast_move(a), depth - 1, alpha, beta))
                if v >= beta:
                    return v
                alpha = max (alpha, v)
            return v
                

        def min_value (self, game, depth, alpha, beta):
            if depth == 0 or self.time_left() < self.TIMER_THRESHOLD+150: 
                return self.score(game, game.active_player);
            v = float ("inf")
            for a in game.get_legal_moves(game.active_player):
                v = min (v, max_value (self, game.forecast_move(a), depth - 1, alpha, beta))
                if v <= alpha:
                    return v
                beta = min (beta, v)
            return v
        
        return max (legalMoves, key = lambda a: min_value (self, game.forecast_move(a), depth, float ("-inf"), float ("inf")))
