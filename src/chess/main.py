import pygame
from sys import exit
from chess.piece import Piece, Pawn, Rook, Knight, Bishop, King, Queen
from chess import util

prog_name = 'Chess'
screen_size = util.screen_size

class Game:
    def __init__(self):
        self.turn = 0
        self.black_pieces = []
        self.white_pieces = []
        self.moving_index = -1

    def print_board(self, screen, chess_board, chesscord_font):
        screen.blit(chess_board, (0, 0))
        for i in range(8):
            num_cord2D = (0, i)
            num_chesscord = util.cord2D_to_chesscord(num_cord2D)
            color = (209, 139, 71)
            if i % 2 != 0: 
                color = (255, 206, 158)
            num_cord_font = chesscord_font.render(f"{num_chesscord[1]}", 1, color)
            screen.blit(num_cord_font, util.cord2tlpixel(num_cord2D))

        for i in range(8):
            letter_cord2D = (i, 7)
            letter_chesscord = util.cord2D_to_chesscord(letter_cord2D)
            color = (209, 139, 71)
            if i % 2 == 0:
                color = (255, 206, 158)
            letter_cord_font = chesscord_font.render(f"{letter_chesscord[0]}", 1, color)
            screen.blit(letter_cord_font, util.cord2blpixel(letter_cord2D))

    def create_black_pieces(self):
        self.black_pieces.append(Rook((0, 0), 'black'))
        self.black_pieces.append(Knight((1, 0), 'black'))
        self.black_pieces.append(Bishop((2, 0), 'black'))
        self.black_pieces.append(Queen((3, 0), 'black'))
        self.black_pieces.append(King((4, 0), 'black'))
        self.black_pieces.append(Bishop((5, 0), 'black'))
        self.black_pieces.append(Knight((6, 0), 'black'))
        self.black_pieces.append(Rook((7, 0), 'black'))
        for i in range(8):
            self.black_pieces.append(Pawn((i, 1), 'black'))

    def create_white_pieces(self):
        self.white_pieces.append(Rook((0, 7), 'white'))
        self.white_pieces.append(Knight((1, 7), 'white'))
        self.white_pieces.append(Bishop((2, 7), 'white'))
        self.white_pieces.append(Queen((3, 7), 'white'))
        self.white_pieces.append(King((4, 7), 'white'))
        self.white_pieces.append(Bishop((5, 7), 'white'))
        self.white_pieces.append(Knight((6, 7), 'white'))
        self.white_pieces.append(Rook((7, 7), 'white'))
        for i in range(8):
            self.white_pieces.append(Pawn((i, 6), 'white'))

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
                nx_cord2D = (-100, -100)
                for r in range(8):
                    for c in range(8):
                        center_dot = util.cord2centerpixel((r, c))
                        if moving[self.moving_index].piece_rec.collidepoint(center_dot):
                            invalid = False
                            nx_cord2D = (r, c)
                if not invalid and moving[self.moving_index].is_valid_move(nx_cord2D):
                    pygame.mixer.Sound("sound/standard/move-self.mp3").play()
                    moving[self.moving_index].chesscord = util.cord2D_to_chesscord(nx_cord2D)
                    moving[self.moving_index].cord = nx_cord2D
                    print(util.cord2D_to_chesscord(nx_cord2D))
                    moving[self.moving_index].pixelcord = util.cord2tlpixel(nx_cord2D)
                    self.turn = (self.turn + 1) % 2
                else:
                    cord_initial = moving[self.moving_index].cord
                    moving[self.moving_index].pixelcord = util.cord2tlpixel(cord_initial)
                    moving[self.moving_index].piece_rec = moving[self.moving_index].piece.get_rect(topleft = util.cord2tlpixel(cord_initial))

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
    chesscord_font = pygame.font.Font("font/NotoSans-Regular.ttf", 20)

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

        game.print_board(screen, chess_board, chesscord_font)
        game.print_pieces(screen)

        if game.turn == 0:
            game.make_a_move(game.white_pieces, game.black_pieces)
        else:
            game.make_a_move(game.black_pieces, game.white_pieces)

        pygame.display.update()
        clock.tick(60)
    return 0
