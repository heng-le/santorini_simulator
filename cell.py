class Cell():
    '''
    Represents each cell on the board in Santorini game. 
    Keeps track of building level, coordinates of cell, and occupancy.
    '''

    def __init__(self, row, col):
        self._row, self._col = row, col
        self.level = 0
        self.occupant = None

    def build_level(self):
        '''
        Increases the level of the building by 1, to a maximum of 4.
        Returns:
            success (bool): True if level was increased, False otherwise.
        '''
        if self.level < 4:
            self.level += 1
            return True
        else:
            return False
        

    def update_occupant(self, new_occupant=None):
        '''
        Updates the occupant of the cell.

        '''
        if new_occupant is None or self.occupant is None:
            self.occupant = new_occupant
            return True
        
        else:
            return False
        

    def __str__(self):
        """
        Returns a string representation of each cell. 
        The Rows and Columns are 1-indexed rather than 0-indexed.  
        """
        return f"Cell({self._row + 1}, {self._col + 1}, Level: {self.level}, Occupant: {self.occupant})"