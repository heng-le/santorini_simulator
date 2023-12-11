class DirectionAdapter:
    @staticmethod
    def to_new_position(current_row, current_col, direction):
        direction_mapping = {
            'n': (-1, 0), 'ne': (-1, 1), 'e': (0, 1), 'se': (1, 1),
            's': (1, 0), 'sw': (1, -1), 'w': (0, -1), 'nw': (-1, -1)
        }
        row_change, col_change = direction_mapping.get(direction, (0, 0))
        new_row = current_row + row_change
        new_col = current_col + col_change
        return new_row, new_col