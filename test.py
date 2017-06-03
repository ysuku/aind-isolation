# -*- coding: utf-8 -*-
"""
Created on Mon May  8 16:24:43 2017

@author: syandra
"""

from isolation import Board
from sample_players import RandomPlayer
from game_agent import AlphaBetaPlayer, custom_score_3

player2 = RandomPlayer()
player1 = AlphaBetaPlayer(score_fn=custom_score_3)
game = Board(player1, player2, 9, 9)   # 9, 9 is the size of the board
player1.search_depth = 2

game._board_state = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0,0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 25, 48]
print(game.to_string())

print(game.get_legal_moves())

winner, history, outcome = game.play(time_limit=60000000)
print("\nWinner: {}\nOutcome: {}".format(winner, outcome))
print(game.to_string())
print("hello")

print("Move history:\n{!s}".format(history))
