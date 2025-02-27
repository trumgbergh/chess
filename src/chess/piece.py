class Piece:
    def __init__(self, cord_, piece_):
        self.cord = cord_
        self.pixelcord = cord2tlpixel(cord_)
        self.piece = pygame.image.load(f'png/all/{piece_}.png').convert_alpha()
        self.piece = pygame.transform.scale(self.piece, (sq_size, sq_size))
        self.piece_rec = self.piece.get_rect(topleft = cord2tlpixel(cord_))
