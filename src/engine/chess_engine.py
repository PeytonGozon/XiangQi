from collections import MutableMapping


class ChessEngine:
    # TODO: Add in rules to generate legal moves
    # TODO: Build an AI

    def __init__(self, board_state=None):
        self.bit_board = BitBoard(board_state)


class BitBoard(MutableMapping):
    def __init__(self, board_state=None):
        """
        Initialize a BitBoard object to encapsulate the board's game state. If board_state is specified, then it uses
        board_state rather than the default game state.

        :param board_state: shape: (N_RANK, N_FILE) string array, containing the game's board state.
        """
        from engine.engine_constants import DEFAULT_BOARD_STATE

        self.bit_boards = {
            'r': 0, 'h': 0, 'e': 0, 'a': 0, 'g': 0, 'c': 0, 'p': 0,  # black's pieces
            'R': 0, 'H': 0, 'E': 0, 'A': 0, 'G': 0, 'C': 0, 'P': 0,  # red's pieces
        }

        self.string_array_to_bit_board(DEFAULT_BOARD_STATE if board_state is None else board_state)

    def __getitem__(self, piece_name):
        return self.bit_boards[piece_name] if piece_name in self.bit_boards else None

    def __str__(self):
        import numpy as np
        from engine.engine_constants import BIT_BOARD_WIDTH
        return '\n'.join(f"{k}: {np.binary_repr(self.bit_boards[k], width=BIT_BOARD_WIDTH)}" for k in self.bit_boards)

    def __iter__(self):
        return self.bit_boards.__iter__()

    def __len__(self):
        return self.bit_boards.__len__()

    def __setitem__(self, key, value):
        self.bit_boards[key] = value

    def __delitem__(self, key):
        self.bit_boards.__delitem__(key)

    def get_locations_by_piece_class(self):
        from engine.engine_constants import BIT_BOARD_WIDTH
        import numpy as np
        locations = {}

        for piece_class in self.bit_boards:
            # convert a piece's location to binary
            binary_rep = np.array(list(np.binary_repr(self.bit_boards[piece_class], width=BIT_BOARD_WIDTH)), dtype='b')
            # obtain the locations of all non-zero entries
            locations[piece_class] = np.nonzero(binary_rep)

        return locations

    def get_class_by_location(self, location):
        from engine.engine_util import location_to_bitboard
        # Convert the location to a bitboard representation
        bitboard = location_to_bitboard(location)

        for key in self.bit_boards:
            if self.bit_boards[key] & bitboard != 0:
                return key

    def string_array_to_bit_board(self, string_game_state, verbose=True):
        from engine.engine_constants import N_RANKS, N_FILES
        """
        Update the bitboards from 2D string array representation of a game state.
        Board Pieces Key:
            r/R: Chariot (rook)
            h/H: Horse
            e/E: Elephant
            a/A: Advisor
            g/G: General
            c/C: Cannon
            p/P: Pawn/Soldier
              .: Empty space
        :param string_game_state: a 2D array containing the individual pieces of the board, encoded via the key above.
        :param verbose: whether to display more detailed output.
        :return: void, all bit boards are updated in place.
        """
        from engine.engine_util import location_to_bitboard
        # Ensure that the string representation is of the right dimensions.
        assert (string_game_state.shape == (N_RANKS, N_FILES))

        if verbose:
            print(string_game_state)

        for y in range(N_RANKS):
            for x in range(N_FILES):
                # Determine the piece's type. If the piece is blank (.), then move to the next piece.
                piece = string_game_state[y][x]

                if piece is '.':
                    continue

                # Add the current position's binary to the correct bit board.
                if piece in self.bit_boards:
                    self.bit_boards[piece] += location_to_bitboard((x, y))


if __name__ == "__main__":
    engine = ChessEngine()
    print(engine.bit_board)
