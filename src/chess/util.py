from chess.piece import Bishop, King, Knight, Pawn, Piece, Queen, Rook

screen_size = width, height = 730, 730
sq_size = screen_size[0] // 8
rec_size = sq_size * (3.0 / 4.0)


def cord2tlpixel(cord):
    return (cord[0] * sq_size, cord[1] * sq_size)


def cord2blpixel(cord):
    return (cord[0] * sq_size + 75, cord[1] * sq_size + 65)


def cord2centerpixel(cord):
    return (cord[0] * sq_size + sq_size // 2, cord[1] * sq_size + sq_size // 2)


def cord2D_to_chesscord(cord):
    col = chr(97 + cord[0])
    row = 8 - cord[1]
    return (col, row)


def piece_type(piece):
    if piece == "king":
        return "K"
    if piece == "queen":
        return "Q"
    if piece == "rook":
        return "R"
    if piece == "bishop":
        return "B"
    if piece == "knight":
        return "N"
    return ""


def debug_board(board):
    for r, row in enumerate(board):
        for c, piece in enumerate(row):
            if piece.piece_name == "None":
                print(end=" ")
                continue
            if piece.piece_name == "white_king":
                print("♔", end="")
            if piece.piece_name == "white_queen":
                print("♕", end="")
            if piece.piece_name == "white_rook":
                print("♖", end="")
            if piece.piece_name == "white_bishop":
                print("♗", end="")
            if piece.piece_name == "white_knight":
                print("♘", end="")
            if piece.piece_name == "white_pawn":
                print("♙", end="")

            if piece.piece_name == "black_king":
                print("♚", end="")
            if piece.piece_name == "black_queen":
                print("♛", end="")
            if piece.piece_name == "black_rook":
                print("♜", end="")
            if piece.piece_name == "black_bishop":
                print("♝", end="")
            if piece.piece_name == "black_knight":
                print("♞", end="")
            if piece.piece_name == "black_pawn":
                print("♟", end="")
        print()


def algebraic_notation(cord, nx_cord2D, board, move_type):
    x, y = cord
    cur_chess_cord = cord2D_to_chesscord(cord)
    dest_chess_cord = cord2D_to_chesscord(nx_cord2D)
    nx_x, nx_y = nx_cord2D
    color = board[x][y].color
    piece = board[x][y].piece_name.split("_")[1]
    move = []
    # BITMASK
    # take = 0
    # check = 1
    # checkmate = 2
    # king_side_castle = 3
    # queen_side_castle = 4
    # pawn promotion_to_rook = 5
    # pawn_promotion_to_knight = 6
    # pawn_promotion_to_bishop = 7
    # pawn_prmotion_to_queen = 8
    move.append(piece_type(piece))
    if (move_type & (1 << 3)) != 0:
        move.append("O-O")
    elif (move_type & (1 << 4)) != 0:
        move.append("O-O-O")
    elif piece != "pawn":
        file = ""
        for i in range(8):
            for j in range(8):
                if i == x:
                    continue
                if (
                    board[i][j].piece_name == f"{color}_{piece}"
                    and board[i][j].is_valid_move(nx_cord2D, board) is True
                ):
                    file = f"{cur_chess_cord[0]}"

        rank = ""
        for i in range(8):
            if i == y:
                continue
            if (
                board[x][i].piece_name == f"{color}_{piece}"
                and board[x][i].is_valid_move(nx_cord2D, board) is True
            ):
                rank = f"{cur_chess_cord[1]}"
        move.append(file)
        move.append(rank)

    if (move_type & (1 << 0)) != 0:
        if piece == "pawn":
            move.append(f"{cur_chess_cord[0]}")
        move.append("x")

    move.append(f"{dest_chess_cord[0]}")
    move.append(f"{dest_chess_cord[1]}")

    if (move_type & (1 << 5)) != 0:
        move.append("=R")

    if (move_type & (1 << 6)) != 0:
        move.append("=K")

    if (move_type & (1 << 7)) != 0:
        move.append("=B")

    if (move_type & (1 << 8)) != 0:
        move.append("=Q")

    if (move_type & (1 << 1)) != 0:
        move.append("+")

    if (move_type & (1 << 2)) != 0:
        move.append("#")
    return "".join(move)


def turn_pgn_to_string(file_name):
    with open(f"{file_name}.pgn", "r") as file:
        moves = file.read()
    return moves
