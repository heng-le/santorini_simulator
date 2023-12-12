from adapter import DirectionAdapter
from memento import Memento
import copy
class GameManager:

    def __init__(self, board, players, undo_redo = 'off', score_display = 'off'):
        self.board = board
        self.players = players
        self.current_player_index = 0
        self.turn_count = 1
        self._undo = undo_redo
        self._score = score_display
        self.history_manager = HistoryManager()

    def next_turn(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)

    def play(self):
        game_over = False
        while not game_over:
            self.save_state()
            current_player = self.players[self.current_player_index]
            self.board.render()
            height_score, center_score, distance_score = current_player.get_score(self)
            if self._score == 'on':
                print(f"Turn: {self.turn_count}, {current_player.name} ({''.join([workers for workers in current_player.get_workers()])}), ({height_score}, {center_score}, {distance_score})")
            else:
                print(f"Turn: {self.turn_count}, {current_player.name} ({''.join([workers for workers in current_player.get_workers()])})")

            

            winner = self.check_win_condition()
            if not winner:
                winner = self.check_no_valid_moves(current_player)

                if self._undo == 'on':
                    user_choice = input("undo, redo, or next\n").strip().lower()
                    while user_choice not in ['undo','next','redo']:
                        user_choice = input("undo, redo, or next\n").strip().lower()
                    if user_choice == "undo":
                        self.undo_move()
                        continue  
                    elif user_choice == "redo":
                        self.redo_move()
                        continue  

            if winner:
                print(f"{winner} has won")
                game_over = True
                break

            # Handle move
            worker_symbol, move_direction = current_player.make_move(self)
            current_row, current_col = current_player.get_workers()[worker_symbol]
            new_row, new_col = DirectionAdapter.to_new_position(current_row, current_col, move_direction)
            current_player.move_worker(self.board, worker_symbol, move_direction)
            height_score, center_score, distance_score = current_player.get_score(self)
            # Handle build
            build_direction = current_player.make_build(self, new_row, new_col)
            current_player.build(self.board, worker_symbol, build_direction)

            if self._score == 'on':
                print(f"{worker_symbol},{move_direction},{build_direction} ({height_score}, {center_score}, {distance_score})")
            else:
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
        self.players[0].place_worker(self.board, "A", 3, 1)
        self.players[0].place_worker(self.board, "B", 1, 3)
        self.players[1].place_worker(self.board, "Y", 1, 1)
        self.players[1].place_worker(self.board, "Z", 3, 3)

    # undo/redo functionality 

    def save_state(self):
        state = self.create_game_snapshot()
        memento = Memento(*state)
        self.history_manager.save_state(memento)

    def create_game_snapshot(self):
        board_copy = copy.deepcopy(self.board)
        return board_copy, self.turn_count, self.current_player_index

    def restore_state(self, memento):
        self.board, self.turn_count, self.current_player_index = memento.get_state()

    def undo_move(self):
        memento = self.history_manager.undo()
        if memento:
            self.restore_state(memento)

    def redo_move(self):
        memento = self.history_manager.redo()
        if memento:
            self.restore_state(memento)


class HistoryManager:
    def __init__(self):
        self.history = []  
        self.future = []   

    def save_state(self, memento):
        self.history.append(memento)
        self.future.clear() 

    def undo(self):
        if self.history:
            memento = self.history.pop()
            self.future.append(memento)
            return memento
        return None

    def redo(self):
        if self.future:
            memento = self.future.pop()
            self.history.append(memento)
            return memento
        return None
