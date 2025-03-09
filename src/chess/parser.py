from chess import util
from chess.piece import Bishop, King, Knight, Pawn, Piece, Queen, Rook


def get_number_moves(pgn_string):
    num_moves = 0
    moves = pgn_string.split(" ")
    print(f"{pgn_string=}")
    sz = int(len(moves))
    k = int((sz + 3) / 3)
    return sz - k


def parse_a_move_pgn(pgn_string, board, turn):
    pass
