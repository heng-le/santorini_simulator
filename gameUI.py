from board import Board 
class GameUI():
    def __init__(self, board):
        self._board = board

    def render(self):
        """
        Prints out a string representation of the board state. 
        """
        for row in self._board:
            print('+--' * self._size + '+')
            print('|' + '|'.join(f'{str(cell.level) + cell.occupant if cell.occupant else cell.level:<2}' for cell in row) + '|')
        print('+--' * self._size + '+')


# board_size = 5
# board = Board(board_size)
# board.render()

