import copy
import datetime
from os import environ
from sys import exit

from chess import parser, util
from chess.piece import Bishop, King, Knight, Pawn, Piece, Queen, Rook

environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame  # noqa: E402

prog_name = "Chess"
screen_size = util.screen_size


class Game:
    def __init__(self):
        self.turn = 0
        self.file_name = datetime.datetime.now().strftime("game%Y_%m_%d_%H_%M_%S")
        self.board = [[Piece((-1, -1), "None")] * 8 for _ in range(8)]
        self.board_history = []
        self.board_rec = [[None] * 8 for _ in range(8)]
        self.image = {}
        self.moving_cell = (-1, -1)
        self.move_type = 0
        self.create_white_pieces()
        self.create_black_pieces()
        for row in self.board:
            for piece in row:
                piece_name = piece.piece_name
                r, c = piece.cord
                if piece_name == "None":
                    continue
                self.image[piece_name] = pygame.image.load(
                    f"png/all/{piece_name}.png"
                ).convert_alpha()
                self.image[piece_name] = pygame.transform.scale(
                    self.image[piece_name], (util.sq_size, util.sq_size)
                )
                self.board_rec[r][c] = self.image[piece_name].get_rect(
                    topleft=util.cord2tlpixel(piece.cord)
                )

    def load_game_from_pgn(self, game_name=None):
        if game_name is None:
            return
        pgn_string = util.turn_pgn_to_string(game_name)
        num_moves = parser.get_number_moves(pgn_string)
        print(f"{num_moves=}")
        for i in range(num_moves):
            cur_cord, nx_cord = parser.parse_move_pgn(pgn_string, self.board, self.turn)
            moving_color = "white"
            if self.turn % 2 != 0:
                moving_color = "black"

    def write_move_to_pgn(self, cell, nx_cord2D):
        util.algebraic_notation(
            cell, nx_cord2D, self.board_history[self.turn], self.move_type
        )
        with open(f"game_pgns/{self.file_name}.pgn", "a") as file:
            if self.turn % 2 == 0:
                file.write(f"{int((self.turn / 2)) + 1}. ")
            file.write(
                util.algebraic_notation(
                    cell, nx_cord2D, self.board_history[self.turn], self.move_type
                )
            )
            file.write(" ")

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
        self.board[0][0] = Rook((0, 0), "black")
        self.board[1][0] = Knight((1, 0), "black")
        self.board[2][0] = Bishop((2, 0), "black")
        self.board[3][0] = Queen((3, 0), "black")
        self.board[4][0] = King((4, 0), "black")
        self.board[5][0] = Bishop((5, 0), "black")
        self.board[6][0] = Knight((6, 0), "black")
        self.board[7][0] = Rook((7, 0), "black")

        for i in range(8):
            self.board[i][1] = Pawn((i, 1), "black")

    def create_white_pieces(self):
        self.board[0][7] = Rook((0, 7), "white")
        self.board[1][7] = Knight((1, 7), "white")
        self.board[2][7] = Bishop((2, 7), "white")
        self.board[3][7] = Queen((3, 7), "white")
        self.board[4][7] = King((4, 7), "white")
        self.board[5][7] = Bishop((5, 7), "white")
        self.board[6][7] = Knight((6, 7), "white")
        self.board[7][7] = Rook((7, 7), "white")
        for i in range(8):
            self.board[i][6] = Pawn((i, 6), "white")

    def print_pieces(self, screen):
        r, c = self.moving_cell
        for row in self.board:
            for piece in row:
                name = piece.piece_name
                if name == "None" or piece.cord == self.moving_cell:
                    continue
                screen.blit(self.image[name], piece.pixelcord)
        if self.moving_cell != (-1, -1):
            piece = self.board[r][c]
            name = piece.piece_name
            screen.blit(self.image[name], piece.pixelcord)

    def pawn_promotion(self, pawn_cord):
        r, c = pawn_cord
        color = self.board[r][c].color
        cur_cord = self.board[r][c].cord
        # 0 = rook, 1 = knight, 2 = bishop, 3 = queen
        chosen = 0
        if chosen == 0:
            self.board[r][c] = Rook(cur_cord, color)
        if chosen == 1:
            self.board[r][c] = Knight(cur_cord, color)
        if chosen == 2:
            self.board[r][c] = Bishop(cur_cord, color)
        if chosen == 3:
            self.board[r][c] = Queen(cur_cord, color)
        return chosen

    def play_sound(self):
        if (self.move_type & (1 << 1)) != 0:
            pygame.mixer.Sound("sound/standard/move-check.mp3").play()
        elif (self.move_type & (1 << 0)) != 0:
            pygame.mixer.Sound("sound/standard/capture.mp3").play()
        elif (self.move_type & (1 << 3)) != 0:
            # King side castle
            pygame.mixer.Sound("sound/standard/castle.mp3").play()
        elif (self.move_type & (1 << 4)) != 0:
            # Queen side castle
            pygame.mixer.Sound("sound/standard/castle.mp3").play()
        elif (self.move_type & (1 << 5)) != 0:
            pygame.mixer.Sound("sound/standard/promote.mp3").play()
        elif (self.move_type & (1 << 6)) != 0:
            pygame.mixer.Sound("sound/standard/promote.mp3").play()
        elif (self.move_type & (1 << 7)) != 0:
            pygame.mixer.Sound("sound/standard/promote.mp3").play()
        elif (self.move_type & (1 << 8)) != 0:
            pygame.mixer.Sound("sound/standard/promote.mp3").play()
        else:
            pygame.mixer.Sound("sound/standard/move-self.mp3").play()

    def move_piece(self, cell, nx_cord2D):
        r, c = cell
        moving_color = self.board[r][c].color
        piece_name = self.board[r][c].piece_name
        nx_r, nx_c = nx_cord2D
        if self.board[nx_r][nx_c].piece_name != "None":
            self.move_type |= 1 << 0

        self.board[nx_r][nx_c] = self.board[r][c]
        self.board[r][c] = Piece((-1, -1), "None")
        self.board_rec[r][c] = None

        util.debug_board(self.board_history[self.turn])
        self.board[nx_r][nx_c].chesscord = util.cord2D_to_chesscord(nx_cord2D)
        self.board[nx_r][nx_c].cord = nx_cord2D

        if piece_name == "white_pawn" and nx_cord2D[1] == 0:
            self.move_type |= 1 << (5 + self.pawn_promotion(nx_cord2D))
        if piece_name == "black_pawn" and nx_cord2D[1] == 7:
            self.move_type |= 1 << (5 + self.pawn_promotion(nx_cord2D))

        print(self.board[nx_r][nx_c].chesscord)
        # updating rec
        self.board[nx_r][nx_c].pixelcord = util.cord2tlpixel(nx_cord2D)
        self.board_rec[nx_r][nx_c] = self.image[piece_name].get_rect(
            topleft=util.cord2tlpixel(nx_cord2D)
        )

        opponent_king_cell = (-1, -1)
        for row in self.board:
            for piece in row:
                if piece.piece_name == "None" or piece.color == moving_color:
                    continue
                piece_type = piece.piece_name.split("_")[1]
                if piece_type == "king":
                    opponent_king_cell = piece.cord

        if self.board[nx_r][nx_c].is_valid_move(opponent_king_cell, self.board):
            self.move_type |= 1 << 1

        self.write_move_to_pgn(cell, nx_cord2D)
        self.play_sound()

    def abort_move(self):
        r, c = self.moving_cell
        piece_name = self.board[r][c].piece_name
        cord_initial = self.board[r][c].cord
        self.board[r][c].pixelcord = util.cord2tlpixel(cord_initial)
        self.board_rec[r][c] = self.image[piece_name].get_rect(
            topleft=util.cord2tlpixel(cord_initial)
        )

    def move_piece_pixel(self, cell, dx, dy):
        r, c = cell
        nx_cord = (
            self.board[r][c].pixelcord[0] + dx,
            self.board[r][c].pixelcord[1] + dy,
        )
        nx_rect = self.board_rec[r][c].move((dx, dy))

        self.board_rec[r][c] = nx_rect
        self.board[r][c].pixelcord = nx_cord

    def process_move(self, moving_color, cell, nx_cord2D):
        r, c = cell
        piece_name = self.board[r][c].piece_name

        if self.board[r][c].is_valid_move(nx_cord2D, self.board):
            self.move_piece(self.moving_cell, nx_cord2D)
            self.turn = self.turn + 1
        elif piece_name == "white_king" or piece_name == "black_king":
            # Castling
            col = 0
            if self.board[r][c].color == "white":
                col = 7
            cord = self.board[r][c].cord
            if nx_cord2D[0] > cord[0]:
                # Castling King side
                right_rook = self.board[7][col]
                nx_rook_cord2D = (nx_cord2D[0] - 1, nx_cord2D[1])
                attacked = False
                for x in range(cord[0], nx_cord2D[0] + 1):
                    king_path_cord = (x, col)
                    for row in self.board:
                        for piece in row:
                            if (
                                piece.piece_name == "None"
                                or piece.color == moving_color
                            ):
                                continue
                            if piece.is_valid_move(king_path_cord, self.board):
                                attacked = True

                if not attacked and self.board[r][c].is_valid_king_side_castle(
                    nx_cord2D, right_rook, self.board
                ):
                    self.move_piece(self.moving_cell, nx_cord2D)
                    self.move_piece(right_rook.cord, nx_rook_cord2D)
                    self.move_type |= 1 << 3
                    self.play_sound()
                    self.turn = self.turn + 1
                else:
                    self.abort_move()
            else:
                # Castling Queen side
                left_rook = self.board[0][col]
                nx_rook_cord2D = (nx_cord2D[0] + 1, nx_cord2D[1])

                attacked = False
                for x in range(nx_cord2D[0], cord[0] + 1):
                    king_path_cord = (x, col)
                    for row in self.board:
                        for piece in row:
                            if (
                                piece.piece_name == "None"
                                or piece.color == moving_color
                            ):
                                continue
                            if piece.is_valid_move(king_path_cord, self.board):
                                attacked = True

                if not attacked and self.board[r][c].is_valid_queen_side_castle(
                    nx_cord2D, left_rook, self.board
                ):
                    self.move_piece(self.moving_cell, nx_cord2D)
                    self.move_piece(left_rook.cord, nx_rook_cord2D)
                    self.move_type |= 1 << 4
                    self.play_sound()
                    self.turn = self.turn + 1
                else:
                    self.abort_move()
        else:
            self.abort_move()
        self.move_type = 0
        self.moving_cell = (-1, -1)

    def make_a_move(self, moving_color):
        mouse_pos = pygame.mouse.get_pos()

        if self.moving_cell == (-1, -1):
            for r in range(8):
                for c in range(8):
                    if (
                        self.board_rec[r][c] is None
                        or self.board[r][c].color != moving_color
                    ):
                        continue
                    if (
                        self.board_rec[r][c].collidepoint(mouse_pos)
                        and pygame.mouse.get_pressed()[0] is True
                    ):
                        center_pixel = util.cord2centerpixel((r, c))
                        dx = mouse_pos[0] - center_pixel[0]
                        dy = mouse_pos[1] - center_pixel[1]
                        self.move_piece_pixel((r, c), dx, dy)
                        self.moving_cell = (r, c)
            pygame.mouse.get_rel()
        else:
            r, c = self.moving_cell
            dx, dy = pygame.mouse.get_rel()
            self.move_piece_pixel((r, c), dx, dy)
            if pygame.mouse.get_pressed()[0] is True:
                return
            invalid = True
            nx_cord2D = (-100, -100)
            for row in range(8):
                for col in range(8):
                    center_dot = util.cord2centerpixel((row, col))
                    if self.board_rec[r][c].collidepoint(center_dot):
                        invalid = False
                        nx_cord2D = (row, col)
            if invalid:
                self.abort_move()
                self.move_type = 0
                self.moving_cell = (-1, -1)
                return
            self.process_move(moving_color, self.moving_cell, nx_cord2D)


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
    game.load_game_from_pgn("game_pgns/game2025_03_09_15_14_41")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        game.print_board(screen, chess_board, chesscord_font)
        game.print_pieces(screen)

        if len(game.board_history) == game.turn:
            game.board_history.append(copy.deepcopy(game.board))

        if game.turn % 2 == 0:
            game.make_a_move("white")
        else:
            game.make_a_move("black")

        pygame.display.update()
        clock.tick(60)
    return 0
