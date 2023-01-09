# classes for basic Pieces on the chess board

class Piece:
    vectors: list[tuple] = None
    first_mv = False            # If a piece has made their first move
    name: str = None

    def __init__(self, color):
        self.color = color

    def set_first_mv_true(self):
        self.first_mv = True

    def __str__(self)-> str:
        return self.color[0] + self.name[0].upper()

class King(Piece):
    name: str = "king"
    range: int = 8
    vectors: list[tuple] =  [
        (1, 0), (-1, 0), (0, 1), (0, -1), 
        (1, 1), (-1, 1), (1, -1), (-1, -1),
    ]

class Queen(Piece):
    name: str = "queen"
    range: int = 8
    vectors: list[tuple] = [
        (1, 0), (-1, 0), (0, 1), (0, -1), 
        (1, 1), (-1, 1), (1, -1), (-1, -1), 
    ]


class Bishop(Piece):
    name: str = "bishop"
    range: int = 8
    vectors: list[tuple] = [
        (1, 1), (-1, 1), (1, -1), (-1, -1),
    ]


class Rook(Piece):
    name: str = "rook"
    range: int = 8
    vectors: list[tuple] = [
    (1, 0), (-1, 0), (0, 1), (0, -1),
    ]

class Knight(Piece):
    name: str = "knight"
    range: int = 1
    vectors: list[tuple] = [
        (2, 1), (1, 2), (-1, 2), (-2, 1), 
        (-2, -1), (-1, -2), (1, -2), (2, -1)
    ]

    def __str__(self)-> str:
        return self.color[0] + self.name[1].upper()

class Pawn(Piece):
    name: str = "pawn"
    range: int = 2

    def __init__(self, color):
        self.color = color
        self.face = 1   # white 
        if color == 'black':
            self.face = -1
            
        self.vectors: list[tuple] = [(self.face, 1), (self.face, -1)]

    def set_first_mv_true(self):
        self.first_mv = True
        self.range = 1

    def capture_vectors(self):
        return [(self.face, 1), (self.face, -1)]

class Empty():
    """This is a special class that represents an empty tile. 
    Its sole purpose is to be compared to other Piece objs.
    """
    name: str = 'empty'
    color = None
    def __str__(self)-> str:
        return '<>'