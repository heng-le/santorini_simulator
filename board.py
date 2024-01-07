from cell import Cell 
class Board():
    def __init__(self, size=5):
        """
        Initializes the board with individual Cells.
        """
        self.size = size
        self._board = [[Cell(row, col) for col in range(size)] for row in range(size)]

    def __iter__(self):
        return BoardIterator(self)

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

    def reset_game(self):
        self._board = [[Cell(row, col) for col in range(self.size)] for row in range(self.size)]



class BoardIterator:
    def __init__(self, board):
        self._board = board._board 
        self._size = board.size  
        self._current_row = 0
        self._current_col = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._current_row < self._size:
            cell = self._board[self._current_row][self._current_col]
            self._current_col += 1
            if self._current_col == self._size:
                self._current_col = 0
                self._current_row += 1
            return cell
        else:
            raise StopIteration