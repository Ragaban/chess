from pieces_and_board import MOVESETS, ChessBoard, ChessPiece


class Player:
    def __init__(self, name):
        self.name = name


class Game:
    def __init__(self, board: ChessBoard, p1, p2):
        self.board = board
        self.p1 = p1
        self.p2 = p2

    def run(self):
        # Gameplay Loop
        # Before Game Start
        white = self.p1
        black = self.p2

        turn = 0
        move_history = []
        current_p = self.p1

        while True:
            # Beginng Step
            turn += 1
            if turn % 2 == 1:
                current_p = self.p1
            else:
                current_p = self.p2

            print(turn)
            print(current_p)
            self.board.prt_board()
            # Player Move
            while True:
                selected_start: str = self.select_location()
                # validate

                selected_dest: str = self.select_location()
                # validate
                break

            x1, y1 = self.translate_chess_coord(selected_start)
            x2, y2 = self.translate_chess_coord(selected_dest)

            # End Step

    def add_move_history(self):
        ...

    def select_location(self) -> str:
        return input()

    def translate_chess_coord(self, s: str) -> tuple[int, int]:
        m = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
        x = m[s[0].lower()]
        y = 8 - int(s[1])
        return x, y


def get_layout() -> list[list[str]]:
    layout = []
    with open("layout.csv") as csv_file:
        for s in csv_file.readlines():
            s = s.strip()
            l = s.split(",")
            layout.append(l[:-1])
    return layout


def fill_board(b: ChessBoard, layout):
    piece_map = {
        "p": "Pawn",
        "r": "Rook",
        "n": "Knight",
        "b": "Bishop",
        "q": "Queen",
        "k": "King",
    }
    colors = {"b": "Black", "w": "White"}
    limited_range = ["Pawn", "Knight", "King"]
    for y, row in enumerate(layout):
        for x, item in enumerate(row):
            if not item:
                continue
            type = piece_map[item[1].lower()]
            color = colors[item[0].lower()]

            if type in limited_range:
                range = False
            else:
                range = True

            p = ChessPiece(type, color, range)
            b.set_piece(p, x, y)


def main():
    board = ChessBoard()
    layout = get_layout()
    fill_board(board, layout)
    p1 = "player1"
    p2 = "player2"

    game = Game(board, p1, p2)
    game.run()


if __name__ == "__main__":
    main()
