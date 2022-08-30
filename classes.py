from typing import TypeAlias

Vector: TypeAlias = tuple[int, int]


# class Player:
#     # games = {"wins": 0, "loses": 0}
#     def __init__(self, color: str, captures: list):
#         self.color = color
#         self.captures = captures

class Piece:
    """ self.vec = (y, x). """
    vec = []
    def __init__(self, color: str):
        self.color = color
        self.first_mv = False

    def __str__(self):
        return  self.color[0] + self.name[0]

    def made_first_move(self):
        self.frist_mv = True

    def my_vectors(self):
        return self.vec
 

class King(Piece):
    name: str = "King"
    range: int = 1
    vec: tuple[Vector,...] = [
        (1, 0), (-1, 0), (0, 1), (0, -1), 
        (1, 1), (-1, 1), (1, -1), (-1, -1),
    ]

    
class Queen(Piece):
    name: str = "Queen"
    range: int = 7
    vec: tuple[Vector,...] = [
        (1, 0), (-1, 0), (0, 1), (0, -1), 
        (1, 1), (-1, 1), (1, -1), (-1, -1), 
    ]

class Bishop(Piece):
    name: str = "Bishop"
    range: int = 7
    vec: tuple[Vector,...] = [
        (1, 1), (-1, 1), (1, -1), (-1, -1),
    ]

class Rook(Piece):
    name: str = "Rook"
    range: int = 7
    vec: tuple[Vector,...] = [
    (1, 0), (-1, 0), (0, 1), (0, -1),
    ]


class Pawn(Piece):
    name: str = "Pawn"
    range: int = 2

    def __init__(self, color: str):
        self.color = color
        self.first_mv = False
        self.direction = 1            # Black move direction
        if self.color == 'white':       
            self.direction = -1       # White move direction

        self.vec: tuple[Vector,...] = [(1 * self.direction, 0),]    

    def made_first_move(self):
        self.range = 1
        self.first_mv = True 

    def capture_vectors(self) -> list[Vector,]:
        """ return the capture vecs with respective direction"""
        return [(1 * self.direction, 1), (1 * self.direction, -1)]
    

class Knight(Piece):
    """ Knight has range 1 so for loops only go once"""
    name: str = "Knight"
    jumps: bool = True
    range: int = 1
    vec: tuple[Vector,...] = [
        (2, 1), (1, 2), (-1, 2), (-2, 1), 
        (-2, -1), (-1, -2), (1, -2), (2, -1)
    ]

    def __str__(self):
        return f"{self.color[0]}{self.name[1].upper()}"