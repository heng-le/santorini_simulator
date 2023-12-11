from board import Board
from player import Player
from game import GameManager
def main():
    board = Board()

    player1 = Player("white", ["A", "B"])
    player2 = Player("blue", ["Y", "Z"])
    players = [player1, player2]

    game_manager = GameManager(board, players)
    game_manager.preset_board()
    game_manager.play()

if __name__ == "__main__":
    main()