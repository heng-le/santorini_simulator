from board import Board
from player import Player
from game import GameManager
from strategy import HumanMoveStrategy, RandomMoveStrategy
import argparse 

def main():
    while True:
        board = Board()

        strategy1 = RandomMoveStrategy()
        strategy2 = RandomMoveStrategy()

        player1 = Player("white", ["A", "B"], strategy1)
        player2 = Player("blue", ["Y", "Z"], strategy2)
        players = [player1, player2]

        game_manager = GameManager(board, players)
        game_manager.preset_board()
        game_manager.play()

        play_again = input("Play again?\n")
        if play_again.lower() != 'yes':
            break


if __name__ == "__main__":
    main()