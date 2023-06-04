import pytest
from main import fill_pieces
from pieces import Piece, Pawn, Rook, Knight, Bishop, Queen, King

def test_fill_pieces():
    input_board = [
        ['', 'wP', '', '', '', '', '', ''],
        ['wR', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', 'bK']
    ]

    expected_output = [
        [None, Pawn('white'), None, None, None, None, None, None],
        [Rook('white'), None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, King('black')]
    ]

    assert fill_pieces(input_board) == expected_output

def test_fill_pieces_empty_board():
    # Test filling an empty board
    empty_board = [['' for _ in range(8)] for _ in range(8)]
    filled_board = fill_pieces(empty_board)
    assert filled_board == [[None for _ in range(8)] for _ in range(8)]

def test_fill_pieces_board_with_pieces():
    # Test filling a board with different pieces
    board_with_pieces = [
        ['bR', '', '', 'wQ', '', '', '', ''],
        ['', 'wK', '', '', '', '', '', ''],
        ['', '', 'bN', '', '', '', '', ''],
        ['', '', '', '', 'wB', '', '', ''],
        ['', '', '', '', '', '', 'wR', ''],
        ['', '', '', '', '', 'bP', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', 'bK']
    ]
    expected_board = [
        [Rook('black'), None, None, Queen('white'), None, None, None, None],
        [None, King('white'), None, None, None, None, None, None],
        [None, None, Knight('black'), None, None, None, None, None],
        [None, None, None, None, Bishop('white'), None, None, None],
        [None, None, None, None, None, None, Rook('white'), None],
        [None, None, None, None, None, Pawn('black'), None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, King('black')]
    ]
    filled_board = fill_pieces(board_with_pieces)
    assert filled_board == expected_board
