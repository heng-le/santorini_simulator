class Memento:
    def __init__(self, board_state, turn_count, current_player_index,players):
        self.board_state = board_state
        self.turn_count = turn_count
        self.current_player_index = current_player_index
        self.players = players

    def get_state(self):
        return self.board_state, self.turn_count, self.current_player_index, self.players
    
