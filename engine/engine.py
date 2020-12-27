from bitboard import BitBoard


class ChessEngine:
    # TODO: Add in rules to generate legal moves
    # TODO: Allow user to move pieces via their mouse
    # TODO: Build an AI

    def __init__(self, board_state=None):
        self.bit_board = BitBoard(board_state)


if __name__ == "__main__":
    engine = ChessEngine()
    print(engine.bit_board)
