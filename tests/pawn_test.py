import pytest

from chess.piece import Pawn

test_boards = [
    [
        [(1, 0), (1, 8), (-1, -1), (-1, -1), (-1, -1), (-1, -1), (0, 8), (0, 0)],
        [(1, 1), (1, 9), (-1, -1), (-1, -1), (-1, -1), (-1, -1), (0, 9), (0, 1)],
        [(1, 2), (1, 10), (-1, -1), (-1, -1), (-1, -1), (-1, -1), (0, 10), (0, 2)],
        [(1, 3), (1, 11), (-1, -1), (-1, -1), (-1, -1), (-1, -1), (0, 11), (0, 3)],
        [(1, 4), (1, 12), (-1, -1), (-1, -1), (-1, -1), (-1, -1), (0, 12), (0, 4)],
        [(1, 5), (1, 13), (-1, -1), (-1, -1), (-1, -1), (-1, -1), (0, 13), (0, 5)],
        [(1, 6), (1, 14), (-1, -1), (-1, -1), (-1, -1), (-1, -1), (0, 14), (0, 6)],
        [(1, 7), (1, 15), (-1, -1), (-1, -1), (-1, -1), (-1, -1), (0, 15), (0, 7)],
    ]
]


@pytest.mark.parametrize(
    ("color", "cur_cord2D", "nx_cord2D", "board"),
    (
        pytest.param(
            "white",
            (3, 6),
            (3, 5),
            test_boards[0],
            id="white_pawn_move_1_forward_no_obstruction",
        ),
        pytest.param(
            "white",
            (3, 6),
            (3, 4),
            test_boards[0],
            id="white_pawn_move_2_forward_no_obstruction",
        ),
    ),
)
def test_valid_pawn_move(color, cur_cord2D, nx_cord2D, board):
    p = Pawn(cur_cord2D, color)
    assert p.is_valid_move(nx_cord2D, board) is True


@pytest.mark.parametrize(
    ("color", "cur_cord2D", "nx_cord2D", "board"),
    (
        pytest.param(
            "white",
            (3, 6),
            (3, 6),
            test_boards[0],
            id="white_pawn_stay_still",
        ),
        pytest.param(
            "white",
            (3, 6),
            (3, 7),
            test_boards[0],
            id="white_pawn_move_1_backward",
        ),
    ),
)
def test_invalid_pawn_move(color, cur_cord2D, nx_cord2D, board):
    p = Pawn(cur_cord2D, color)
    assert p.is_valid_move(nx_cord2D, board) is False
