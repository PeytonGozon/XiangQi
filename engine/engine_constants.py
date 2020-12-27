import numpy as np
import engine_util

N_FILES = 9
N_RANKS = 10
BIT_BOARD_WIDTH = N_FILES * N_RANKS

DEFAULT_BOARD_STATE = np.array([
            ['r', 'h', 'e', 'a', 'g', 'a', 'e', 'h', 'r'],
            ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', 'c', '.', '.', '.', '.', '.', 'c', '.'],
            ['p', '.', 'p', '.', 'p', '.', 'p', '.', 'p'],
            ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['P', '.', 'P', '.', 'P', '.', 'P', '.', 'P'],
            ['.', 'C', '.', '.', '.', '.', '.', 'C', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['R', 'H', 'E', 'A', 'G', 'A', 'E', 'H', 'R'],
        ])

# Due to the backwards implementation of positions in this engine, rank 9 is actually the first location.
RANK_9 = int('1'*N_FILES + '0' * N_FILES * (N_RANKS - 1), 2)
RANK_8 = int('1'*N_FILES + '0' * N_FILES * (N_RANKS - 2), 2)
RANK_7 = int('1'*N_FILES + '0' * N_FILES * (N_RANKS - 3), 2)
RANK_6 = int('1'*N_FILES + '0' * N_FILES * (N_RANKS - 4), 2)
RANK_5 = int('1'*N_FILES + '0' * N_FILES * (N_RANKS - 5), 2)
RANK_4 = int('1'*N_FILES + '0' * N_FILES * (N_RANKS - 6), 2)
RANK_3 = int('1'*N_FILES + '0' * N_FILES * (N_RANKS - 7), 2)
RANK_2 = int('1'*N_FILES + '0' * N_FILES * (N_RANKS - 8), 2)
RANK_1 = int('1'*N_FILES, 2)

BLACK_PALACE_LOCATIONS = [
    (3, 0), (4, 0), (5, 0),
    (3, 1), (4, 1), (5, 1),
    (3, 2), (4, 2), (5, 2)
]

RED_PALACE_LOCATIONS = [
    (3,  8), (4,  8), (5,  8),
    (3,  9), (4,  9), (5,  9),
    (3, 10), (4, 10), (5, 10)
]

BLACK_PALACE_BITBOARD = engine_util.locations_to_bitboard(BLACK_PALACE_LOCATIONS)
