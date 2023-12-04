from pieces_and_board import MOVESETS, ChessBoard, ChessPiece


class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color


class ValidationHandler:
    def __init__(self, board: ChessBoard):
        self.board = board

    def is_owned(self, player: Player, x: int, y: int):
        item = self.board.get_item(x, y)
        if item:
            if item.color == player.color:
                return True
        return False

    def is_chess_coord(ipt: str) -> bool:
        # valid chess coordinate?
        if len(ipt) == 2 and (97 < ord(ipt) < 105):
            return True
        return False


class Game:
    def __init__(self, board: ChessBoard, p1: Player, p2: Player):
        self.board = board
        self.p1 = p1
        self.p2 = p2
        self.validator = ValidationHandler(self.board)

    def run(self):
        # Gameplay Loop
        # Before Game Start
        move_history = []  # all the moves made in a game
        current_p = self.p1
        turn = 0

        while True:
            #
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
            self.select_tile(current_p, "Choose your Piece (A1-H8): ", b=True)
            self.select_tile(current_p, "Choose Destination", b=False)

            # End Step

    def add_move_history(self):
        ...

    def select_tile(self, current_p, info: str, b: bool):
        # TODO
        while True:
            ipt = input(info)


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
    p1 = Player("player1", "white")
    p2 = Player("player2", "black")

    game = Game(board, p1, p2)
    game.run()


if __name__ == "__main__":
    main()
