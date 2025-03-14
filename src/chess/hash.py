from random import randint


class ZobristHash:
    def __init__(self, board):
        self.hash_board = [
            [[randint(1, (1 << 64) - 1) for _ in range(21)] for _ in range(8)]
            for _ in range(8)
        ]
        self.black_to_move = randint(1, (1 << 64) - 1)
        self.hash = 0

        for i in range(8):
            for j in range(8):
                self.hash ^= self.hash_board[i][j][self.get_id(board, (i, j))]

    def update_hash_piece_move(self, board, cord2D):
        x, y = cord2D
        self.hash ^= self.hash_board[x][y][self.get_id(board, (x, y))]

    def update_hash_player_turn(self, turn):
        if turn % 2 == 0 and turn != 0:
            self.hash ^= self.black_to_move
        if turn % 2 != 0:
            self.hash ^= self.black_to_move

    def get_id(self, board, cell):
        r, c = cell
        piece_name = board[r][c].piece_name
        if piece_name == "None":
            return 20
        if piece_name == "white_pawn":
            if r > 0 and c == 3:
                if board[r - 1][c].piece_name == "black_pawn" and board[r][
                    c
                ].is_valid_move((r - 1, c - 1), board):
                    return 18
            if r < 7 and c == 3:
                if board[r + 1][c].piece_name == "black_pawn" and board[r][
                    c
                ].is_valid_move((r + 1, c - 1), board):
                    return 18
            return 0
        if piece_name == "white_rook":
            return 1
        if piece_name == "white_knight":
            return 2
        if piece_name == "white_bishop":
            return 3
        if piece_name == "white_queen":
            return 4
        if piece_name == "white_king":
            mask = 0
            if board[r][c].has_moved is False:
                if (
                    board[7][7].piece_name == "white_rook"
                    and board[7][7].has_moved is False
                ):
                    mask |= 1 << 0
                if (
                    board[0][7].piece_name == "white_rook"
                    and board[0][7].has_moved is False
                ):
                    mask |= 1 << 1
            return 5 + mask  # 5 -> 8

        if piece_name == "black_pawn":
            if r > 0 and c == 4:
                if board[r - 1][c].piece_name == "white_pawn" and board[r][
                    c
                ].is_valid_move((r - 1, c + 1), board):
                    return 19
            if r < 7 and c == 4:
                if board[r + 1][c].piece_name == "white_pawn" and board[r][
                    c
                ].is_valid_move((r + 1, c + 1), board):
                    return 19
            return 9
        if piece_name == "black_rook":
            return 10
        if piece_name == "black_knight":
            return 11
        if piece_name == "black_bishop":
            return 12
        if piece_name == "black_queen":
            return 13
        if piece_name == "black_king":
            mask = 0
            if board[r][c].has_moved is False:
                if (
                    board[7][0].piece_name == "black_rook"
                    and board[7][0].has_moved is False
                ):
                    mask |= 1 << 0
                if (
                    board[0][0].piece_name == "black_rook"
                    and board[0][0].has_moved is False
                ):
                    mask |= 1 << 1
            return 14 + mask  # 14 -> 17
        return -1
