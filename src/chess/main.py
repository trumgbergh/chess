import pygame
from sys import exit
from chess.piece import Piece

breakpoint()

prog_name = 'Chess'
screen_size = width, height = 730, 730

sq_size = screen_size[0] // 8
rec_size = sq_size * (3.0 / 4.0)

def cord2tlpixel(cord):
    return (cord[0] * sq_size, cord[1] * sq_size)
def cord2centerpixel(cord):
    return (cord[0] * sq_size + sq_size // 2,
            cord[1] * sq_size + sq_size // 2)

class Game:
    def __init__(self):
        self.turn = 0
        self.black_pieces = []
        self.white_pieces = []
        self.moving_index = -1

    def print_board(self, screen, chess_board):
        screen.blit(chess_board, (0, 0))

    def create_black_pieces(self):
        self.black_pieces.append(Piece((0, 0), 'black_rook'))
        self.black_pieces.append(Piece((1, 0), 'black_knight'))
        self.black_pieces.append(Piece((2, 0), 'black_bishop'))
        self.black_pieces.append(Piece((3, 0), 'black_queen'))
        self.black_pieces.append(Piece((4, 0), 'black_king'))
        self.black_pieces.append(Piece((5, 0), 'black_bishop'))
        self.black_pieces.append(Piece((6, 0), 'black_knight'))
        self.black_pieces.append(Piece((7, 0), 'black_rook'))
        for i in range(8):
            self.black_pieces.append(Piece((i, 1), 'black_pawn'))

    def create_white_pieces(self):
        self.white_pieces.append(Piece((0, 7), 'white_rook'))
        self.white_pieces.append(Piece((1, 7), 'white_knight'))
        self.white_pieces.append(Piece((2, 7), 'white_bishop'))
        self.white_pieces.append(Piece((3, 7), 'white_queen'))
        self.white_pieces.append(Piece((4, 7), 'white_king'))
        self.white_pieces.append(Piece((5, 7), 'white_bishop'))
        self.white_pieces.append(Piece((6, 7), 'white_knight'))
        self.white_pieces.append(Piece((7, 7), 'white_rook'))
        for i in range(8):
            self.white_pieces.append(Piece((i, 6), 'white_pawn'))

    def print_pieces(self, screen):
        for bpiece in self.black_pieces:
            screen.blit(bpiece.piece, bpiece.pixelcord)
        for wpiece in self.white_pieces:
            screen.blit(wpiece.piece, wpiece.pixelcord)

    def make_a_move(self, moving, waiting):
        mouse_pos = pygame.mouse.get_pos()
        if self.moving_index == -1:
            id = 0
            for p in moving:
                if p.piece_rec.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0] == True:
                    self.moving_index = id
                id += 1
            pygame.mouse.get_rel()
        else:
            dx, dy = pygame.mouse.get_rel()
            nx_cord = (moving[self.moving_index].pixelcord[0] + dx, moving[self.moving_index].pixelcord[1] + dy)
            nx_rect = moving[self.moving_index].piece_rec.move((dx, dy))

            moving[self.moving_index].piece_rec = nx_rect
            moving[self.moving_index].pixelcord = nx_cord
            if pygame.mouse.get_pressed()[0] == False:
                invalid = True
                for r in range(8):
                    for c in range(8):
                        center_dot = cord2centerpixel((r, c))
                        if moving[self.moving_index].piece_rec.collidepoint(center_dot):
                            invalid = False
                            moving[self.moving_index].cord = (r, c)
                            print((r, c))
                            moving[self.moving_index].pixelcord = cord2tlpixel((r, c))
                if not invalid:
                    pygame.mixer.Sound("sound/standard/move-self.mp3").play()
                    self.turn = (self.turn + 1) % 2
                else:
                    cord_initial = moving[self.moving_index].cord
                    moving[self.moving_index].pixelcord = cord2tlpixel(cord_initial)
                    moving[self.moving_index].piece_rec = moving[self.moving_index].piece.get_rect(topleft = cord2tlpixel(cord_initial))

                self.moving_index = -1

def main():
    game = Game()
    InGame = False
    pygame.init()
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption(prog_name)
    clock = pygame.time.Clock()
    chess_board = pygame.image.load('png/chessboard/chessboard1.png').convert_alpha()
    chess_board = pygame.transform.scale(chess_board, screen_size)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        if not InGame:
            pygame.mixer.Sound("sound/standard/game-start.mp3").play()
            game.create_black_pieces()
            game.create_white_pieces()
            InGame = True

        game.print_board(screen, chess_board)
        game.print_pieces(screen)

        if game.turn == 0:
            game.make_a_move(game.white_pieces, game.black_pieces)
        else:
            game.make_a_move(game.black_pieces, game.white_pieces)

        pygame.display.update()
        clock.tick(60)
    return 0
