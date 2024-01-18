ascii_map = {
    "Black": {
        "King": "♔",
        "Queen": "♕",
        "Rook": "♖",
        "Bishop": "♗",
        "Knight": "♘",
        "Pawn": "♙",
    },
    "White": {
        "King": "♚",
        "Queen": "♛",
        "Rook": "♜",
        "Bishop": "♝",
        "Knight": "♞",
        "Pawn": "♟︎",
    },
}


class ChessPiece:
    def __init__(self, type, color):
        self.type: str = type
        self.color: str = color
        if type == "Pawn":
            self.set_pawn_attr_direction(color)
        self.moves_current = []
        self.has_moved = False
        self.symbol = ascii_map[color][type]

    def __str__(self):
        return self.symbol

    # def __str__(self):
    #     if self.type != "Knight":
    #         return f"{self.color[0].lower()}{self.type[0].upper()}"
    #     return f"{self.color[0].lower()}{self.type[1].upper()}"

    def set_pawn_attr_direction(self, color):
        if color.capitalize() == "White":
            self.direction = -1
        else:
            self.direction = 1

    def add_current_moves(self, m: list):
        self.moves_current += m

    def del_current_moves(self):
        self.moves_current = []

    def set_has_moved_true(self):
        self.has_moved = True

    def set_has_moved_false(self):
        self.has_moved = False
