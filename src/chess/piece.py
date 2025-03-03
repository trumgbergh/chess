from chess import util
import pygame

class Piece:
    def __init__(self, cord_, piece_):
        pygame.init()
        self.cord = cord_
        self.chesscord = util.cord2D_to_chesscord(cord_)
        self.pixelcord = util.cord2tlpixel(cord_)
        self.piece = pygame.image.load(f'png/all/{piece_}.png').convert_alpha()
        self.piece = pygame.transform.scale(self.piece, (util.sq_size, util.sq_size))
        self.piece_rec = self.piece.get_rect(topleft = util.cord2tlpixel(cord_))

class Pawn(Piece):
    def __init__(self, cord, color):
        super().__init__(cord, f"{color}_pawn")
        self.color = color
        self.has_moved = False

    def is_valid_move(self, next_cord2D):
        dx = self.cord[0] - next_cord2D[0]
        dy = self.cord[1] - next_cord2D[1]
        max_dis = 1
        if self.has_moved == False:
            max_dis = 2
        if self.color == 'white':
            if (not 1 <= dy <= max_dis) or dx != 0:
                return False
        if self.color == 'black':
            if (not -1 >= dy >= -max_dis) or dx != 0:
                return False
        self.has_move = True
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
        
