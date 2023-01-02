import pygame
from pygame import Surface

from config.colors import *


class Cell:
    def __init__(self, value: int, row: int, col: int, size) -> None:
        self.value = value
        self.row = row
        self.col = col
        self.temp: int = 0
        self.size = size

    def draw(self) -> None:
        '''Method to render the value / temp in different fonts
        at location given by its row and col'''
        fnt = pygame.font.SysFont("comicsans", int(0.7 * self.size))
        tmp_fnt = pygame.font.SysFont("comicsans", int(0.45 * self.size))

        window = pygame.display.get_surface()

        x: int = self.col * self.size
        y: int = self.row * self.size

        if self.temp != 0 and self.value == 0:
            number: Surface = tmp_fnt.render(str(self.temp), True, TEMP_COLOR)
            window.blit(number, (x + self.size//8, y))
        elif self.value != 0:
            number: Surface = fnt.render(str(self.value), True, NUM_COLOR)
            window.blit(number, ((x + (self.size/2 - number.get_width()/2)),
                        (y + (self.size/2 - number.get_height()/2))))


    def __eq__(self, val: int) -> bool:
        '''Returns self.value == val'''
        return self.value == val

    def __ne__(self, val: int) -> bool:
        '''Returns self.value != val'''
        return self.value != val
