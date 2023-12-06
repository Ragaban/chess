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
        if len(ipt) == 2 and (97 < ord(ipt.lower()) < 105):
            return True
        return False

    def is_valid_move_pawn():
        ...

    def is_valid_move_knight():
        ...

    def is_valid_move_rest():
        ...

    def is_king_checked():
        ...


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
        turn = 1

        while True:
            #
            # Beginng Step
            if turn % 2 == 1:
                self.current_p = self.p1
            else:
                self.current_p = self.p2

            print(turn)
            print(self.current_p)
            self.board.prt_board()

            # Player Move
            while True:
                x1, y1 = self.select_piece(self.current_p)
                # we then provide possible moves for the player and if they want to change their mind

            # End Step
            turn += 1

    def add_move_history(self):
        ...

    def select_piece(self, player) -> tuple[int, int]:
        """This function returns the coordinates to the piece"""
        while True:
            ipt = input("Select your piece (A1-H8): ")
            if not self.validator.is_chess_coord(ipt):
                print("Invalid coordinates")
                continue
            x, y = self.board.parse_chess_coord(ipt)
            if self.validator.is_owned(player, x, y):
                return x, y

    def calculate_move(self):
        ...

    def calculate_move_pawn(self):
        ...

    def calculate_move_knight(self):
        ...


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
