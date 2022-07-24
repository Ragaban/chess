from typing import TypeAlias

Vector: TypeAlias = tuple[int, int]


class Player:
    captures = []
    # games = {"wins": 0, "loses": 0}

    def __init__(self, color: str):
        self.color = color


class Piece:
    """ vec attr = (y, x) """
    def __init__(self, color: str):
        self.color = color
        self.fm = False

    def __str__(self):
        return  self.color[0] + self.name[0]

    def did_first_move(self):
        self.fm = True
 

class King(Piece):
    name: str = "King"
    range: int = 1
    vec: tuple[Vector,...] = (
        (1, 0), (-1, 0), (0, 1), (0, -1), 
        (1, 1), (-1, 1), (1, -1), (-1, -1),
    )

    
class Queen(Piece):
    name: str = "Queen"
    range: int = 7
    vec: tuple[Vector,...] = (
        (1, 0), (-1, 0), (0, 1), (0, -1), 
        (1, 1), (-1, 1), (1, -1), (-1, -1), 
    )

class Bishop(Piece):
    name: str = "Bishop"
    range: int = 7
    vec: tuple[Vector,...] = (
        (1, 1), (-1, 1), (1, -1), (-1, -1),
    )

class Rook(Piece):
    name: str = "Rook"
    range: int = 7
    vec: tuple[Vector,...] = (
    (1, 0), (-1, 0), (0, 1), (0, -1),
    )

class Pawn(Piece):
    name: str = "Pawn"
    range: int = 2
    def __init__(self, color: str):
        # set vector of pawn piece
        self.color = color
        self.fm = False

        if color == 'white': 
            self.vec: tuple[Vector,...] = ((-1, 0),) 
        else: 
            self.vec: tuple[Vector,...] = ((1, 0),)             

    def did_first_move(self):
        self.range = 1
        self.fm = True 
    
    


# Knight special piece
class Knight(Piece):
    """ Knight has range 1 so for loops only go once"""
    name: str = "Knight"
    jumps: bool = True
    range: int = 1
    vec: tuple[Vector,...] = (
        (2, 1), (1, 2), (-1, 2), (-2, 1), 
        (-2, -1), (-1, -2), (1, -2), (2, -1)
    )

    def __str__(self):
        return f"{self.color[0]}{self.name[1].upper()}"