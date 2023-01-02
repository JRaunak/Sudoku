import random
from .solver import find_empty, is_possible


class BoardGenerator():
    def __init__(self) -> None:
        self.solved = [[0 for _ in range(9)] for _ in range(9)]
        self.unsolved = None
        self.boards = None

    def __difficulty_translator(self, difficulty):
        extreme_open = [i for i in range(41, 46)]
        hard_open = [i for i in range(31, 41)]
        med_open = [i for i in range(21, 31)]
        easy_open = [i for i in range(11, 21)]

        if difficulty is None:
            difficulty = random.randint(0, 3)
        print(f'========== Difficulty: {difficulty} ==========')
        self.difficulty = difficulty
        diff = [easy_open, med_open, hard_open, extreme_open][difficulty]
        num_open = random.choice(diff)

        return num_open

    def solve(self) -> bool:
        cell_pos = find_empty(self.solved)
        if not cell_pos:
            return True

        row, col = cell_pos

        lst = list(range(1, 10))
        random.shuffle(lst)
        for n in lst:
            if is_possible(self.solved, row, col, n):
                self.solved[row][col] = n
                if self.solve():
                    return True

                self.solved[row][col] = 0

        return False

    def unsolve(self, difficulty) -> None:

        self.unsolved = [[n for n in row] for row in self.solved]
        num_open = self.__difficulty_translator(difficulty)
        while num_open > 0:
            row, col = random.randint(0, 8), random.randint(0, 8)
            if self.unsolved[row][col]:
                self.unsolved[row][col] = 0
                num_open -= 1

    def generate(self, difficulty: int = None) -> None:
        self.solve()
        self.unsolve(difficulty)
        self.boards = self.unsolved, self.solved

    def show(self) -> None:
        print()
        for row in self.unsolved:
            print(row)


if __name__ == '__main__':
    gen = BoardGenerator()
    gen.generate()
    gen.show()
