# chess game logic

# TYPES = ["Pawn", "Rook", "Knight", "Bishop", "Queen", "King"]
MOVESETS = {
    # Moves are in (x, y)
    "Pawn": ((0, 1), (0, 2), (-1, 1), (1, 1)),
    "Rook": ((0, 1), (0, -1), (1, 0), (-1, 0)),
    "Knight": ((2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (-1, 2), (1, -2), (-1, -2)),
    "Bishop": ((1, 1), (-1, 1), (1, -1), (1, 1)),
    "Queen": ((1, 1), (-1, 1), (1, -1), (1, 1), (0, 1), (0, -1), (1, 0), (-1, 0)),
    "King": ((1, 1), (-1, 1), (1, -1), (1, 1), (0, 1), (0, -1), (1, 0), (-1, 0)),
}


class ChessPiece:
    def __init__(self, type, color, range):
        self.type: str = type
        self.color: str = color
        self.range: bool = range
        self.moveset: tuple[tuple, ...] = MOVESETS[type]
        self.first_move = False

    def __str__(self):
        if self.type == "Knight":
            return f"{self.color[0]}{self.type[1].upper()}"
        else:
            return f"{self.color[0]}{self.type[0].upper()}"


class ChessBoard:
    def __init__(self):
        self.board = [
            [None for _ in range(8)] for _ in range(8)
        ]  # 8x8 2d list filled with None

    def get_item(self, x, y):
        return self.board[y][x]

    def set_piece(self, p, x, y):
        self.board[y][x] = p

    def remove_piece(self, x, y) -> ChessPiece | None:
        item = self.board[y].pop(x)
        self.board[y][x] = None
        return item

    def prt_board(self):
        for row in self.board:
            print("  A B C D E F G H")
            for i, item in enumerate(row):
                if i == 0:
                    print(f"8 - {i} |")
                if not item:
                    print("[]", end="")
                else:
                    print(item)

    def parse_chess_coord(self, s: str) -> tuple[int, int]:
        """Turns Chess Coordinates (A1-H8) to 2d list coordinates"""
        m = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
        x = m[s[0].lower()]
        y = 8 - int(s[1])
        return x, y
