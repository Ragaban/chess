from typing import Protocol

# classes for basic Pieces on the chess board


class Piece(Protocol):
    """Base Class for all Piece objects"""

    name: str
    vectors: tuple[tuple[int, int], ...]
    color: str


class King(Piece):
    name: str = "King"
    vectors: tuple[tuple[int, int], ...] = (
        (1, 0),
        (-1, 0),
        (0, 1),
        (0, -1),
        (1, 1),
        (-1, 1),
        (1, -1),
        (-1, -1),
    )

    castling_vectors: tuple[tuple[int, int], ...] = ((0, 2), (0, -2))

    def __init__(self, color):
        self.color = color


class Queen(Piece):
    name: str = "Queen"
    vectors: tuple[tuple[int, int], ...] = (
        (1, 0),
        (-1, 0),
        (0, 1),
        (0, -1),
        (1, 1),
        (-1, 1),
        (1, -1),
        (-1, -1),
    )

    def __init__(self, color):
        self.color = color


class Bishop(Piece):
    name: str = "Bishop"
    vectors: tuple[tuple[int, int], ...] = (
        (1, 1),
        (-1, 1),
        (1, -1),
        (-1, -1),
    )

    def __init__(self, color):
        self.color = color


class Rook(Piece):
    name: str = "Rook"
    vectors: tuple[tuple[int, int], ...] = (
        (1, 0),
        (-1, 0),
        (0, 1),
        (0, -1),
    )

    def __init__(self, color):
        self.color = color


class Knight(Piece):
    name: str = "Knight"
    vectors: tuple[tuple[int, int], ...] = (
        (2, 1),
        (1, 2),
        (-1, 2),
        (-2, 1),
        (-2, -1),
        (-1, -2),
        (1, -2),
        (2, -1),
    )

    def __init__(self, color):
        self.color = color

    def __str__(self) -> str:
        return self.color[0] + self.name[1].upper()


class Pawn(Piece):
    def __init__(self, color):
        self.name = "Pawn"
        self.color = color

        self.d = 1 if color == "black" else -1  # self.d is the direction the pawn moves

        self.vectors: tuple[tuple[int, int], ...] = (
            (self.d, 0),  # standard forward
            (self.d * 2, 0),  # double advance first move
        )

        self.capture_vectors: tuple[tuple[int, int], ...] = (
            (self.d, 1),  # capture vector/en passant
            (self.d, -1),  # capture vector/en passant
        )
