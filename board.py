from cell import Cell 
class Board():
    def __init__(self, size=5):
        """
        Initializes the board with individual Cells.
        """
        self.size = size
        self._board = [[Cell(row, col) for col in range(size)] for row in range(size)]

    def get_cell(self, row, col):
        return self._board[row][col]
    
    def render(self):
        """
        Prints out a string representation of the board state. 
        """
        for row in self._board:
            print('+--' * self.size + '+')
            print('|' + '|'.join(f'{str(cell.level) + cell.occupant if cell.occupant else cell.level:<2}' for cell in row) + '|')
        print('+--' * self.size + '+')



