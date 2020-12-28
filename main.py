from engine.engine_constants import DEFAULT_BOARD_STATE
from engine.chess_engine import ChessEngine
from visuals.xiangqi_board import Board

if __name__ == "__main__":
    tweaked_board = DEFAULT_BOARD_STATE
    tweaked_board[1][4] = 'P'
    xiangqi_engine = ChessEngine()
    xiangqi_board = Board(xiangqi_engine)
    xiangqi_board.on_execute()
