# Sudoku Solving functions

def is_possible(grid: list[list[int]], row: int, col: int, n: int) -> bool:
    '''Checks if an integer 'n' [1 - 9]
    can be placed in a particular grid cell.

    Returns True if 'n' can be placed in the grid
    at position (row, col).'''
    for i in range(9):
        if grid[row][i] == n and i != col:
            return False

    for i in range(9):
        if grid[i][col] == n and i != row:
            return False

    x0 = (col//3)*3
    y0 = (row//3)*3
    for i in range(3):
        for j in range(3):
            if grid[y0+i][x0+j] == n and (y0+i, x0+j) != (row, col):
                return False

    return True


def validate(grid: list[list[int]]) -> None:
    '''Checks if a valid board is set.
    For a set number it checks to see it is repeated in its own row,
    column or block.
    For an empty cell it checks that at least one value is possible to be set.
    An Assertion Error if either of these conditions are violated
    '''
    for row in range(9):
        for col in range(9):
            if grid[row][col] != 0:
                n = grid[row][col]
                grid[row][col] = 0
                assert is_possible(grid, row, col, n), f"Invalid Grid! bad value at {row}, {col}"
                grid[row][col] = n
            else:
                any_number_possible = False
                for n in range(10):
                    any_number_possible |= is_possible(grid, row, col, n)
                assert any_number_possible, f"Invalid Grid! No valid value possible {row}, {col}"


def find_empty(grid):
    '''Function that returns the (row, col) values of the
    earliest encountered empty cell present in the grid'''
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                return row, col
    return None


def solve(grid) -> bool:
    '''Function with a conditional recursive call.

    It iterates over each empty cell to evaluate its possible value
    and places the lowest value (using the is_possible
    function) in the cell and moves to the next cell.

    If a conflict arises i.e no value is possible in a particular
    cell, then it returns out of one recursive level (back-tracks)
    to try out the next possible value. This function implements
    trial-error back-tracking.

    The Function terminates when all cells are filled'''
    cell_pos = find_empty(grid)

    if cell_pos is None:
        return True

    row, col = cell_pos

    for n in range(1, 10):
        if is_possible(grid, row, col, n):
            grid[row][col] = n

            if solve(grid):
                return True

            grid[row][col] = 0

    return False
