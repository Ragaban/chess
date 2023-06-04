from dataclasses import dataclass
# classes for basic Pieces on the chess board

@dataclass
class Piece:
    """ Base Class for all Piece objects """
    vectors = None              # default vectors w/o special ones
    first_mv = False            # If a piece has made their first move
    name = None
    rules = None
    color: str

    def set_first_mv(self):
        self.first_mv = True

    def __str__(self)-> str:
        return self.color[0] + self.name[0].upper()

    # def get_scalarized_vectors(self, vector) -> list[tuple]:
    #     """ Returns a list of vectors that are scalars of a base vector
    #     Args:
    #         vector is a vector from self.vectors
    #     Return:
    #         list of vectors * range(1, scalar+1)
    #     """
    #     ## TODO: Use this function to for calculations later 
    #     return [(vector[0] * s, vector[1] * s) for s in range(1, self.scalar+1)]


class King(Piece):
    name: str = "king"
    vectors: tuple[tuple] =  (
        (1, 0), (-1, 0), (0, 1), (0, -1), # TODO: Set Opponent AI,
        (1, 1), (-1, 1), (1, -1), (-1, -1),
    )
    castling_vectors = [(0, 2), (2, 0)]

class Queen(Piece):
    name: str = "queen"
    vectors: list[tuple] = [
        (1, 0), (-1, 0), (0, 1), (0, -1), 
        (1, 1), (-1, 1), (1, -1), (-1, -1), 
    ]


class Bishop(Piece):
    name: str = "bishop"
    vectors: list[tuple] = [
        (1, 1), (-1, 1), (1, -1), (-1, -1),
    ]

class Rook(Piece):
    name: str = "rook"
    vectors: list[tuple] = [
    (1, 0), (-1, 0), (0, 1), (0, -1),
    ]

class Knight(Piece):
    name: str = "knight"
    vectors: list[tuple] = [
        (2, 1), (1, 2), (-1, 2), (-2, 1), 
        (-2, -1), (-1, -2), (1, -2), (2, -1)
    ]

    def __str__(self)-> str:
        return self.color[0] + self.name[1].upper()

class Pawn(Piece):
    name: str = "pawn"
    first_mv = False

    def __init__(self, color):
        self.color = color
        self.d = -1   # directon
        if color == 'black':
            self.d = 1
            
        self.vectors: tuple[tuple] = ((self.d, 0))
        self.vectors_first_mv: tuple[tuple] = ((2, 0))
        # capture vectors are also used for en_passant they are the same vectors
        self.capture_vectors: tuple[tuple] = ((self.d, 1), (-self.d, -1))

    def set_first_mv(self):
        self.first_mv = True
