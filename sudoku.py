import time

import pygame
from pygame.surface import Surface

from config.colors import *
from config.settings import *
from helper import ControlMode as Mode
from helper import convert, format_time, highlight_cell
from logic.board_generator import BoardGenerator
from logic.solver import find_empty, is_possible
from logic.user_board import UserBoardGenerator
from ui.sudoku_grid import Grid


class Sudoku:
    '''The main game class that handles initialization of pygame and
    other relevant data'''

    def __init__(self) -> None:
        self.width = WIDTH
        self.height = HEIGHT
        self.size = SIZE
        self.clock = pygame.time.Clock()
        if BOARD_PROVIDED:
            self.board_generator = UserBoardGenerator()
        else:
            self.board_generator = BoardGenerator()

        pygame.init()
        pygame.font.init()
        self.window = pygame.display.set_mode(
            (self.width, self.height))
        pygame.display.set_caption("Sudoku")

    def init(self, difficulty: int = None) -> None:
        '''Method to initialize the mutable parts of the code providing
        the ability to restart the game'''
        self.difficulty = difficulty
        self.strikes: int = 0
        self.key: int = 0
        self.running: bool = True
        self.selected: tuple[int, int] | None = None

        self.board_generator.generate(difficulty)
        boards = self.board_generator.solved, self.board_generator.unsolved

        self.board = Grid(boards, self.width, self.height, self.size)

    def select(self, row: int, col: int) -> None:
        '''Method to select and focus on a particular cell on the grid'''
        if row > 8:
            return
        for r in range(9):
            for c in range(9):
                self.board.cells[r][c].selected = False

        self.selected = (row, col)

    def trial(self, temp: int) -> None:
        '''Method to set the temp value of the selected cell'''
        row, col = self.selected
        self.board.cells[row][col].temp = temp

    def clear_cell(self) -> None:
        '''Clears the temp value stored in the selected cell'''
        row, col = self.selected
        if self.board.cells[row][col].value == 0:
            self.board.cells[row][col].set_temp(0)

    def place(self, value: int) -> bool:
        '''Places the temp value of a cell as its permanent value, then
        matches with the solution if the placing of number was a valid move.
        If it is validated, the permanent value is updated in
        self.board.cells otherwise the values are cleared from temp
        and the value of :self.strikes: is incremented by 1'''
        row, col = self.selected

        if self.board.cells[row][col].value == 0:
            if value == self.board.solution[row][col]:
                self.board.cells[row][col].value = value
                return True
            else:
                self.board.cells[row][col].temp = 0
        return False

    def draw(self, time: int, mode: Mode):
        '''Calls the the draw() methods of all classes and blits some text like
        :time:, :player_name: and no. of :strikes: onto the window'''
        self.window.fill(BG_COLOR)

        fnt = pygame.font.SysFont("comicsans", int(0.3 * self.size))
        Timer: Surface = fnt.render(
            f'Time: {format_time(time)}', True, TIMER_COLOR)
        self.window.blit(Timer, (int(0.25 * self.size),
                         self.width + int(0.1 * self.size)))

        Player: Surface = fnt.render(f'{mode.name}', True, CTRL_COLOR)
        self.window.blit(Player, (int(3.75 * self.size),
                         self.width + int(0.1 * self.size)))

        Strikes: Surface = fnt.render('X '*self.strikes, True, STRIKE_COLOR)
        self.window.blit(Strikes, (6.75 * self.size,
                         self.width + int(0.1 * self.size)))

        if self.selected is not None:
            highlight_cell(self.selected, SELECT_COLOR)

        self.board.draw()

        pygame.display.update()

    def auto_solve(self, start_time: int) -> bool:
        '''Wrapper for the recursive function algo_solve().
        Also initialises the algorithm Clock and
        calls the inner function'''

        self.selected = None
        algo_clock: pygame.time.Clock = pygame.time.Clock()

        def algo_solve(board: Grid) -> bool:
            '''Function with a conditional recursive call.

            It iterates over each empty cell ( using find_empty() ) to evaluate
            its possible values ( using is_possible() ) and places the
            lowest value in the cell and moves to the next cell.

            If a conflict arises i.e no value is possible in a particular
            cell, then it returns out of one recursive level (back-tracks)
            to try out the next possible value. This function implements
            trial-error back-tracking.

            The function comes out of all recursive levels when all cells are
            filled i.e find_empty() returns None'''
            algo_clock.tick(ALGO_FPS)

            # Event loop to terminte the AI and the program
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True

            time_by_algo: int = round(time.time() - start_time)
            self.draw(time_by_algo, mode=Mode.ALGORITHM)

            cell_pos = find_empty(board.cells)

            if cell_pos is None:
                return True

            row, col = cell_pos

            for n in range(1, 10):
                if is_possible(board.cells, row, col, n):
                    board.cells[row][col].value = n

                    highlight_cell((row, col), ALGO_CURSOR_COLOR)
                    pygame.display.update()

                    if algo_solve(board):
                        return True

                    board.cells[row][col].value = 0

            highlight_cell((row, col), BACK_TRACK_COLOR)

            return False

        return algo_solve(self.board)

    def run(self, fps: int) -> None:
        '''It contains the main game loop with all the input detection
        and method calling'''

        start_time: int = time.time()

        while self.running:
            self.clock.tick(fps)
            play_time = round(time.time() - start_time)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    clicked_at = convert(pygame.mouse.get_pos())

                    # Mouse cursor is clicked inside the sudoku grid
                    if clicked_at is not None:
                        self.select(*clicked_at)
                        self.key = None

                    if self.board.is_finished():
                        self.running = False

                if event.type == pygame.KEYDOWN:
                    match event.key:
                        case pygame.K_1:
                            self.key = 1
                        case pygame.K_2:
                            self.key = 2
                        case pygame.K_3:
                            self.key = 3
                        case pygame.K_4:
                            self.key = 4
                        case pygame.K_5:
                            self.key = 5
                        case pygame.K_6:
                            self.key = 6
                        case pygame.K_7:
                            self.key = 7
                        case pygame.K_8:
                            self.key = 8
                        case pygame.K_9:
                            self.key = 9

                        case pygame.K_BACKSPACE:
                            self.clear_cell()
                            self.key = None

                        # To reset and restart the game ( calling self.init() )
                        case pygame.K_r:
                            self.init(self.difficulty)

                        # To start the back-tracking algorithm
                        case pygame.K_SPACE:

                            ai_start_time: int = time.time()

                            self.auto_solve(ai_start_time)

                            if self.board.is_finished():
                                print(f"Algorithm completed in {round(time.time() - ai_start_time)} seconds")
                            else:
                                print(f"Algorithm Terminated")
                                self.running = False

                        # To confirm a value in a cell
                        case pygame.K_RETURN:
                            r, c = self.selected
                            if self.board.cells[r][c].temp != 0:
                                num_placed = self.place(
                                    self.board.cells[r][c].temp)

                                if not num_placed:
                                    self.strikes += 1

                                self.key = None
                                if self.board.is_finished():
                                    print(f"You completed in {round(time.time() - start_time)} seconds")

            if self.selected and self.key is not None:
                self.trial(self.key)

            self.draw(play_time, mode=Mode.PLAYER)

    def quit(self) -> None:
        '''A wrapper function to quit pygame'''
        pygame.quit()
