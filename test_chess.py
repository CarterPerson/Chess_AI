# pip3 install python-chess



import chess
from RandomAI import RandomAI
from HumanPlayer import HumanPlayer
from MinimaxAI import MinimaxAI
from AlphaBetaAI import AlphaBetaAI
from ChessGame import ChessGame
from IterativeDeepeningAI import IterativeDeepeningAI


import sys

#player1 = AlphaBetaAI(3, True)
#player2 = MinimaxAI(3, False)

#game = ChessGame(player1, player2)

#while not game.is_game_over():
#   print(game)
#   game.make_move()
#print("\n Game is Over!!!! \n \n \n")

player1 = HumanPlayer()
player2 = AlphaBetaAI(4, False)

game = ChessGame(player1, player2)

while not game.is_game_over():
    print(game)
    game.make_move()


#print(hash(str(game.board)))
