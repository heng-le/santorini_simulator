from board import Board
from player import Player
from game import GameManager
def main():
    board = Board()

    player1 = Player("white", ["A", "B"])
    player2 = Player("blue", ["Y", "Z"])
    players = [player1, player2]

    game_manager = GameManager(board, players)
    player1.place_worker(board, "A", 1, 3)
    player1.place_worker(board, "B", 3, 1)
    player2.place_worker(board, "Y", 1, 1)
    player2.place_worker(board, "Z", 3, 3)
    game_manager.play()

if __name__ == "__main__":
    main()