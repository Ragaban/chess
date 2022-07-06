
from re import X


class Piece:
    def __init__(self, color : str):
        self.color = color
        self.not_moved_yet = True

        #self.pos = pos
    def update_pos(self, x, y):
        self.posx = x
        self.posy = y

    def __repr__(self):
        return f"Piece({self.color}"

    def __str__(self):
        return self.name + self.color

    def move(self):
        pass

class King(Piece):
    name = "K"
    range = 1
    dir =  (1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1),
    

class Queen(Piece):
    name = "Q"
    range = 7
    dir = (1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1), 

class Bishop(Piece):
    name = "B"
    range = 7
    dir = (1, 1), (-1, 1), (1, -1), (-1, -1)

class Rook(Piece):
    name = "R"
    range = 7
    dir = (1, 0), (-1, 0), (0, 1), (0, -1)

class Pawn(Piece):
    name = "P"
    range = 1
    def __init__(self, color: str):
        self.color = color
        if color == 'w': self.dir = ((0, -1))
        else: self.dir = ((0, 1))

# Knight special piece
class Knight(Piece):
    name = "G"
    jumps = True
    dir = (())

