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
            if bpiece.dead is True:
                continue
            name = bpiece.piece_name
            screen.blit(self.image[name], bpiece.pixelcord)
        for wpiece in self.white_pieces:
            if wpiece.dead is True:
                continue
            name = wpiece.piece_name
            screen.blit(self.image[name], wpiece.pixelcord)

    def pawn_promotion(self, moving):
        i = self.moving_index
        color = moving[i].color
        cur_cord = moving[i].cord
        # 0 = rook, 1 = knight, 2 = bishop, 3 = queen
        chosen = 0
        if chosen == 0:
            moving[i] = Rook(cur_cord, color)
        if chosen == 1:
            moving[i] = Knight(cur_cord, color)
        if chosen == 2:
            moving[i] = Bishop(cur_cord, color)
        if chosen == 3:
            moving[i] = Queen(cur_cord, color)

    def move_piece(self, id, nx_cord2D, moving, moving_rec, waiting):
        p = moving[id].piece_name
        cur_cord = moving[id].cord
        if self.board[nx_cord2D[0]][nx_cord2D[1]][0] == -1:
            pygame.mixer.Sound("sound/standard/move-self.mp3").play()
        else:
            pygame.mixer.Sound("sound/standard/capture.mp3").play()
            j = self.board[nx_cord2D[0]][nx_cord2D[1]][1]
            waiting[j].dead = True

        self.board[nx_cord2D[0]][nx_cord2D[1]] = self.board[cur_cord[0]][cur_cord[1]]
        self.board[cur_cord[0]][cur_cord[1]] = (-1, -1)

        moving[id].chesscord = util.cord2D_to_chesscord(nx_cord2D)
        moving[id].cord = nx_cord2D
        if p == "white_pawn" and nx_cord2D[1] == 0:
            self.pawn_promotion(moving)
        if p == "black_pawn" and nx_cord2D[1] == 7:
            self.pawn_promotion(moving)

        print(util.cord2D_to_chesscord(nx_cord2D))
        # updating rec
        moving[id].pixelcord = util.cord2tlpixel(nx_cord2D)
        moving_rec[id] = self.image[p].get_rect(topleft=util.cord2tlpixel(nx_cord2D))

    def abort_move(self, moving, moving_rec):
        p = moving[self.moving_index].piece_name
        cord_initial = moving[self.moving_index].cord
        moving[self.moving_index].pixelcord = util.cord2tlpixel(cord_initial)
        moving_rec[self.moving_index] = self.image[p].get_rect(
            topleft=util.cord2tlpixel(cord_initial)
        )

    def is_king_on_check(self, moving, waiting):
        pass

    def make_a_move(self, moving, moving_rec, waiting):
        mouse_pos = pygame.mouse.get_pos()
        if self.moving_index == -1:
            for i in range(len(moving_rec)):
                if moving[i].dead is True:
                    continue
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
            if pygame.mouse.get_pressed()[0] is True:
                return
            invalid = True
            nx_cord2D = (-100, -100)
            for r in range(8):
                for c in range(8):
                    center_dot = util.cord2centerpixel((r, c))
                    if moving_rec[self.moving_index].collidepoint(center_dot):
                        invalid = False
                        nx_cord2D = (r, c)

            # Checking and updating
            p = moving[self.moving_index].piece_name
            if invalid:
                self.abort_move(moving, moving_rec)
                self.moving_index = -1
                return

            if moving[self.moving_index].is_valid_move(nx_cord2D, self.board):
                self.move_piece(
                    self.moving_index, nx_cord2D, moving, moving_rec, waiting
                )
                self.turn = self.turn ^ 1
            elif p == "white_king" or p == "black_king":
                # Castling
                col = 0
                if moving[self.moving_index].color == "white":
                    col = 7
                cord = moving[self.moving_index].cord
                if nx_cord2D[0] > cord[0]:
                    # Castling King side
                    rook_id = self.board[7][col][1]
                    right_rook = moving[rook_id]
                    rook_cord2D = (nx_cord2D[0] - 1, nx_cord2D[1])
                    attacked = False
                    for x in range(cord[0], nx_cord2D[0] + 1):
                        king_path_cord = (x, col)
                        for piece in waiting:
                            if piece.is_valid_move(king_path_cord, self.board):
                                attacked = True

                    if not attacked and moving[
                        self.moving_index
                    ].is_valid_king_side_castle(nx_cord2D, right_rook, self.board):
                        self.move_piece(
                            self.moving_index, nx_cord2D, moving, moving_rec, waiting
                        )
                        self.move_piece(
                            rook_id, rook_cord2D, moving, moving_rec, waiting
                        )
                        self.turn = self.turn ^ 1
                    else:
                        self.abort_move(moving, moving_rec)
                else:
                    # Castling Queen side
                    rook_id = self.board[0][col][1]
                    left_rook = moving[rook_id]
                    rook_cord2D = (nx_cord2D[0] + 1, nx_cord2D[1])

                    attacked = False
                    for x in range(nx_cord2D[0], cord[0] + 1):
                        king_path_cord = (x, col)
                        for piece in waiting:
                            if piece.is_valid_move(king_path_cord, self.board):
                                attacked = True
                    if not attacked and moving[
                        self.moving_index
                    ].is_valid_queen_side_castle(nx_cord2D, left_rook, self.board):
                        self.move_piece(
                            self.moving_index, nx_cord2D, moving, moving_rec, waiting
                        )
                        self.move_piece(
                            rook_id, rook_cord2D, moving, moving_rec, waiting
                        )
                        self.turn = self.turn ^ 1
                    else:
                        self.abort_move(moving, moving_rec)
            else:
                self.abort_move(moving, moving_rec)
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
            )
        else:
            game.make_a_move(
                game.black_pieces,
                game.black_pieces_rec,
                game.white_pieces,
            )

        pygame.display.update()
        clock.tick(60)
    return 0
