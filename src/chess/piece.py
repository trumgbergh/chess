from chess import util


class Piece:
    def __init__(self, cord_, piece_):
        self.cord = cord_
        self.color = piece_.split("_")[0]
        self.has_moved = False
        self.chesscord = util.cord2D_to_chesscord(cord_)
        self.pixelcord = util.cord2tlpixel(cord_)
        self.piece_name = piece_

    def is_king_in_danger(self, cur_cord, nx_cord2D, board):
        attacked = False
        x, y = cur_cord
        nx_x, nx_y = nx_cord2D

        piece1, piece2 = board[x][y], board[nx_x][nx_y]
        board[x][y] = Piece((-1, -1), "None")
        board[nx_x][nx_y] = piece1

        team_king = (-1, -1)
        for r, row in enumerate(board):
            for c, piece in enumerate(row):
                if piece.piece_name == f"{self.color}_king":
                    team_king = (r, c)

        attacked = board[team_king[0]][team_king[1]].is_king_checked(board)

        board[x][y], board[nx_x][nx_y] = piece1, piece2
        return attacked


class Pawn(Piece):
    def __init__(self, cord, color):
        self.en_passant = False
        super().__init__(cord, f"{color}_pawn")

    def check_any_valid_move(self, board):
        dr = [-1, 0, 1, 0]
        dc = [1, 1, 1, 2]
        for i in range(len(dr)):
            x, y = self.cord
            x += dr[i]
            if self.color == "white":
                y -= dc[i]
            else:
                y += dc[i]
            if not (0 <= x <= 7 and 0 <= y <= 7):
                continue
            nx_cord2D = (x, y)
            if self.is_valid_move(nx_cord2D, board) is True:
                return True
        return False

    def is_valid_move(self, next_cord2D, board, king_protection=True):
        x, y = self.cord[0], self.cord[1]
        nx_x, nx_y = next_cord2D
        dx = self.cord[0] - next_cord2D[0]
        dy = self.cord[1] - next_cord2D[1]
        max_dis = 1

        if self.has_moved is False:
            max_dis = 2
        if self.color == "black":
            dy = -dy

        if abs(dx) == 1:
            if dy != 1:
                return False
            invalid = 0
            if self.color == "white":
                if board[nx_x][nx_y].color != "black":
                    invalid += 1
                if (
                    board[nx_x][y].piece_name != "black_pawn"
                    or board[nx_x][y].en_passant is False
                ):
                    invalid += 1

            if self.color == "black":
                if board[nx_x][nx_y].color != "white":
                    invalid += 1
                if (
                    board[nx_x][y].piece_name != "white_pawn"
                    or board[nx_x][y].en_passant is False
                ):
                    invalid += 1
            if invalid == 2:
                return False

            if king_protection is False:
                return True
            else:
                return not super().is_king_in_danger(self.cord, next_cord2D, board)
        elif dy < 1 or max_dis < dy or dx != 0:
            return False
        # No jumping over/on piece
        for i in range(1, dy + 1):
            d = i
            if self.color == "black":
                d = -i
            if board[x][y - d].piece_name != "None":
                return False

        if king_protection is True:
            attacked = super().is_king_in_danger(self.cord, next_cord2D, board)
            if attacked is True:
                return False

        if abs(dy) == 2:
            op_pawn = "white_pawn"
            if self.color == "white":
                op_pawn = "black_pawn"

            if nx_x != 0 and board[nx_x - 1][nx_y].piece_name == op_pawn:
                self.en_passant = True
            if nx_x != 7 and board[nx_x + 1][nx_y].piece_name == op_pawn:
                self.en_passant = True
        self.has_moved = True
        return True


class Rook(Piece):
    def __init__(self, cord, color):
        super().__init__(cord, f"{color}_rook")

    def check_any_valid_move(self, board):
        dr = [1, 0, -1, 0]
        dc = [0, 1, 0, -1]
        for i in range(len(dr)):
            x, y = self.cord
            x += dr[i]
            y += dc[i]
            if not (0 <= x <= 7 and 0 <= y <= 7):
                continue
            nx_cord2D = (x, y)
            if self.is_valid_move(nx_cord2D, board) is True:
                return True
        return False

    def is_valid_move(self, nx_cord2D, board, king_protection=True):
        x = self.cord[0]
        y = self.cord[1]
        nx_x = nx_cord2D[0]
        nx_y = nx_cord2D[1]
        dx = x - nx_x
        dy = y - nx_y
        if dx != 0 and dy != 0:
            return False
        if dx == 0 and dy == 0:
            return False

        # No jumping over
        if dx != 0:
            l, r = x, nx_cord2D[0]
            if l > r:
                l, r = r, l
            for i in range(l + 1, r):
                if board[i][y].piece_name != "None":
                    return False

        if dy != 0:
            l, r = y, nx_cord2D[1]
            if l > r:
                l, r = r, l
            for i in range(l + 1, r):
                if board[x][i].piece_name != "None":
                    return False
        if self.color == "white" and board[nx_x][nx_y].color == "white":
            return False
        if self.color == "black" and board[nx_x][nx_y].color == "black":
            return False

        if king_protection is True:
            attacked = super().is_king_in_danger(self.cord, nx_cord2D, board)
            if attacked is True:
                return False
        self.has_moved = True
        return True


class Knight(Piece):
    def __init__(self, cord, color):
        super().__init__(cord, f"{color}_knight")

    def check_any_valid_move(self, board):
        dr = [2, 2, 1, 1, -1, -1, -2, -2]
        dc = [1, -1, 2, -2, 2, -2, 1, -1]
        for i in range(len(dr)):
            x, y = self.cord
            x += dr[i]
            y += dc[i]
            if not (0 <= x <= 7 and 0 <= y <= 7):
                continue
            nx_cord2D = (x, y)
            if self.is_valid_move(nx_cord2D, board) is True:
                return True
        return False

    def is_valid_move(self, nx_cord2D, board, king_protection=True):
        x = self.cord[0]
        y = self.cord[1]
        nx_x = nx_cord2D[0]
        nx_y = nx_cord2D[1]
        dx = x - nx_x
        dy = y - nx_y
        if dx == 0 or dy == 0:
            return False
        if abs(dx) + abs(dy) != 3:
            return False

        if self.color == "white" and board[nx_x][nx_y].color == "white":
            return False
        if self.color == "black" and board[nx_x][nx_y].color == "black":
            return False

        if king_protection is True:
            attacked = super().is_king_in_danger(self.cord, nx_cord2D, board)
            if attacked is True:
                return False

        return True


class Bishop(Piece):
    def __init__(self, cord, color):
        super().__init__(cord, f"{color}_bishop")

    def check_any_valid_move(self, board):
        dr = [1, 1, -1, -1]
        dc = [1, -1, 1, -1]
        for i in range(len(dr)):
            x, y = self.cord
            x += dr[i]
            y += dc[i]
            if not (0 <= x <= 7 and 0 <= y <= 7):
                continue
            nx_cord2D = (x, y)
            if self.is_valid_move(nx_cord2D, board) is True:
                return True
        return False

    def is_valid_move(self, nx_cord2D, board, king_protection=True):
        x = self.cord[0]
        y = self.cord[1]
        nx_x = nx_cord2D[0]
        nx_y = nx_cord2D[1]
        dx = x - nx_x
        dy = y - nx_y

        if abs(dx) != abs(dy):
            return False
        if dx == 0 and dy == 0:
            return False
        for d in range(1, abs(dx)):
            r, c = x + d, y + d
            if dx > 0:
                r = x - d
            if dy > 0:
                c = y - d

            if board[r][c].piece_name != "None":
                return False
        if self.color == "white" and board[nx_x][nx_y].color == "white":
            return False
        if self.color == "black" and board[nx_x][nx_y].color == "black":
            return False

        if king_protection is True:
            attacked = super().is_king_in_danger(self.cord, nx_cord2D, board)
            if attacked is True:
                return False

        return True


class King(Piece):
    def __init__(self, cord, color):
        super().__init__(cord, f"{color}_king")

    def check_any_valid_move(self, board):
        dr = [1, 1, -1, -1, 1, 0, -1, 0]
        dc = [1, -1, 1, -1, 0, -1, 0, 1]
        for i in range(len(dr)):
            x, y = self.cord
            x += dr[i]
            y += dc[i]
            if not (0 <= x <= 7 and 0 <= y <= 7):
                continue
            nx_cord2D = (x, y)
            if self.is_valid_move(nx_cord2D, board) is True:
                return True
        return False

    def is_checkmated(self, board):
        x, y = self.cord
        if self.is_king_checked(board) is False:
            return False
        for row in board:
            for piece in row:
                if piece.piece_name == "None" or piece.color != self.color:
                    continue

                for r in range(8):
                    for c in range(8):
                        if piece.is_valid_move((r, c), board) is True:
                            return False
        return True

    def is_valid_move(self, nx_cord2D, board, king_protection=True):
        x, y = self.cord
        nx_x, nx_y = nx_cord2D
        dx = x - nx_x
        dy = y - nx_y
        if abs(dx) > 1 or abs(dy) > 1:
            return False
        if self.color == "white" and board[nx_x][nx_y].color == "white":
            return False
        if self.color == "black" and board[nx_x][nx_y].color == "black":
            return False
        if king_protection is True:
            attacked = super().is_king_in_danger(self.cord, nx_cord2D, board)
            if attacked is True:
                return False

        self.has_moved = True
        return True

    def is_king_checked(self, board):
        for i in range(8):
            for j in range(8):
                if board[i][j].piece_name == self.piece_name:
                    x, y = i, j
        for row in board:
            for piece in row:
                if piece.piece_name == "None" or piece.color == self.color:
                    continue
                if piece.is_valid_move((x, y), board, False):
                    return True
        return False

    def is_valid_king_side_castle(self, nx_cord2D, board):
        x, y = self.cord
        nx_x, nx_y = nx_cord2D
        dx = x - nx_x
        dy = y - nx_y

        if self.color == "white" and y != 7:
            return False
        if self.color == "black" and y != 0:
            return False

        rook = board[7][y]
        if rook.piece_name != f"{self.color}_rook":
            return False

        for r in range(x, nx_x + 1):
            king_path_cord = (r, y)
            for row in board:
                for piece in row:
                    if piece.piece_name == "None" or piece.color == self.color:
                        continue
                    if piece.is_valid_move(king_path_cord, board):
                        return False

        if dx != -2 or dy != 0:
            return False
        if self.has_moved is True or rook.has_moved is True:
            return False
        for i in range(x + 1, nx_x + 1):
            if board[i][y].piece_name != "None":
                return False
        return True

    def is_valid_queen_side_castle(self, nx_cord2D, board):
        x, y = self.cord
        nx_x, nx_y = nx_cord2D
        dx = x - nx_x
        dy = y - nx_y

        if self.color == "white" and y != 7:
            return False
        if self.color == "black" and y != 0:
            return False

        rook = board[0][y]
        if rook.piece_name != f"{self.color}_rook":
            return False

        for r in range(nx_x, x + 1):
            king_path_cord = (r, y)
            for row in board:
                for piece in row:
                    if piece.piece_name == "None" or piece.color == self.color:
                        continue
                    if piece.is_valid_move(king_path_cord, board):
                        return False
        if dx != 2 or dy != 0:
            return False
        if self.has_moved is True or rook.has_moved is True:
            return False
        for i in range(rook.cord[0] + 1, x):
            if board[i][y].piece_name != "None":
                return False
        return True


class Queen(Piece):
    def __init__(self, cord, color):
        super().__init__(cord, f"{color}_queen")

    def check_any_valid_move(self, board):
        dr = [1, 1, -1, -1, 1, 0, -1, 0]
        dc = [1, -1, 1, -1, 0, -1, 0, 1]
        for i in range(len(dr)):
            x, y = self.cord
            x += dr[i]
            y += dc[i]
            if not (0 <= x <= 7 and 0 <= y <= 7):
                continue
            nx_cord2D = (x, y)
            if self.is_valid_move(nx_cord2D, board) is True:
                return True
        return False

    def is_valid_move(self, nx_cord2D, board, king_protection=True):
        x, y = self.cord
        nx_x, nx_y = nx_cord2D
        dx = x - nx_x
        dy = y - nx_y
        is_a_bishop = False
        is_a_rook = False
        if dx == 0 and dy == 0:
            return False

        if abs(dx) == abs(dy):
            is_a_bishop = True
        if (dx != 0 and dy == 0) or (dx == 0 and dy != 0):
            is_a_rook = True

        if not is_a_rook and not is_a_bishop:
            return False

        if is_a_rook is True:
            if dx != 0:
                l, r = x, nx_cord2D[0]
                if l > r:
                    l, r = r, l
                for i in range(l + 1, r):
                    if board[i][y].piece_name != "None":
                        return False

            if dy != 0:
                l, r = y, nx_cord2D[1]
                if l > r:
                    l, r = r, l
                for i in range(l + 1, r):
                    if board[x][i].piece_name != "None":
                        return False
        else:
            for d in range(1, abs(dx)):
                r, c = x + d, y + d
                if dx > 0:
                    r = x - d
                if dy > 0:
                    c = y - d

                if board[r][c].piece_name != "None":
                    return False

        if self.color == "white" and board[nx_x][nx_y].color == "white":
            return False
        if self.color == "black" and board[nx_x][nx_y].color == "black":
            return False

        if king_protection is True:
            attacked = super().is_king_in_danger(self.cord, nx_cord2D, board)
            if attacked is True:
                return False

        return True
