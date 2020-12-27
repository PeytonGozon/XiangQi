import engine_util
import engine_constants
import bitboard as bb
import numpy as np

"""
This file contains all the valid piece movement functions.
"""


def black_general_valid_movements(bit_boards: bb):
    """
    Given a bit board representation of the game, determine all valid movement options for black pawns.
    :param bit_boards: BitBoard object
    :return: a list containing all valid movement locations.
    """
    # The general may only move in an orthogonal manner in its palace. We therefore construct the grid of it moving in
    # all orthogonal directions. 'g' is the inner representation of the black general.
    general_bitboard = bit_boards['g']
    # Implement side-to-side movement by one place
    potential_locations = (general_bitboard << 1) + (general_bitboard >> 1)

    # Implement up-down movement by one place (only need to change logic if the general is in the 9th rank)
    if general_bitboard & engine_constants.RANK_9 > 0:
        potential_locations += general_bitboard >> engine_constants.N_FILES
    else:
        potential_locations += (general_bitboard >> engine_constants.N_FILES) + \
                               (general_bitboard << engine_constants.N_FILES)

    potential_locations = restrict_movement_by_team(potential_locations, bit_boards, 'b')

    # Restrict the movement to inside the palace
    potential_locations &= engine_constants.BLACK_PALACE_BITBOARD

    # TODO: implement the rule that generals may not look at each other

    return potential_locations


def restrict_movement_by_team(piece_bitboard, bit_boards: bb, team):

    for key in bit_boards:
        if team == 'b' and str.islower(key):
            piece_bitboard &= ~bit_boards[key]
        elif team == 'r' and str.isupper(key):
            piece_bitboard &= ~bit_boards[key]

    return piece_bitboard


def return_valid_moves_by_type(bit_boards: bb, piece_class):
    if piece_class == 'g':
        return black_general_valid_movements(bit_boards)
    return 0
