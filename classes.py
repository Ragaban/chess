class Piece:
    def __init__(self, color : str):
        self.color = color
        #self.pos = pos

    def __repr__(self):
        return self.name + self.color

    def move(self):
        pass

class King(Piece):
    name = "K"

class Queen(Piece):
    name = "Q"

class Bishop(Piece):
    name = "B"

class Knight(Piece):
    name = "G"

class Rooke(Piece):
    name = "R"

class Pawn(Piece):
    name = "P"


class Empty:
    name = '<>'
    def __repr__(self):
        return self.name