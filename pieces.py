# classes for basic Pieces on the chess board

class Piece:
    """ Base Class for all Piece objects """
    vectors = None              # base_vectors
    first_mv = False            # If a piece has made their first move
    name = None
    scalar = None

    def __init__(self, color):
        self.color = color

    def set_first_mv_true(self):
        self.first_mv = True

    def __str__(self)-> str:
        return self.color[0] + self.name[0].upper()

    def get_scalarized_vectors(self, vector) -> list[tuple]:
        """ Returns a list of vectors that are scalars of a base vector
        Args:
            vector is a vector from self.vectors
        Return:
            list of vectors * range(1, scalar+1)
        """
        return [(vector[0] * s, vector[1] * s) for s in range(1, self.scalar+1)]


class King(Piece):
    name: str = "king"
    scalar: int = 1
    vectors: list[tuple] =  [
        (1, 0), (-1, 0), (0, 1), (0, -1), 
        (1, 1), (-1, 1), (1, -1), (-1, -1),
    ]

class Queen(Piece):
    name: str = "queen"
    scalar: int = 7
    vectors: list[tuple] = [
        (1, 0), (-1, 0), (0, 1), (0, -1), 
        (1, 1), (-1, 1), (1, -1), (-1, -1), 
    ]


class Bishop(Piece):
    name: str = "bishop"
    scalar: int = 7
    vectors: list[tuple] = [
        (1, 1), (-1, 1), (1, -1), (-1, -1),
    ]

class Rook(Piece):
    name: str = "rook"
    scalar: int = 7
    vectors: list[tuple] = [
    (1, 0), (-1, 0), (0, 1), (0, -1),
    ]

class Knight(Piece):
    name: str = "knight"
    scalar: int = 1
    vectors: list[tuple] = [
        (2, 1), (1, 2), (-1, 2), (-2, 1), 
        (-2, -1), (-1, -2), (1, -2), (2, -1)
    ]

    def __str__(self)-> str:
        return self.color[0] + self.name[1].upper()

class Pawn(Piece):
    name: str = "pawn"
    scalar: int = 2

    def __init__(self, color):
        self.color = color
        self.face = -1   # white 
        if color == 'black':
            self.face = 1
            
        self.vectors: list[tuple] = [(self.face, 0)]

    def set_first_mv_true(self):
        self.first_mv = True
        self.scalar = 1

    def capture_vectors(self):
        return [(self.face, 1), (-self.face, -1)]

class Empty():
    """This is a special class that represents an empty tile. 
    Its sole purpose is to be compared to other Piece objs.
    """
    name: str = 'empty'
    color = None
    def __str__(self)-> str:
        return '<>'