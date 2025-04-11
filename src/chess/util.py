from chess.piece import Piece

screen_size = width, height = 730, 850
board_size = width, height = 730, 730
sq_size = board_size[0] // 8
board_pixel = 0, 80


def cord2tlpixel(cord: tuple[int, int]) -> tuple[int, int]:
    return (board_pixel[0] + cord[0] * sq_size, board_pixel[1] + cord[1] * sq_size)


def cord2blpixel(cord: tuple[int, int]) -> tuple[int, int]:
    return (
        board_pixel[0] + cord[0] * sq_size + 75,
        board_pixel[1] + cord[1] * sq_size + 65,
    )


def cord2centerpixel(cord: tuple[int, int]) -> tuple[int, int]:
    return (
        board_pixel[0] + cord[0] * sq_size + sq_size // 2,
        board_pixel[1] + cord[1] * sq_size + sq_size // 2,
    )


def cord2D_to_chesscord(cord: tuple[int, int]) -> tuple[str, str]:
    file = chr(97 + cord[0])
    rank = chr(48 + (8 - cord[1]))
    return (file, rank)


def chesscord_to_cord2D(chesscord: tuple[str, str]) -> tuple[int, int]:
    row = ord(chesscord[0]) - 97
    col = 56 - ord(chesscord[1])
    return (row, col)


def piece_type(piece: str) -> str:
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


def long_algebraic_notation(
    cord: tuple[int, int], nx_cord2D: tuple[int, int], move_type: int
) -> str:
    cur_chesscord = cord2D_to_chesscord(cord)
    nx_chesscord = cord2D_to_chesscord(nx_cord2D)
    move = []
    move.append(f"{cur_chesscord[0]}")
    move.append(f"{cur_chesscord[1]}")
    move.append(f"{nx_chesscord[0]}")
    move.append(f"{nx_chesscord[1]}")
    if (move_type & (1 << 5)) != 0:
        move.append("q")
    if (move_type & (1 << 6)) != 0:
        move.append("k")
    if (move_type & (1 << 7)) != 0:
        move.append("r")
    if (move_type & (1 << 8)) != 0:
        move.append("b")
    return "".join(move)


def get_FEN(
    board: list[list[Piece]], half_moves: int, full_moves: int, turn: int
) -> str:
    fen = []
    for i in range(8):
        dis = 0
        for j in range(8):
            r, c = j, i
            piece_name = board[r][c].piece_name
            if piece_name == "None":
                dis += 1
            else:
                if dis != 0:
                    num = chr(48 + dis)
                    fen.append(num)
                fen.append(get_FEN_char(piece_name))
                dis = 0
        if dis != 0:
            num = chr(48 + dis)
            fen.append(num)
        if i != 7:
            fen.append("/")

    fen.append(" ")

    if turn % 2 == 0:
        fen.append("w")
    else:
        fen.append("b")

    fen.append(" ")
    castle_rights = False
    wk_r, wk_c = 4, 7
    piece_name = board[wk_r][wk_c].piece_name
    if piece_name == "white_king":
        if board[wk_r][wk_c].has_moved is False:
            if (
                board[7][7].piece_name == "white_rook"
                and board[7][7].has_moved is False
            ):
                castle_rights = True
                fen.append("K")
            if (
                board[0][7].piece_name == "white_rook"
                and board[0][7].has_moved is False
            ):
                castle_rights = True
                fen.append("Q")

    bk_r, bk_c = 4, 0
    piece_name = board[bk_r][bk_c].piece_name
    if piece_name == "black_king":
        if board[bk_r][bk_c].has_moved is False:
            if (
                board[7][0].piece_name == "black_rook"
                and board[7][0].has_moved is False
            ):
                castle_rights = True
                fen.append("k")
            if (
                board[0][0].piece_name == "black_rook"
                and board[0][0].has_moved is False
            ):
                castle_rights = True
                fen.append("q")

    if castle_rights is False:
        fen.append("-")

    fen.append(" ")
    en_passant = False
    for i in range(8):
        if en_passant is True:
            break
        for j in range(8):
            if (
                board[i][j].piece_name == "white_pawn"
                and board[i][j].en_passant is True
            ):
                en_passant = True
                chess_cord = cord2D_to_chesscord((i, j + 1))
                fen.append(chess_cord[0])
                fen.append(chess_cord[1])
            if (
                board[i][j].piece_name == "black_pawn"
                and board[i][j].en_passant is True
            ):
                en_passant = True
                chess_cord = cord2D_to_chesscord((i, j - 1))
                fen.append(chess_cord[0])
                fen.append(chess_cord[1])

    if en_passant is False:
        fen.append("-")

    fen.append(" ")
    fen.append(str(half_moves))

    fen.append(" ")
    fen.append(str(full_moves))
    return "".join(fen)


def get_FEN_char(piece_name: str) -> str:
    if piece_name == "white_pawn":
        return "P"
    elif piece_name == "white_rook":
        return "R"
    elif piece_name == "white_knight":
        return "N"
    elif piece_name == "white_bishop":
        return "B"
    elif piece_name == "white_queen":
        return "Q"
    elif piece_name == "white_king":
        return "K"

    if piece_name == "black_pawn":
        return "p"
    elif piece_name == "black_rook":
        return "r"
    elif piece_name == "black_knight":
        return "n"
    elif piece_name == "black_bishop":
        return "b"
    elif piece_name == "black_queen":
        return "q"
    elif piece_name == "black_king":
        return "k"
    return "?"


def debug_board(board: list[list[Piece]]):
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


def algebraic_notation(
    cord: tuple[int, int],
    nx_cord2D: tuple[int, int],
    board: list[list[Piece]],
    move_type: int,
) -> str:
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
    # pawn promotion_to_queen = 5
    # pawn_promotion_to_knight = 6
    # pawn_promotion_to_rook = 7
    # pawn_prmotion_to_bishop = 8
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
        move.append("=Q")

    if (move_type & (1 << 6)) != 0:
        move.append("=K")

    if (move_type & (1 << 7)) != 0:
        move.append("=R")

    if (move_type & (1 << 8)) != 0:
        move.append("=B")

    if (move_type & (1 << 1)) != 0:
        move.append("+")

    if (move_type & (1 << 2)) != 0:
        move.append("#")
    return "".join(move)


def turn_pgn_to_string(file_name: str) -> str:
    moves_str = []
    with open(f"{file_name}.pgn", "r") as file:
        for line in file:
            moves = line
            if moves[-1] == "\n":
                moves = line[:-1]
            moves_str.append(moves)
            moves_str.append(" ")

    return "".join(moves_str)
