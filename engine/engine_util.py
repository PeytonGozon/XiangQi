import engine_constants
import bitboard as bb


def piece_class_by_location(bit_board: bb, location):
    """
    Find the class of the piece at a given board position
    :param bit_board: BitBoard object
    :param location: 2-tuple (x,y) of the given location
    :return: the piece's class at location, or "" if it does not exist.
    """
    location_bitboard = location_to_bitboard(location)

    for key in bit_board:
        if bit_board[key] & location_bitboard != 0:
            import visual_constants
            name, color = visual_constants.PIECE_CLASS_TO_TEXT[key]
            return "red " if color == 'r' else "black" + " " + name

    return ""


def location_to_bitboard(location):
    # Create a string of 0s with capacity to store the entire board state.
    binary = '0' * engine_constants.BIT_BOARD_WIDTH

    # Denote the current position with a 1.
    loc = location[1] * engine_constants.N_FILES + location[0]
    binary = binary[:loc] + '1' + binary[loc + 1:]

    # Return the corresponding bit board as a number.
    return int(binary, 2)


def move_piece_by_location(bit_boards, old_location, new_location):
    """ Given two locations, update the bit board.

    :param bit_boards: a BitBoard object
    :param old_location: 2-tuple (x,y), The location of the original piece.
    :param new_location: 2-tuple (x,y), The location to move the piece to.
    :return: void, bit_boards is updated in place.
    """
    # Convert the locations into their bitboard representations.
    old_bitboard = location_to_bitboard(old_location)
    new_bitboard = location_to_bitboard(new_location)

    # The type of the piece we're moving
    piece_type = None

    # Determine the piece class by its location:
    for key in bit_boards:
        # Remove the position from the old bit board
        if bit_boards[key] & old_bitboard != 0:
            piece_type = key
            break

    # Update the board positions
    if piece_type is not None:
        bit_boards[key] &= ~old_bitboard
        bit_boards[key] |= new_bitboard
