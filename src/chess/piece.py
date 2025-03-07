from chess import util


class Piece:
    def __init__(self, cord_, piece_):
        self.cord = cord_
        self.dead = False
        self.has_moved = False
        self.chesscord = util.cord2D_to_chesscord(cord_)
        self.pixelcord = util.cord2tlpixel(cord_)
        self.piece_name = piece_


class Pawn(Piece):
    def __init__(self, cord, color):
        super().__init__(cord, f"{color}_pawn")
        self.color = color

    def is_valid_move(self, next_cord2D, board):
        x = self.cord[0]
        y = self.cord[1]
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
            if self.color == "white" and board[x - dx][y - dy][0] != 1:
                return False
            if self.color == "black" and board[x - dx][y + dy][0] != 0:
                return False
            return True
        elif dy < 1 or max_dis < dy or dx != 0:
            return False
        # No jumping over/on piece
        for i in range(1, dy + 1):
            d = i
            if self.color == "black":
                d = -i
            if board[x][y - d][0] != -1:
                return False

        self.has_moved = True
        return True


class Rook(Piece):
    def __init__(self, cord, color):
        self.color = color
        super().__init__(cord, f"{color}_rook")

    def is_valid_move(self, nx_cord2D, board):
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
                if board[i][y][0] != -1:
                    return False

        if dy != 0:
            l, r = y, nx_cord2D[1]
            if l > r:
                l, r = r, l
            for i in range(l + 1, r):
                if board[x][i][0] != -1:
                    return False
        if self.color == "white" and board[nx_x][nx_y][0] == 0:
            return False
        if self.color == "black" and board[nx_x][nx_y][0] == 1:
            return False
        self.has_moved = True
        return True


class Knight(Piece):
    def __init__(self, cord, color):
        self.color = color
        super().__init__(cord, f"{color}_knight")

    def is_valid_move(self, nx_cord2D, board):
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

        if self.color == "white" and board[nx_x][nx_y][0] == 0:
            return False
        if self.color == "black" and board[nx_x][nx_y][0] == 1:
            return False
        return True


class Bishop(Piece):
    def __init__(self, cord, color):
        self.color = color
        super().__init__(cord, f"{color}_bishop")

    def is_valid_move(self, nx_cord2D, board):
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

            if board[r][c][0] != -1:
                return False
        if self.color == "white" and board[nx_x][nx_y][0] == 0:
            return False
        if self.color == "black" and board[nx_x][nx_y][0] == 1:
            return False
        return True


class King(Piece):
    def __init__(self, cord, color):
        self.color = color
        super().__init__(cord, f"{color}_king")

    def is_valid_move(self, nx_cord2D, board):
        x = self.cord[0]
        y = self.cord[1]
        nx_x = nx_cord2D[0]
        nx_y = nx_cord2D[1]
        dx = x - nx_x
        dy = y - nx_y
        if abs(dx) > 1 or abs(dy) > 1:
            return False
        if self.color == "white" and board[nx_x][nx_y][0] == 0:
            return False
        if self.color == "black" and board[nx_x][nx_y][0] == 1:
            return False

        self.has_moved = True
        return True

    def is_valid_king_side_castle(self, nx_cord2D, rook, board):
        x = self.cord[0]
        y = self.cord[1]
        nx_x = nx_cord2D[0]
        nx_y = nx_cord2D[1]
        dx = x - nx_x
        dy = y - nx_y
        if dx != -2 or dy != 0:
            return False
        if self.has_moved is True or rook.has_moved is True:
            return False
        for i in range(x + 1, nx_x + 1):
            if board[i][y][0] != -1:
                return False
        return True

    def is_valid_queen_side_castle(self, nx_cord2D, rook, board):
        x = self.cord[0]
        y = self.cord[1]
        nx_x = nx_cord2D[0]
        nx_y = nx_cord2D[1]
        dx = x - nx_x
        dy = y - nx_y
        if dx != 2 or dy != 0:
            return False
        if self.has_moved is True or rook.has_moved is True:
            return False
        for i in range(rook.cord[0] + 1, x):
            if board[i][y][0] != -1:
                return False
        return True


class Queen(Piece):
    def __init__(self, cord, color):
        self.color = color
        super().__init__(cord, f"{color}_queen")

    def is_valid_move(self, nx_cord2D, board):
        rk = Rook(self.cord, self.color)
        bs = Bishop(self.cord, self.color)
        if not rk.is_valid_move(nx_cord2D, board) and not bs.is_valid_move(
            nx_cord2D, board
        ):
            return False
        return True
