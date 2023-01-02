from config.settings import BOARD

from .solver import solve, validate


class UserBoardGenerator:
    def __init__(self) -> None:
        self.unsolved = BOARD
        self.solved = [[cell for cell in row] for row in BOARD]

    def generate(self, _) -> None:
        validate(self.unsolved)
        solve(self.solved)
