def piece_class_by_location(bit_board, location, just_class=False):
    """
    Find the class of the piece at a given board position
    :param bit_board: BitBoard object
    :param location: 2-tuple (x,y) of the given location
    :param just_class: whether to just return the internal name of the piece or not.
    :return: the piece's class at location, or None if it does not exist.
    """
    location_bitboard = location_to_bitboard(location)

    for key in bit_board:
        if bit_board[key] & location_bitboard != 0:
            if just_class:
                return key
            import visuals.visual_constants
            name, color = visuals.visual_constants.PIECE_CLASS_TO_TEXT[key]
            return "red " if color == 'r' else "black" + " " + name

    return None


def bitboard_to_locations(single_piece_bit_board):
    """
    Converts a bitboard into a list of locations
    :param single_piece_bit_board: integer containing the bitboard of a single piece
    :return: a list containing 2-tuples (x,y) of all the locations.
    """
    from engine import engine_constants
    import numpy as np
    locations = []

    # Convert the bit board into a string
    binary_rep = np.binary_repr(single_piece_bit_board, width=engine_constants.N_FILES * engine_constants.N_RANKS)

    for i in range(len(binary_rep)):
        if binary_rep[i] == '1':
            # Decode the position into its x and y grid coordinates
            x_location = i % engine_constants.N_FILES
            y_location = i // engine_constants.N_RANKS
            locations.append((x_location, y_location))

    # Return the list of all locations, as specified by the bit board.
    return locations


def locations_to_bitboard(locations):
    """
    Given a list of locations, convert it into a bitboard representation.
    :param locations: list of 2-tuples (x,y)
    :return: a bit board locations.
    """
    bit_board = 0

    for location in locations:
        bit_board += location_to_bitboard(location)

    return bit_board


def location_to_bitboard(location):
    """
    Converts a location into a bitboard representation.
    :param location: a 2-Tuple (x,y) of grid coordinates.
    :return: an integer containing the underlying bitboard representation.
    """
    from engine import engine_constants
    # Create a string of 0s with capacity to store the entire board state.
    binary = '0' * engine_constants.BIT_BOARD_WIDTH

    # Denote the current position with a 1.
    loc = location[1] * engine_constants.N_FILES + location[0]
    binary = binary[:loc] + '1' + binary[loc + 1:]

    # Return the corresponding bit board as a number.
    return int(binary, 2)


def move_piece_by_location(bit_boards, old_location, new_location):
    """ Given two locations, update the bit board. No assumptions are made about the move's validity. If the move
    results in a capture, then the capture is made.

    :param bit_boards: a BitBoard object
    :param old_location: 2-tuple (x,y), The location of the original piece.
    :param new_location: 2-tuple (x,y), The location to move the piece to.
    :return: boolean, True if the movement is valid, and False otherwise.
    """
    from engine import piece_movement
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

    if piece_type is not None:
        # Determine the bitboard of valid locations for movement by the piece

        valid_movement_options = piece_movement.return_valid_moves_by_type_and_location(bit_boards, piece_type,
                                                                                        old_bitboard)

        # If the piece type is not valid
        if new_bitboard & valid_movement_options == 0:
            return False

        # Update the board positions
        bit_boards[piece_type] &= ~old_bitboard
        bit_boards[piece_type] |= new_bitboard

        # Black team pieces are represented by lower case letters.
        team = 'b' if str.islower(piece_type) else 'r'
        # Handle capturing the other team's pieces (if they exist):
        for key in bit_boards:
            # Case of capturing a red piece.
            if (team == 'b' and str.isupper(key)) or (team == 'r' and str.islower(key)):
                bit_boards[key] &= ~new_bitboard

        return True

    return False
