from adapter import DirectionAdapter
class GameManager:

    def __init__(self, board, players):
        self._board = board
        self._players = players
        self._current_player_index = 0
        self._turn_count = 0

    def next_turn(self):
        self._current_player_index = (self._current_player_index + 1) % len(self._players)

    def play(self):
        while not self.is_game_over():
            current_player = self._players[self._current_player_index]
            self._board.render()
            print(f"Turn: {self._turn_count}, {current_player.name} ({''.join([workers for workers in current_player.get_workers()])})")

            worker_symbol = self.get_worker_input(current_player)
            move_direction = self.get_direction_input("move")
            build_direction = self.get_direction_input("build")

            current_player.move_worker(self._board, worker_symbol, move_direction)
            current_player.build(self._board, worker_symbol, build_direction)

            print(f"{worker_symbol},{move_direction},{build_direction}")

            self.next_turn()

    def get_worker_input(self, player):
        valid = False
        while not valid:
            worker_symbol = input("Select a worker to move: ")
            if worker_symbol in player.get_workers():
                valid = True
            elif any(worker_symbol in player.get_workers() for player in self._players if player != player):
                print("That is not your worker")
            else:
                print("Not a valid worker")
        return worker_symbol

    def get_direction_input(self, action_type):
        valid_directions = ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']
        valid = False
        while not valid:
            direction = input(f"Select a direction to {action_type} (n, ne, e, se, s, sw, w, nw): ")
            if direction in valid_directions:
                valid = True
            else:
                print("Not a valid direction")
        return direction

    def is_game_over(self):
        if self.check_win_condition():
            return True

        if self.check_no_valid_moves(self._players[self._current_player_index]):
            return True

        return False

    def check_win_condition(self):
        for row in range(self._board.size):
            for col in range(self._board.size):
                cell = self._board.get_cell(row, col)
                if cell.level == 3 and cell.occupant is not None:
                    for player in self._players:
                        if cell.occupant in player.get_workers():
                            print(f"{player.name} has won")
                            return True
        return False

    def check_no_valid_moves(self, player):
        for worker_symbol in player.get_workers().keys():
            if self.can_worker_move_or_build(player, worker_symbol):
                return False
        print(f"{player.name} cannot move or build, they lose")
        return True
    
    def can_worker_move_or_build(self, player, worker_symbol):
        current_row, current_col = player.get_workers()[worker_symbol]
        directions = ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']
        for direction in directions:
            new_row, new_col = DirectionAdapter.to_new_position(current_row, current_col, direction)
            if player.is_valid_move(self._board, current_row, current_col, new_row, new_col):
                return True
            if player.is_valid_build(self._board, new_row, new_col): 
                return True
        return False



