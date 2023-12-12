from adapter import DirectionAdapter
from strategy import MoveStrategy
class Player:
    def __init__(self, name, worker_symbols, strategy):
        self.name = name
        self._workers = {symbol: None for symbol in worker_symbols}  
        self._strategy = strategy
    
    def player_strategy(self):
        return self._strategy

    def place_worker(self, board, worker_symbol, row, col):
        if worker_symbol in self._workers and board.get_cell(row, col).occupant is None:
            board.get_cell(row, col).occupant = worker_symbol
            self._workers[worker_symbol] = (row, col)
            return True
        return False

    def move_worker(self, board, worker_symbol, direction):
        if worker_symbol in self._workers:
            current_row, current_col = self._workers[worker_symbol]
            new_row, new_col = DirectionAdapter.to_new_position(current_row, current_col, direction)
            if self.is_valid_move(board, current_row, current_col, new_row, new_col):
                board.get_cell(current_row, current_col).occupant = None
                board.get_cell(new_row, new_col).occupant = worker_symbol
                self._workers[worker_symbol] = (new_row, new_col)
                return True
        return False
    
    def get_workers(self):
        return self._workers
    
    def build(self, board, worker_symbol, direction):
        if worker_symbol in self._workers:
            current_row, current_col = self._workers[worker_symbol]
            build_row, build_col = DirectionAdapter.to_new_position(current_row, current_col, direction)
            if self.is_valid_build(board, build_row, build_col):
                return board.get_cell(build_row, build_col).build_level()
        return False


    def is_valid_move(self, board, current_row, current_col, new_row, new_col):
        if new_row < 0 or new_row >= board.size or new_col < 0 or new_col >= board.size:
            return False
        if board.get_cell(new_row, new_col).occupant is not None:
            return False
        current_cell = board.get_cell(current_row, current_col)
        destination_cell = board.get_cell(new_row, new_col)
        if destination_cell.level > current_cell.level + 1:
            return False
        return True
    
    def is_valid_build(self, board, row, col):
        if row < 0 or row >= board.size or col < 0 or col >= board.size:
            return False
        if board.get_cell(row, col).occupant is not None:
            return False
        if board.get_cell(row, col).level >= 4:
            return False
        return True
    
    def make_move(self, game_manager):
        return self._strategy.choose_move(game_manager, self)
    
    def make_build(self, game_manager, new_row, new_col):
        return self._strategy.choose_build(game_manager, self, new_row, new_col)


class ComputerPlayer(Player):
    def __init__(self, strategy: MoveStrategy):
        self.strategy = strategy

    def make_move(self, game_state):
        move = self.strategy.choose_move(game_state)
        print(f"Computer chose move: {move}")
        # Execute the move

