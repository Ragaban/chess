from typing import TypeAlias

Vector: TypeAlias = tuple[int, int]

class Piece:
    """vec attr = (y, x)"""
    def __init__(self, color: str):
        self.color = color
        self.first_move = False

    def __repr__(self):
        return f"Piece('{self.color}')"

    def __str__(self):
        return  self.color + self.name

    def moved(self):
        self.first_move = False

    def active_move(self, vec: tuple[int, int]):
        self.active_vec = vec

    def rm_active_vec(self):
        del self.active_vec

 
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
            self.vec: tuple[Vector,...] = ((-1, 0),) 
        else: 
            self.vec: tuple[Vector,...] = ((1, 0),)             

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

# ============================================================= #
#                   TESTING AREA

def get_start_board():
    # TODO: Rework loading the board and
    """creates start board"""
    board = [
        [
            Rook('b'), Knight('b'), Bishop('b'), Queen('b'),
            King('b'), Bishop('b'), Knight('b'), Rook('b')
        ],
        [
            Pawn('b'), Pawn('b'), Pawn('b'), Pawn('b'),
            Pawn('b'), Pawn('b'), Pawn('b'), Pawn('b')
        ],
            ['<>','<>','<>','<>','<>','<>','<>','<>'],                                                              # 6
            ['<>','<>','<>','<>','<>','<>','<>','<>'],                                                              # 5
            ['<>','<>','<>','<>','<>','<>','<>','<>'],                                                              # 4
            ['<>','<>','<>','<>','<>','<>','<>','<>'],                                                              # 3
        [
            Pawn('w'), Pawn('w'), Pawn('w'), Pawn('w'),
            Pawn('w'), Pawn('w'), Pawn('w'), Pawn('w')
        ],
        [
            Rook('w'), Knight('w'), Bishop('w'), Queen('w'),
            King('w'), Bishop('w'), Knight('w'), Rook('w')
        ],
    ]
    return board

def all_possible_vectors(
    piece: Piece,
    board: list[list, list]
) -> list[tuple[int, int], ]:
    """return all possible vectors the given piece has on the board"""
    all_vectors = []
    for s in range(1, piece.range+1):
        for v in piece.vec:
            y = v[0] * s
            x = v[1] * s
            try:
                if board[y][x]:
                    pass
            except IndexError:
                continue
            all_vectors.append((y, x))
    return all_vectors

king = King("w")
board = get_start_board()

av = all_possible_vectors(piece=king, board=board)