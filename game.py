from adapter import DirectionAdapter
from board import Board
from player import Player
class GameManager:

    def __init__(self, board, players):
        self.board = board
        self.players = players
        self.current_player_index = 0
        self.turn_count = 1

    def next_turn(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)

    def play(self):
        game_over = False
        while not game_over:
            current_player = self.players[self.current_player_index]
            self.board.render()

            print(f"Turn: {self.turn_count}, {current_player.name} ({''.join([workers for workers in current_player.get_workers()])})")

            winner = self.check_win_condition()
            if not winner:
                winner = self.check_no_valid_moves(current_player)

            if winner:
                print(f"{winner} has won")
                game_over = True
                break 

            # Handle move
            worker_symbol, move_direction = current_player.make_move(self)
            current_row, current_col = current_player.get_workers()[worker_symbol]
            new_row, new_col = DirectionAdapter.to_new_position(current_row, current_col, move_direction)
            current_player.move_worker(self.board, worker_symbol, move_direction)

            # Handle build
            build_direction = current_player.make_build(self, new_row, new_col)
            current_player.build(self.board, worker_symbol, build_direction)

            print(f"{worker_symbol},{move_direction},{build_direction}")

            self.turn_count += 1
            self.next_turn()



    def check_win_condition(self):
        for row in range(self.board.size):
            for col in range(self.board.size):
                cell = self.board.get_cell(row, col)
                if cell.level == 3 and cell.occupant is not None:
                    for player in self.players:
                        if cell.occupant in player.get_workers():
                            return player.name 
        return None 
    

    def check_no_valid_moves(self, player):
        for worker_symbol in player.get_workers().keys():
            if self.can_worker_move(player, worker_symbol):
                return None  
        for opponent in self.players:
            if opponent != player:
                return opponent.name

    
    def can_worker_move(self, player, worker_symbol):
        current_row, current_col = player.get_workers()[worker_symbol]
        directions = ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']
        for direction in directions:
            new_row, new_col = DirectionAdapter.to_new_position(current_row, current_col, direction)
            if player.is_valid_move(self.board, current_row, current_col, new_row, new_col):
                return True
        return False
    

    
    def preset_board(self):
        self.players[0].place_worker(self.board, "A", 1, 3)
        self.players[0].place_worker(self.board, "B", 3, 1)
        self.players[1].place_worker(self.board, "Y", 1, 1)
        self.players[1].place_worker(self.board, "Z", 3, 3)

    # AI-related methods 
    # def play_computer_move(self, computer_moves):
        






# player1 = Player("white", ["A", "B"])
# player2 = Player("blue", ["Y", "Z"])
# players = [player1, player2]
# board = Board()
# game_manager = GameManager(board, players)

# game_manager.get_worker_input(player1)
