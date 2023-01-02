# Type Aliasing
Color = tuple[int, int, int]
'''A tuple of R G B values.'''

# Color Value Assignments

BLACK: Color = (0, 0, 0)
'''(0, 0, 0)'''
WHITE: Color = (255, 255, 255)
'''(255, 255, 255)'''
GRAY: Color = (128, 128, 128)
'''(128, 128, 128)'''
RED: Color = (216, 40, 40)
'''(216, 40, 40)'''
GREEN: Color = (40, 216, 40)
'''(40, 216, 40)'''
PURPLE: Color = (100, 50, 200)
'''(100, 50, 200)'''
CYAN: Color = (0, 200, 180)
'''(0, 200, 180)'''

# Colors for Each cell
TEMP_COLOR = GRAY
NUM_COLOR = BLACK
SELECT_COLOR = CYAN

# Algorithm Colors
ALGO_CURSOR_COLOR = PURPLE
BACK_TRACK_COLOR = RED

# Info Colors
TIMER_COLOR = BLACK
CTRL_COLOR = GREEN
STRIKE_COLOR = RED

# Grid Color
BG_COLOR = WHITE
GRID_COLOR = BLACK
