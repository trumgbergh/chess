from sys import exit

import pygame

from chess import util
from chess.piece import Bishop, King, Knight, Pawn, Queen, Rook

prog_name = "Chess"
screen_size = util.screen_size


class Game:
    def __init__(self):
        self.turn = 0
        self.board = [[(-1, -1)] * 8 for _ in range(8)]
        self.image = {}
        self.black_pieces = []
        self.black_pieces_rec = []
        self.white_pieces = []
        self.white_pieces_rec = []
        self.moving_index = -1
        self.create_white_pieces()
        self.create_black_pieces()
        for piece in self.black_pieces:
            p = piece.piece_name
            self.image[p] = pygame.image.load(f"png/all/{p}.png").convert_alpha()
            self.image[p] = pygame.transform.scale(
                self.image[p], (util.sq_size, util.sq_size)
            )
            self.black_pieces_rec.append(
                self.image[p].get_rect(topleft=util.cord2tlpixel(piece.cord))
            )
        for piece in self.white_pieces:
            p = piece.piece_name
            self.image[p] = pygame.image.load(f"png/all/{p}.png").convert_alpha()
            self.image[p] = pygame.transform.scale(
                self.image[p], (util.sq_size, util.sq_size)
            )
            self.white_pieces_rec.append(
                self.image[p].get_rect(topleft=util.cord2tlpixel(piece.cord))
            )

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
        self.board[0][0] = (1, len(self.black_pieces))
        self.black_pieces.append(Rook((0, 0), "black"))

        self.board[1][0] = (1, len(self.black_pieces))
        self.black_pieces.append(Knight((1, 0), "black"))

        self.board[2][0] = (1, len(self.black_pieces))
        self.black_pieces.append(Bishop((2, 0), "black"))

        self.board[3][0] = (1, len(self.black_pieces))
        self.black_pieces.append(Queen((3, 0), "black"))

        self.board[4][0] = (1, len(self.black_pieces))
        self.black_pieces.append(King((4, 0), "black"))

        self.board[5][0] = (1, len(self.black_pieces))
        self.black_pieces.append(Bishop((5, 0), "black"))

        self.board[6][0] = (1, len(self.black_pieces))
        self.black_pieces.append(Knight((6, 0), "black"))

        self.board[7][0] = (1, len(self.black_pieces))
        self.black_pieces.append(Rook((7, 0), "black"))

        for i in range(8):
            self.board[i][1] = (1, len(self.black_pieces))
            self.black_pieces.append(Pawn((i, 1), "black"))

    def create_white_pieces(self):
        self.board[0][7] = (0, len(self.white_pieces))
        self.white_pieces.append(Rook((0, 7), "white"))

        self.board[1][7] = (0, len(self.white_pieces))
        self.white_pieces.append(Knight((1, 7), "white"))

        self.board[2][7] = (0, len(self.white_pieces))
        self.white_pieces.append(Bishop((2, 7), "white"))

        self.board[3][7] = (0, len(self.white_pieces))
        self.white_pieces.append(Queen((3, 7), "white"))

        self.board[4][7] = (0, len(self.white_pieces))
        self.white_pieces.append(King((4, 7), "white"))

        self.board[5][7] = (0, len(self.white_pieces))
        self.white_pieces.append(Bishop((5, 7), "white"))

        self.board[6][7] = (0, len(self.white_pieces))
        self.white_pieces.append(Knight((6, 7), "white"))

        self.board[7][7] = (0, len(self.white_pieces))
        self.white_pieces.append(Rook((7, 7), "white"))
        for i in range(8):
            self.board[i][6] = (0, len(self.white_pieces))
            self.white_pieces.append(Pawn((i, 6), "white"))

    def print_pieces(self, screen):
        for bpiece in self.black_pieces:
            name = bpiece.piece_name
            screen.blit(self.image[name], bpiece.pixelcord)
        for wpiece in self.white_pieces:
            name = wpiece.piece_name
            screen.blit(self.image[name], wpiece.pixelcord)

    def make_a_move(self, moving, moving_rec, waiting, waiting_rec):
        mouse_pos = pygame.mouse.get_pos()
        if self.moving_index == -1:
            for i in range(len(moving_rec)):
                if (
                    moving_rec[i].collidepoint(mouse_pos)
                    and pygame.mouse.get_pressed()[0] is True
                ):
                    self.moving_index = i
            pygame.mouse.get_rel()
        else:
            dx, dy = pygame.mouse.get_rel()
            nx_cord = (
                moving[self.moving_index].pixelcord[0] + dx,
                moving[self.moving_index].pixelcord[1] + dy,
            )
            nx_rect = moving_rec[self.moving_index].move((dx, dy))

            moving_rec[self.moving_index] = nx_rect
            moving[self.moving_index].pixelcord = nx_cord
            if pygame.mouse.get_pressed()[0] is False:
                invalid = True
                nx_cord2D = (-100, -100)
                for r in range(8):
                    for c in range(8):
                        center_dot = util.cord2centerpixel((r, c))
                        if moving_rec[self.moving_index].collidepoint(center_dot):
                            invalid = False
                            nx_cord2D = (r, c)
                p = moving[self.moving_index].piece_name
                if not invalid and moving[self.moving_index].is_valid_move(
                    nx_cord2D, self.board
                ):
                    pygame.mixer.Sound("sound/standard/move-self.mp3").play()
                    cur_cord = moving[self.moving_index].cord
                    self.board[nx_cord2D[0]][nx_cord2D[1]] = self.board[cur_cord[0]][
                        cur_cord[1]
                    ]
                    self.board[cur_cord[0]][cur_cord[1]] = (-1, -1)

                    moving[self.moving_index].chesscord = util.cord2D_to_chesscord(
                        nx_cord2D
                    )
                    moving[self.moving_index].cord = nx_cord2D

                    print(util.cord2D_to_chesscord(nx_cord2D))

                    moving[self.moving_index].pixelcord = util.cord2tlpixel(nx_cord2D)
                    moving_rec[self.moving_index] = self.image[p].get_rect(
                        topleft=util.cord2tlpixel(nx_cord2D)
                    )
                    self.turn = self.turn ^ 1
                else:
                    cord_initial = moving[self.moving_index].cord
                    moving[self.moving_index].pixelcord = util.cord2tlpixel(
                        cord_initial
                    )
                    moving_rec[self.moving_index] = self.image[p].get_rect(
                        topleft=util.cord2tlpixel(cord_initial)
                    )

                self.moving_index = -1


def main():
    pygame.init()
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption(prog_name)
    clock = pygame.time.Clock()
    game = Game()
    chess_board = pygame.image.load("png/chessboard/chessboard1.png").convert_alpha()
    chess_board = pygame.transform.scale(chess_board, screen_size)
    chesscord_font = pygame.font.Font("font/NotoSans-Regular.ttf", 20)
    pygame.mixer.Sound("sound/standard/game-start.mp3").play()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        game.print_board(screen, chess_board, chesscord_font)
        game.print_pieces(screen)

        if game.turn == 0:
            game.make_a_move(
                game.white_pieces,
                game.white_pieces_rec,
                game.black_pieces,
                game.black_pieces_rec,
            )
        else:
            game.make_a_move(
                game.black_pieces,
                game.black_pieces_rec,
                game.white_pieces,
                game.white_pieces_rec,
            )

        pygame.display.update()
        clock.tick(60)
    return 0
