
from re import X


class Piece:
    """vec attr = (y, x)"""
    def __init__(self, color : str):
        self.color = color
        self.first_move = False

        #self.pos = pos
    # OLD: 
    # def update_pos(self, x, y):
    #     self.posx = x
    #     self.posy = y

    def __repr__(self):
        return f"Piece('{self.color}')"

    def __str__(self):
        return  self.color + self.name

    def moved(self):
        self.first_move = False

    def active_move(self, vec : tuple[int, int]):
        self.active_vec = vec

    def rm_active_vec(self):
        del self.active_vec

 
class King(Piece):
    name : str = "K"
    range : int = 1
    vec : tuple[tuple[int, int],...] = (1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1),
    
class Queen(Piece):
    name : str = "Q"
    range : int = 7
    vec : tuple[tuple[int, int],...] = (1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1), 

class Bishop(Piece):
    name : str = "B"
    range : int = 7
    vec : tuple[tuple[int, int],...] = (1, 1), (-1, 1), (1, -1), (-1, -1),

class Rook(Piece):
    name : str = "R"
    range : int = 7
    vec : tuple[tuple[int, int],...] = (1, 0), (-1, 0), (0, 1), (0, -1),

class Pawn(Piece):
    name : str = "P"
    range : int = 1
    def __init__(self, color: str):
        # set vector of pawn piece
        self.color = color
        if color == 'w': self.vec : tuple[tuple[int, int],...] = (-1, 0),  # (0, 0) are needed because ((-1, 0), (0, 0)) is desired
        else: self.vec = (1, 0),              # and ((-1,0)) gets reduced to (-1, 0)   

# Knight special piece
class Knight(Piece):
    """ Knight has range 1 so for loops only go once"""
    name : str = "N"
    jumps : bool = True
    range : int = 1
    vec : tuple[tuple[int, int],...] = (2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)
