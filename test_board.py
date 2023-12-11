from cell import Cell
from board import Board 

def test_initial_level():
    cell = Cell(0, 0)
    assert cell.level == 0, "Initial level should be 0"

def test_update_level():
    cell = Cell(0, 0)
    for _ in range(4):
        cell.build_level()
    assert cell.level == 4, "Level should be 4 after 4 updates"
    assert not cell.build_level(), "Level should not increase beyond 4"

def test_initial_occupant():
    cell = Cell(0, 0)
    assert cell.occupant is None, "Initial occupant should be None"

def test_update_occupant():
    cell = Cell(0, 0)
    cell.update_occupant("Player1")
    assert cell.occupant == "Player1", "Occupant should be 'Player1'"
    cell.update_occupant(None)
    assert cell.occupant is None, "Occupant should be None after update"

def test_board_initialization():
    board_size = 5
    board = Board(board_size)
    for row in range(board_size):
        for col in range(board_size):
            cell = board.get_cell(row, col)
            assert isinstance(cell, Cell), "Board should be initialized with Cell objects"
            assert cell.row == row, f"Cell at ({row}, {col}) should have row {row}"
            assert cell.col == col, f"Cell at ({row}, {col}) should have column {col}"
            assert cell.level == 0, f"Cell at ({row}, {col}) should have level 0"
            assert cell.occupant is None, f"Cell at ({row}, {col}) should have no occupant"
