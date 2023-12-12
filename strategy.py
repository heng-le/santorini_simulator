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
    
    def calculate_distance_score(self, game_manager, player, current_row, current_col):

        total_min_distance = 0
        opponent_workers = [worker_pos for opponent in game_manager.players if opponent != player
                            for worker_pos in opponent.get_workers().values()]

        min_distance = min(self.chebyshev_distance((current_row, current_col), opponent_pos) 
                           for opponent_pos in opponent_workers)
        total_min_distance += min_distance

        return total_min_distance
    

    @staticmethod
    def chebyshev_distance(pos1, pos2):
        return max(abs(pos1[0] - pos2[0]), abs(pos1[1] - pos2[1]))
        

    def calculate_center_score(self, row, col):
        center = (2, 2)  
        ring = [(2, 1), (2, 3), (1, 2), (3, 2), (1, 1), (1, 3), (3, 1), (3, 3)]

        if (row, col) == center:
            return 2  
        elif (row, col) in ring:
            return 1  
        else:
            return 0  
        
    def calculate_distance_score(self, game_manager, player):
        total_min_distance = 0
        opponent_workers = [worker_pos for opponent in game_manager.players if opponent != player
                            for worker_pos in opponent.get_workers().values()]

        for opponent_pos in opponent_workers:
            min_distance_to_opponent = min(
                self.chebyshev_distance(worker_pos, opponent_pos) 
                for worker_pos in player.get_workers().values()
            )
            total_min_distance += min_distance_to_opponent

        return total_min_distance
    

    def score_move(self, game_manager, player):
        height_score = 0
        center_score = 0
        distance_score = 0

        for worker_symbol, (current_row, current_col) in player.get_workers().items():
            height_score += game_manager.board.get_cell(current_row, current_col).level
            center_score += self.calculate_center_score(current_row, current_col)

        distance_score = self.calculate_distance_score(game_manager, player)

        adjusted_distance_score = 8 - distance_score

        return height_score, center_score, adjusted_distance_score
    

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
            worker_symbol = input("Select a worker to move:\n")

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
            direction = input(f"Select a direction to {action_type} (n, ne, e, se, s, sw, w, nw):\n")
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
    def choose_move(self, game_manager, current_player):
        best_score = -float('inf')
        best_move = None
        valid_directions = ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']

        for worker_symbol in current_player.get_workers().keys():
            current_row, current_col = current_player.get_workers()[worker_symbol]

            for move_direction in valid_directions:
                new_row, new_col = DirectionAdapter.to_new_position(current_row, current_col, move_direction)

                if current_player.is_valid_move(game_manager.board, current_row, current_col, new_row, new_col):
                    current_player.get_workers()[worker_symbol] = (new_row, new_col)
                    height_score, center_score, adjusted_distance_score = self.score_move(game_manager, current_player)

                    if game_manager.board.get_cell(new_row, new_col).level == 3:
                        score = 100000
                    else:
                        score = height_score + center_score + adjusted_distance_score

                    current_player.get_workers()[worker_symbol] = (current_row, current_col)

                    if score > best_score:
                        best_score = score
                        best_move = (worker_symbol, move_direction)

        return best_move if best_move else (None, None)


    def choose_build(self, game_manager, current_player, new_row, new_col):
        build_direction = self.get_valid_build_direction(current_player, game_manager, new_row, new_col)
        return build_direction
    
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
    