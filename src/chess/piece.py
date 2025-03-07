from chess import util


class Piece:
    def __init__(self, cord_, piece_):
        self.cord = cord_
        self.chesscord = util.cord2D_to_chesscord(cord_)
        self.pixelcord = util.cord2tlpixel(cord_)
        self.piece_name = piece_


class Pawn(Piece):
    def __init__(self, cord, color):
        super().__init__(cord, f"{color}_pawn")
        self.color = color
        self.has_moved = False

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

        print(max_dis)
        if dy < 1 or max_dis < dy or dx != 0:
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
        super().__init__(cord, f"{color}_rook")


class Knight(Piece):
    def __init__(self, cord, color):
        super().__init__(cord, f"{color}_knight")


class Bishop(Piece):
    def __init__(self, cord, color):
        super().__init__(cord, f"{color}_bishop")


class King(Piece):
    def __init__(self, cord, color):
        super().__init__(cord, f"{color}_king")


class Queen(Piece):
    def __init__(self, cord, color):
        super().__init__(cord, f"{color}_queen")
