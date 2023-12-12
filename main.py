from board import Board
from player import Player
from game import GameManager
from strategy import HumanMoveStrategy, RandomMoveStrategy

def main():
    board = Board()

    strategy1 = HumanMoveStrategy()
    strategy2 = HumanMoveStrategy()

    player1 = Player("white", ["A", "B"], strategy1)
    player2 = Player("blue", ["Y", "Z"], strategy2)
    players = [player1, player2]

    game_manager = GameManager(board, players)
    game_manager.preset_board()
    game_manager.play()


if __name__ == "__main__":
    main()