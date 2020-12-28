from typing import Union
from .chess_engine import BitBoard
"""
This file contains all the valid piece movement functions.
"""


def black_general_valid_movements(bit_boards: BitBoard):
    """
    Given a bit board representation of the game, determine all valid movement options for the blakc general.
    :param bit_boards: BitBoard object
    :return: a bit board containing all valid movement locations.
    """
    from engine.engine_constants import RANK_9, N_FILES, BLACK_PALACE_BITBOARD
    # The general may only move in an orthogonal manner in its palace. We therefore construct the grid of it moving in
    # all orthogonal directions. 'g' is the inner representation of the black general.
    general_bitboard = bit_boards['g']
    # Implement side-to-side movement by one place
    potential_locations = (general_bitboard << 1) | (general_bitboard >> 1)

    # Implement up-down movement by one place (only need to change logic if the general is in the 9th rank)
    if general_bitboard & RANK_9 > 0:
        potential_locations |= general_bitboard >> N_FILES
    else:
        potential_locations |= (general_bitboard >> N_FILES) | \
                               (general_bitboard << N_FILES)

    potential_locations = restrict_movement_by_team(potential_locations, bit_boards, 'b')

    # Restrict the movement to inside the palace
    potential_locations &= BLACK_PALACE_BITBOARD

    # TODO: implement the rule that generals may not look at each other

    return potential_locations


def black_advisor_valid_movements(bit_boards: Union[BitBoard, int]):
    """
    Given a bit board representation of the game, determine all valid movement options for the blakc general.
    :param bit_boards: BitBoard object
    :return: a bit board containing all valid movement locations.
    """
    from engine.engine_constants import N_FILES, BLACK_PALACE_BITBOARD
    # Advisors only move along the diagonal lines. This means we need to try movement along a right bitshift of
    # N_FILES-1 AND N_FILES+1 (for going down), and a corresponding left bitshift for going up.
    if isinstance(bit_boards, BitBoard):
        advisor_bitboard = bit_boards['a']
    elif isinstance(bit_boards, int):
        advisor_bitboard = bit_boards
    else:
        return 0

    potential_locations = (advisor_bitboard >> N_FILES - 1) | \
                          (advisor_bitboard >> N_FILES + 1)

    # If we're not in the 9th rank, we can move downward too.
    # if advisor_bitboard & engine_constants.RANK_9 == 0:
    potential_locations |= (advisor_bitboard << N_FILES + 1) | \
                           (advisor_bitboard << N_FILES - 1)

    # Ensure that the moves are valid by first checking that they are inside the palace
    potential_locations &= BLACK_PALACE_BITBOARD

    # Then ensure that they are not going on top of another black piece
    potential_locations = restrict_movement_by_team(potential_locations, bit_boards, 'b')

    return potential_locations


def restrict_movement_by_team(piece_bitboard, bit_boards: BitBoard, team):
    """ Ensure that the piece passed in will not be landing on top of a piece from the same team.

    :param piece_bitboard: a integer containing the bitboard representation of some particular piece.
    :param bit_boards: a BitBoard object
    :param team: either 'r' for the red team or 'b' for the black team.
    :return: the updated piece bitboard, after removing all conflicting moves.
    """
    for key in bit_boards:
        if (team == 'r' and str.isupper(key)) or (team == 'b' and str.islower(key)):
            piece_bitboard &= ~bit_boards[key]

    return piece_bitboard


def return_valid_moves_by_type(bit_boards: BitBoard, piece_class):
    if piece_class == 'g':
        return black_general_valid_movements(bit_boards)
    if piece_class == 'a':
        return black_advisor_valid_movements(bit_boards)
    return 0
