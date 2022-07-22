from typing import TypeAlias

Vector: TypeAlias = tuple[int, int]


class Player:
    captures = []
    # games = {"wins": 0, "loses": 0}

    def __init__(self, color: str):
        self.color = color

    

class Piece:
    """vec attr = (y, x)"""
    def __init__(self, color: str):
        self.color = color
        self.moved = False

    def __repr__(self):
        return f"Piece('{self.color}')"

    def __str__(self):
        return  self.color + self.name

    def moved(self):
        self.first_move = False
 
class King(Piece):
    name: str = "K"
    range: int = 1
    vec: tuple[Vector,...] = (
        (1, 0), (-1, 0), (0, 1), (0, -1), 
        (1, 1), (-1, 1), (1, -1), (-1, -1),
    )
    
class Queen(Piece):
    name: str = "Q"
    range: int = 7
    vec: tuple[Vector,...] = (
        (1, 0), (-1, 0), (0, 1), (0, -1), 
        (1, 1), (-1, 1), (1, -1), (-1, -1), 
    )

class Bishop(Piece):
    name: str = "B"
    range: int = 7
    vec: tuple[Vector,...] = (
        (1, 1), (-1, 1), (1, -1), (-1, -1),
    )

class Rook(Piece):
    name: str = "R"
    range: int = 7
    vec: tuple[Vector,...] = (
    (1, 0), (-1, 0), (0, 1), (0, -1),
    )

class Pawn(Piece):
    name: str = "P"
    range: int = 1
    def __init__(self, color: str):
        # set vector of pawn piece
        self.color = color
        if color == 'w': 
            self.vec: tuple[Vector,...] = ((-1, 0), (-2, 0)) 
        else: 
            self.vec: tuple[Vector,...] = ((1, 0), (2, 0))             

    def first_move(self):
        self.moved = True
        if self.vec[0] < 0:
            self.vec = ((-1, 0),)
        else:
            self.vec = ((1, 0),)

# Knight special piece
class Knight(Piece):
    """ Knight has range 1 so for loops only go once"""
    name: str = "N"
    jumps: bool = True
    range: int = 1
    vec: tuple[Vector,...] = (
        (2, 1), (1, 2), (-1, 2), (-2, 1), 
        (-2, -1), (-1, -2), (1, -2), (2, -1)
    )
