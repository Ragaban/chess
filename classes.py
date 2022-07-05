
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
        return self.name + self.color

    def move(self):
        pass

class King(Piece):
    name = "K"
    dir=  (1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1),


class Queen(Piece):
    name = "Q"
    dir= (7, 0), (-7, 0), (0, 7), (0, -7), (7, 7), (-7, 7), (7, -7), (-7, -7), 

class Bishop(Piece):
    name = "B"
    dir = (7, 7), (-7, 7), (7, -7), (-7, -7)

class Knight(Piece):
    name = "G"
    jumps = True
    dir = (())

class Rook(Piece):
    name = "R"
    dir = (7, 0), (-7, 0), (0, 7), (0, -7)

class Pawn(Piece):
    name = "P"
    def __init__(self, color: str):
        self.color = color
        if color == 'w': self.dir = (0, -1)
        else: self.dir = (0, 1)

