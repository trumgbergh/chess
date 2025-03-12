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
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()


class Game:
    def __init__(self):
        self.turn = 0
        self.running = False
        self.writing_file = True
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
        self.writing_file = False
        if game_name is None:
            return
        pgn_string = util.turn_pgn_to_string(game_name)
        num_moves = parser.get_number_moves(pgn_string)
        for i in range(num_moves):
            if len(self.board_history) == self.turn:
                self.board_history.append(copy.deepcopy(self.board))

            moving_color = "white"
            if self.turn % 2 != 0:
                moving_color = "black"
            cur_cord, nx_cord, chosen = parser.parse_move_pgn(
                pgn_string, moving_color, self.board, self.turn
            )
            self.move_piece(cur_cord, nx_cord, chosen)
            self.move_type = 0
            self.turn += 1
        # self.writing_file = True

    def write_move_to_pgn(self, cell, nx_cord2D):
        if self.writing_file is False:
            return
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

    def print_board(self, chess_board, chesscord_font):
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

    def print_pieces(self):
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

    def pawn_promotion(self, pawn_cord, chosen=0):
        r, c = pawn_cord
        color = self.board[r][c].color
        cur_cord = self.board[r][c].cord
        # 0 = queen, 1 = knight, 2 = rook, 3 = bishop
        if chosen == 0:
            self.board[r][c] = Queen(cur_cord, color)
        if chosen == 1:
            self.board[r][c] = Knight(cur_cord, color)
        if chosen == 2:
            self.board[r][c] = Rook(cur_cord, color)
        if chosen == 3:
            self.board[r][c] = Bishop(cur_cord, color)
        return chosen

    def draw_promotion_UI(self, moving_color, promotion_cell):
        white_color = (255, 255, 255)
        topleft_pixel = util.cord2tlpixel(promotion_cell)
        width, height = util.sq_size + 2, util.sq_size * 4

        rectangle = pygame.Rect(topleft_pixel, (width, height))
        pygame.draw.rect(screen, white_color, rectangle)

        promotion_piece = ["queen", "knight", "rook", "bishop"]
        for d, piece_name in enumerate(promotion_piece):
            r, c = promotion_cell
            piece = f"{moving_color}_{piece_name}"
            if moving_color == "white":
                c += d
            else:
                c -= d
            screen.blit(self.image[piece], util.cord2tlpixel((r, c)))

    def pick_promotion(self, moving_color, promotion_cell):
        piece_rec = []
        promotion_piece = ["queen", "knight", "rook", "bishop"]
        for d, piece_name in enumerate(promotion_piece):
            r, c = promotion_cell
            if moving_color == "white":
                c += d
            else:
                c -= d
            piece = f"{moving_color}_{piece_name}"
            piece_rec.append(
                self.image[piece].get_rect(topleft=util.cord2tlpixel((r, c)))
            )

        while pygame.mouse.get_pressed()[0] is False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            self.draw_promotion_UI(moving_color, promotion_cell)

            pygame.display.update()
            clock.tick(60)

        mouse_pos = pygame.mouse.get_pos()
        for d, rec in enumerate(piece_rec):
            if rec.collidepoint(mouse_pos) is True:
                return d
        return -1

    def play_sound(self):
        print(f"{self.move_type=}")
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

        if (self.move_type & (1 << 9)) != 0:
            pygame.mixer.Sound("sound/standard/game-end.mp3").play()

    def move_piece(self, cell, nx_cord2D, chosen=0):
        r, c = cell
        moving_color = self.board[r][c].color
        piece_name = self.board[r][c].piece_name
        nx_r, nx_c = nx_cord2D
        pawn_en_passant = False
        if self.board[nx_r][nx_c].piece_name != "None":
            self.move_type |= 1 << 0
        else:
            pawn_en_passant = False
            if moving_color == "white":
                if (
                    self.board[nx_r][c].piece_name == "black_pawn"
                    and self.board[nx_r][c].en_passant is True
                ):
                    pawn_en_passant = True
            else:
                if (
                    self.board[nx_r][c].piece_name == "white_pawn"
                    and self.board[nx_r][c].en_passant is True
                ):
                    pawn_en_passant = True

        if pawn_en_passant is True:
            self.move_type |= 1 << 0
            self.board[nx_r][c] = Piece((-1, -1), "None")
            self.board_rec[nx_r][c] = None

        self.board[nx_r][nx_c] = self.board[r][c]
        self.board[r][c] = Piece((-1, -1), "None")
        self.board_rec[r][c] = None

        self.board[nx_r][nx_c].chesscord = util.cord2D_to_chesscord(nx_cord2D)
        self.board[nx_r][nx_c].cord = nx_cord2D

        if piece_name == "white_pawn" and nx_cord2D[1] == 0:
            chosen = self.pick_promotion(moving_color, nx_cord2D)
            if chosen == -1:
                self.abort_move()
                self.turn -= 1
                return
            self.move_type |= 1 << (5 + self.pawn_promotion(nx_cord2D, chosen))
        if piece_name == "black_pawn" and nx_cord2D[1] == 7:
            chosen = self.pick_promotion(moving_color, nx_cord2D)
            if chosen == -1:
                self.abort_move()
                self.turn -= 1
                return
            self.move_type |= 1 << (5 + self.pawn_promotion(nx_cord2D, chosen))

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

        king_row, king_col = opponent_king_cell
        if self.board[nx_r][nx_c].is_valid_move(opponent_king_cell, self.board):
            self.move_type |= 1 << 1
        if self.board[king_row][king_col].is_checkmated(self.board):
            self.running = False
            self.move_type |= 1 << 9

        self.write_move_to_pgn(cell, nx_cord2D)
        self.play_sound()

    def abort_move(self):
        self.board = copy.deepcopy(self.board_history[self.turn])
        for r, row in enumerate(self.board):
            for c, piece in enumerate(row):
                if piece.piece_name == "None":
                    continue
                self.board_rec[r][c] = self.image[piece.piece_name].get_rect(
                    topleft=util.cord2tlpixel(piece.cord)
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

    def process_move(self, moving_color, cur_cord2D, nx_cord2D):
        r, c = cur_cord2D
        piece_name = self.board[r][c].piece_name

        if self.board[r][c].is_valid_move(nx_cord2D, self.board):
            self.move_piece(self.moving_cell, nx_cord2D)
            self.turn = self.turn + 1
        elif piece_name == "white_king" or piece_name == "black_king":
            # Castling
            cord = self.board[r][c].cord
            if nx_cord2D[0] > cord[0]:
                # Castling King side
                if self.board[r][c].is_valid_king_side_castle(nx_cord2D, self.board):
                    rook_cord = (7, c)
                    nx_rook_cord2D = (nx_cord2D[0] - 1, nx_cord2D[1])

                    self.move_piece(self.moving_cell, nx_cord2D)
                    self.move_piece(rook_cord, nx_rook_cord2D)
                    self.move_type |= 1 << 3
                    self.play_sound()
                    self.turn = self.turn + 1
                else:
                    self.abort_move()
            else:
                # Castling Queen side
                if self.board[r][c].is_valid_queen_side_castle(nx_cord2D, self.board):
                    rook_cord = (0, c)
                    nx_rook_cord2D = (nx_cord2D[0] + 1, nx_cord2D[1])
                    self.move_piece(self.moving_cell, nx_cord2D)
                    self.move_piece(rook_cord, nx_rook_cord2D)
                    self.move_type |= 1 << 4
                    self.play_sound()
                    self.turn = self.turn + 1
                else:
                    self.abort_move()
        else:
            self.abort_move()
        self.move_type = 0
        self.moving_cell = (-1, -1)

    def remove_en_passant(self, moving_color):
        for row in self.board:
            for piece in row:
                if piece.color != moving_color:
                    continue
                if piece.piece_name == f"{moving_color}_pawn":
                    piece.en_passant = False

    def make_a_move(self, moving_color):
        mouse_pos = pygame.mouse.get_pos()
        self.remove_en_passant(moving_color)

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
    pygame.display.set_caption(prog_name)
    game = Game()
    game.running = True
    chess_board = pygame.image.load("png/chessboard/chessboard1.png").convert_alpha()
    chess_board = pygame.transform.scale(chess_board, screen_size)
    chesscord_font = pygame.font.Font("font/NotoSans-Regular.ttf", 20)
    pygame.mixer.Sound("sound/standard/game-start.mp3").play()
    game.load_game_from_pgn("game_pgns/game2025_03_12_18_07_55")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return 0

        game.print_board(chess_board, chesscord_font)
        game.print_pieces()

        if game.running is False:
            if game.turn % 2 == 0:
                print("BLACK WON!!!")
            else:
                print("WHITE WON!!!")
            continue

        if len(game.board_history) == game.turn:
            game.board_history.append(copy.deepcopy(game.board))

        if game.turn % 2 == 0:
            game.make_a_move("white")
        else:
            game.make_a_move("black")

        pygame.display.update()
        clock.tick(60)
    return 0
