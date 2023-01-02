from enum import Enum, auto

import pygame.draw
from config.colors import Color
from config.settings import *


class ControlMode(Enum):
    ALGORITHM = auto()
    PLAYER = auto()


def highlight_cell(pos: tuple[int, int], color: Color) -> None:
    '''Takes :(row, col): of a cell and highlights it with the :color:'''
    row, col = pos
    pygame.draw.rect(pygame.display.get_surface(), color, (col*SIZE, row*SIZE,
                     SIZE, SIZE), 3, int(0.1 * SIZE))


def convert(pos: tuple[int, int]) -> tuple[int, int] | None:
    '''Verifies if the :pos: was inside the grid and then converts
    the :pos: (x, y) to (row, col) and returns it.

    Returns None otherwise'''

    x, y = pos
    if x < WIDTH and y < HEIGHT:
        row = y // SIZE
        col = x // SIZE
        return row, col
    return None


def format_time(time: int) -> str:
    '''Takes time in seconds as input and formats it in "min : sec" format.'''
    sec = time % 60

    if sec < 10:
        sec = f'0{sec}'

    minute = time//60
    if minute < 10:
        minute = f'0{minute}'

    return f'{minute}:{sec}'
