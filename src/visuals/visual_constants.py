from pygame import Rect, Surface, SRCALPHA
from engine.engine_constants import N_RANKS, N_FILES

# Scale of all UI components, Refresh Rate (30 Hz)
SCALE = 1
FPS = 30

# The width and height of the game window
WINDOW_WIDTH = 800*SCALE
WINDOW_HEIGHT = 800*SCALE

# The visual padding for the outer game board
HORIZONTAL_PADDING = 100*SCALE
VERTICAL_PADDING = 50*SCALE

# The size of each tile
VERTICAL_TILE_SIZE = (WINDOW_HEIGHT - 2 * VERTICAL_PADDING) / (N_RANKS - 1)
HORIZONTAL_TILE_SIZE = (WINDOW_WIDTH - 2 * HORIZONTAL_PADDING) / (N_FILES - 1)

# The board's rectangle
BOARD_LEFT = HORIZONTAL_PADDING
BOARD_WIDTH = WINDOW_WIDTH-2*HORIZONTAL_PADDING
BOARD_TOP = VERTICAL_PADDING
BOARD_HEIGHT = WINDOW_HEIGHT-2*VERTICAL_PADDING

GAME_BOARD_RECTANGLE = Rect(BOARD_LEFT, BOARD_TOP, BOARD_WIDTH, BOARD_HEIGHT)

# Line thickness
OUTER_LINE_THICKNESS = 5*SCALE
INNER_LINE_THICKNESS = 5*SCALE

# Colors
LINE_COLOR = (0, 0, 0)
BACKGROUND_COLOR = (255, 165, 0)
PIECE_COLOR = (128, 128, 128)
RED_TEXT = (255, 0, 0)
BLACK_TEXT = (0, 0, 0)
POTENTIAL_COLOR = (0, 255, 0, 128)

# Piece properties
PIECE_RADIUS = SCALE*25
POTENTIAL_LOCATION_SURF = Surface((2*PIECE_RADIUS, 2*PIECE_RADIUS), SRCALPHA)

# Convert a piece class into its correct text
PIECE_CLASS_TO_TEXT = {
    'r': ('车', 'b'),
    'h': ('马', 'b'),
    'e': ('象', 'b'),
    'a': ('仕', 'b'),
    'g': ('将', 'b'),
    'c': ('炮', 'b'),
    'p': ('卒', 'b'),
    'R': ('车', 'r'),
    'H': ('马', 'r'),
    'E': ('相', 'r'),
    'A': ('士', 'r'),
    'G': ('帅', 'r'),
    'C': ('炮', 'r'),
    'P': ('兵', 'r'),
}
