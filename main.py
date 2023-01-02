from config.settings import FPS
from sudoku import Sudoku

game = Sudoku()
game.init(2)
game.run(FPS)
game.quit()
