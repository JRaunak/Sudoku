import pygame.draw

from config.colors import *
from .sudoku_cell import Cell


class Grid:
    '''A class to enclose the cells in a grid of generated sudoku board'''

    def __init__(self, boards, width: int, height: int, size: int) -> None:
        '''Initializes the Board generator to generate a random
        9 X 9 grid of sudoku and assigns it to self.board.
        self.cells is initialised with the corresponding values
        of self.board

        :difficulty: is a parameter ranging from 0 - 3, which is fed into the
        Board Generator to generate an easy or hard board accordingly'''
        solved, unsolved = boards

        self.solution: list[list[int]] = solved
        self.grid: list[list[int]] = unsolved
        self.cells: list[list[Cell]] = [
            [Cell(self.grid[row][col], row, col, size) for col in range(9)]
            for row in range(9)]
        self.width = width
        self.height = height
        self.size = size

    def draw(self) -> None:
        '''Draws the Grid Lines and the cells along with the values
        associated with them'''
        window = pygame.display.get_surface()

        for i in range(10):
            t = 1
            if i % 3 == 0:
                t = 3
            pygame.draw.line(window, GRID_COLOR, (i*self.size, 0),
                             (i*self.size, self.width), t)
        for i in range(10):
            t = 1
            if i % 3 == 0:
                t = 3
            pygame.draw.line(window, GRID_COLOR, (0, i*self.size),
                             (self.width, i*self.size), t)

        for row in range(9):
            for col in range(9):
                self.cells[row][col].draw()

    def is_finished(self) -> bool:
        '''Checks whether the grid is complete, i.e. the puzzle is solved'''
        for row in range(9):
            for col in range(9):
                if self.cells[row][col].value == 0:
                    return False
        return True
