import argparse
from board import Board
from player import Player
from game import GameManager
from strategy import HumanMoveStrategy, RandomMoveStrategy, HeuristicMoveStrategy

def main():
    parser = argparse.ArgumentParser(description="Configure the Santorini game settings.")
    parser.add_argument("white_player_type", nargs='?', default="human", 
                        choices=["human", "heuristic", "random"],
                        help="Type of the white player: human, heuristic, or random")
    parser.add_argument("blue_player_type", nargs='?', default="human", 
                        choices=["human", "heuristic", "random"],
                        help="Type of the blue player: human, heuristic, or random")
    parser.add_argument("undo_redo", nargs='?', default="off", 
                        choices=["on", "off"],
                        help="Enable or disable undo/redo functionality")
    parser.add_argument("score_display", nargs='?', default="off", 
                        choices=["on", "off"],
                        help="Enable or disable score display")
    
    args = parser.parse_args()

    strategy_map = {
        "human": HumanMoveStrategy(),
        "random": RandomMoveStrategy(),
        "heuristic": HeuristicMoveStrategy()
    }

    white_strategy = strategy_map[args.white_player_type]
    blue_strategy = strategy_map[args.blue_player_type]

    while True: 
        board = Board()
        player1 = Player("white", ["A", "B"], white_strategy)
        player2 = Player("blue", ["Y", "Z"], blue_strategy)
        players = [player1, player2]

        # Initialize GameManager with undo/redo and score display settings
        game_manager = GameManager(board, players, undo_redo=args.undo_redo, score_display=args.score_display)

        game_manager.preset_board()
        game_manager.play()
        play_again = input("Play again?\n")
        
        if play_again.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
