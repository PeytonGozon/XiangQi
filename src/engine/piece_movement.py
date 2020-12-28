from typing import Union, Optional
from .chess_engine import BitBoard
from .engine_constants import N_FILES
"""
This file contains all the valid piece movement functions.
"""


def black_general_valid_movements(bit_boards: BitBoard, piece_location: Optional[int] = None):
    """
    Given a bit board representation of the game, determine all valid movement options for the black general.
    :param bit_boards: BitBoard object
    :param piece_location: an integer containing the bitboard of the black general. If not specified, then all viable
    locations are returned.
    :return: a bit board containing all valid movement locations.
    """
    from engine.engine_constants import RANK_9, BLACK_PALACE_BITBOARD
    # The general may only move in an orthogonal manner in its palace. We therefore construct the grid of it moving in
    # all orthogonal directions. 'g' is the inner representation of the black general.
    general_bitboard = piece_location if piece_location is not None else bit_boards['g']
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


def black_adviser_valid_movements(bit_boards: BitBoard, piece_location: Optional[int] = None):
    """
    Given a bit board representation of the game, determine all valid movement options for the black advisers.
    :param bit_boards: BitBoard object
    :param piece_location: an integer containing the bitboard of a black adviser. If not specified, then all viable
    locations are returned.
    :return: a bit board containing all valid movement locations.
    """
    from engine.engine_constants import BLACK_PALACE_BITBOARD
    # Advisers only move along the diagonal lines. This means we need to try movement along a right bitshift of
    # N_FILES-1 AND N_FILES+1 (for going down), and a corresponding left bitshift for going up.
    adviser_bitboard = piece_location if piece_location is not None else bit_boards['a']

    potential_locations = (adviser_bitboard >> N_FILES - 1) | \
                          (adviser_bitboard >> N_FILES + 1)

    # FIXME: strictly enforce the bit limit being less than 90 bits long
    potential_locations |= (adviser_bitboard << N_FILES + 1) | \
                           (adviser_bitboard << N_FILES - 1)

    # Ensure that the moves are valid by first checking that they are inside the palace
    potential_locations &= BLACK_PALACE_BITBOARD

    # Then ensure that they are not going on top of another black piece
    potential_locations = restrict_movement_by_team(potential_locations, bit_boards, 'b')

    return potential_locations


def black_pawn_valid_movements(bit_boards: BitBoard, piece_location: Optional[int] = None):
    """
    Given a bit board representation of the game, determine all valid movement options for the black pawns.
    :param bit_boards: BitBoard object
    :param piece_location: an integer containing the bitboard of a black pawn. If not specified, then all viable
    locations are returned.
    :return: a bit board containing all valid movement locations.
    """
    from .engine_constants import RANK_1, BOTTOM_HALF, FILE_1, FILE_8

    pawn_bitboard = piece_location if piece_location is not None else bit_boards['p']

    # With pawns, there are two types of movement. If the pawn is still on its side of the river, then
    # it may only move forward. However, once it crosses the river, then the piece may move one step either forward,
    # left, or right.

    potential_location = 0

    # If the piece is not in the final rank, it may move forward.
    if pawn_bitboard & RANK_1 == 0:
        potential_location |= pawn_bitboard >> N_FILES

    # If the pawn has crossed the river, allow for left and right movement.
    if pawn_bitboard & BOTTOM_HALF != 0:
        # If we can move to the left without going off the board
        if pawn_bitboard & FILE_1 == 0:
            potential_location |= (pawn_bitboard << 1)
        # If we can move to the right without going off the board
        if pawn_bitboard & FILE_8 == 0:
            potential_location |= (pawn_bitboard >> 1)

    potential_location = restrict_movement_by_team(pawn_bitboard, bit_boards, 'b')

    return potential_location


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


def return_valid_moves_by_type_and_location(bit_boards: BitBoard, piece_class, piece_location: Optional[int] = None):
    if isinstance(piece_location, tuple):
        from engine.engine_util import location_to_bitboard
        piece_location = location_to_bitboard(piece_location)

    if piece_class == 'g':
        return black_general_valid_movements(bit_boards, piece_location)
    elif piece_class == 'a':
        return black_adviser_valid_movements(bit_boards, piece_location)
    elif piece_class == 'p':
        return black_pawn_valid_movements(bit_boards, piece_location)
    return 0
