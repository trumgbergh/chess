import re

from chess import util
from chess.piece import Bishop, King, Knight, Pawn, Piece, Queen, Rook


def get_number_moves(pgn_string):
    num_moves = 0
    moves = pgn_string.split(" ")
    sz = int(len(moves))
    k = int((sz + 3) / 3)
    return sz - k


def parse_single(move_str, moving_color, board):
    if re.search(r"^O-O[+#]?$", move_str) != None:
        if moving_color == "white":
            return (4, 7), (6, 7), -1
        if moving_color == "black":
            return (4, 0), (6, 0), -1
    if re.search(r"^O-O-O[+#]?$", move_str) != None:
        if moving_color == "white":
            return (4, 7), (2, 7), -1
        if moving_color == "black":
            return (4, 0), (2, 0), -1

    pattern = r"^([A-Z]?)([a-h]?)([1-8]?)x?([a-h]{1}[1-8]{1})(\+?|\#?|(\=[A-Z])?)$"
    piece = re.match(pattern, move_str).group(1)
    cur_file = re.match(pattern, move_str).group(2)
    cur_rank = re.match(pattern, move_str).group(3)
    dest = re.match(pattern, move_str).group(4)
    dest_cord2D = util.chesscord_to_cord2D(dest)

    end = re.match(pattern, move_str).group(5)
    chosen = -1
    if end == "=R":
        chosen = 0
    elif end == "=K":
        chosen = 1
    elif end == "=B":
        chosen = 2
    elif end == "=Q":
        chosen = 3

    piece_name = ""
    if piece == "R":
        piece_name = f"{moving_color}_rook"
    elif piece == "N":
        piece_name = f"{moving_color}_knight"
    elif piece == "B":
        piece_name = f"{moving_color}_bishop"
    elif piece == "Q":
        piece_name = f"{moving_color}_queen"
    elif piece == "K":
        piece_name = f"{moving_color}_king"
    else:
        piece_name = f"{moving_color}_pawn"

    for r in range(8):
        for c in range(8):
            if board[r][c].piece_name != piece_name:
                continue
            if cur_file != "" and cur_file != board[r][c].chesscord[0]:
                continue
            if cur_rank != "" and cur_rank != board[r][c].chesscord[1]:
                continue
            if board[r][c].is_valid_move(dest_cord2D, board) is False:
                continue
            return (r, c), dest_cord2D, chosen


def parse_move_pgn(pgn_string, moving_color, board, turn):
    moves = pgn_string.split(" ")
    for i, move in enumerate(moves):
        if i % 3 == 0:
            continue
        if turn == 0:
            return parse_single(move, moving_color, board)
        turn -= 1
