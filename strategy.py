import random
from adapter import DirectionAdapter
class MoveStrategy:
    def choose_move(self, game_manager, current_player):
        """
        Method to be implemented by concrete strategies.
        It should determine the best move based on the current game state.
        """
        raise NotImplementedError("This method should be implemented by subclasses.")
    
    def choose_build(self, game_manager, current_player, new_row, new_col):
        raise NotImplementedError("This method should be implemented by subclasses.")
    

class HumanMoveStrategy(MoveStrategy):
    def choose_move(self, game_manager, current_player):
        worker_symbol = self.get_worker_input(current_player, game_manager)
        current_row, current_col = current_player.get_workers()[worker_symbol]
        move_direction = self.get_valid_move_direction(current_player, game_manager, current_row, current_col)
        return worker_symbol, move_direction

    def choose_build(self, game_manager, current_player, new_row, new_col):
        build_direction = self.get_valid_build_direction(current_player, game_manager, new_row, new_col)
        return build_direction

    def get_valid_move_direction(self, current_player, game_manager, current_row, current_col):
        while True:
            move_direction = self.get_direction_input("move")
            new_row, new_col = DirectionAdapter.to_new_position(current_row, current_col, move_direction)

            if current_player.is_valid_move(game_manager.board, current_row, current_col, new_row, new_col):
                return move_direction
            else:
                print(f"Cannot move {move_direction}")

    def get_valid_build_direction(self, current_player, game_manager, new_row, new_col):
        while True:
            build_direction = self.get_direction_input("build")
            build_row, build_col = DirectionAdapter.to_new_position(new_row, new_col, build_direction)

            if current_player.is_valid_build(game_manager.board, build_row, build_col):
                return build_direction
            else:
                print(f"Cannot build {build_direction}")


    def get_worker_input(self, current_player, game_manager):
        while True:
            worker_symbol = input("Select a worker to move: ")

            if worker_symbol in current_player.get_workers():
                if game_manager.can_worker_move(current_player, worker_symbol):
                    return worker_symbol
                else:
                    print("That worker cannot move")
            elif any(worker_symbol in other_player.get_workers() for other_player in game_manager.players if other_player != current_player):
                print("That is not your worker")
            else:
                print("Not a valid worker")

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


class RandomMoveStrategy(MoveStrategy):
    def choose_move(self, game_manager, current_player):
        worker_symbol = self.get_worker_input(current_player, game_manager)
        current_row, current_col = current_player.get_workers()[worker_symbol]
        move_direction = self.get_valid_move_direction(current_player, game_manager, current_row, current_col)
        return worker_symbol, move_direction

    def choose_build(self, game_manager, current_player, new_row, new_col):
        build_direction = self.get_valid_build_direction(current_player, game_manager, new_row, new_col)
        return build_direction

    def get_valid_move_direction(self, current_player, game_manager, current_row, current_col):
        while True:
            move_direction = self.get_direction_input("move")
            new_row, new_col = DirectionAdapter.to_new_position(current_row, current_col, move_direction)

            if current_player.is_valid_move(game_manager.board, current_row, current_col, new_row, new_col):
                return move_direction

    def get_valid_build_direction(self, current_player, game_manager, new_row, new_col):
        while True:
            build_direction = self.get_direction_input("build")
            build_row, build_col = DirectionAdapter.to_new_position(new_row, new_col, build_direction)

            if current_player.is_valid_build(game_manager.board, build_row, build_col):
                return build_direction
            

    def get_worker_input(self, current_player, game_manager):
        worker_symbols = list(current_player.get_workers().keys())

        movable_workers = [worker for worker in worker_symbols if game_manager.can_worker_move(current_player, worker)]

        if not movable_workers:
            print("No workers can move")
            return None  
        return random.choice(movable_workers)

    def get_direction_input(self, action_type):
        valid_directions = ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']
        valid = False
        while not valid:
            direction = random.choice(valid_directions)
            if direction in valid_directions:
                valid = True
            else:
                print("Not a valid direction")
        return direction



class HeuristicMoveStrategy(MoveStrategy):
    def choose_move(self, game_state):
        # Implement logic to choose the best move based on the criteria
        pass  # Return the best move based on heuristic criteria

    def choose_build(self, game_manager, current_player, new_row, new_col):
        pass
