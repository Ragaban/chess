from pieces_and_board import MOVESETS, ChessBoard, ChessPiece, NegIndexError


class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color


class GameLogic:
    def __init__(self, board: ChessBoard, player_current):
        self.board = board
        self.player_current = player_current

    def is_owned(self, player: Player, x: int, y: int) -> bool:
        item = self.board[(x, y)]
        if item:
            if item.color == player.color:
                return True
        return False

    def is_chess_coord(self, ipt: str) -> bool:
        if len(ipt) == 2 and (97 < ord(ipt.lower()) < 105):
            return True
        return False

    def check_vec_oob(self, posx, posy, v) -> bool:
        """oob = Out of Bonds which is our Chessboard"""
        n_posx, n_posy = posx + v[0], posy + v[1]
        try:
            if n_posx < 0 or n_posy < 0:
                raise NegIndexError
            self.board[(n_posx, n_posy)]
            return True
        except (IndexError, NegIndexError):
            return False

    def get_rbqk_moves(self, vectors, posx, posy) -> list:
        m = []
        for v in vectors:
            while True:
                s = 1
                vx, vy = v[0] * s, v[1] * s

                if not self.check_vec_oob(posx, posy, (vx, vy)):
                    break

                n_posx, n_posy = posx + vx, posy + vy
                owned = self.is_owned(self.player_current, n_posx, n_posy)
                if owned:
                    break
                elif not owned:
                    m.append((vx, vy))
                    break

                m.append((vx, vy))
                s + 1

        return m

    def get_knight_moves(self, posx, posy) -> list:
        m = []
        vectors = MOVESETS["Knight"]
        for v in vectors:
            if self.check_vec_oob(posx, posy, v):
                continue
            n_posx, n_posy = posx + v[0], posy + v[1]
            if self.is_owned(self.player_current, n_posx, n_posy):
                continue
            m.append(v)
        return m

    def get_pawn_moves(self):
        # TODO
        ...


class Game:
    messages = [
        "Choose a piece (a1-h8): ",
        "Choose where to move (a1-h8): ",
    ]

    def __init__(self, board: ChessBoard, p1: Player, p2: Player):
        self.board = board
        self.p1 = p1
        self.p2 = p2
        self.logic = GameLogic(self.board, MOVESETS)

    def run(self):
        # Gameplay Loop
        # Before Game Start
        move_history = []  # all the moves made in a game
        turn = 1

        while True:
            self.get_all_moves()

            # Turn Start
            if turn % 2 == 1:
                self.change_current_player(self.p1)
            else:
                self.change_current_player(self.p2)

            print(f"Turn: {turn}, {self.p_current}'s turn")
            self.board.prt_board()

            # Player Decision Time
            while True:
                # Choose your piece
                posx, posy = self.select_coord(self.messages[0])
                piece_selected = self.board[(posx, posy)]
                if not self.logic.is_owned(self.player_current, piece_selected):
                    continue

                # Choose where to go
                n_posx, n_posy = self.select_coord(self.messages[1])
                # TODO: validate chosen point

                # we then provide possible moves for the player and if they want to change their mind

            # End Step
            turn += 1

    def get_all_moves(self):
        for y, row in enumerate(self.board.board):
            for x, item in enumerate(row):
                if not item:
                    continue
                if item.type == "Knight":
                    m = self.logic.get_knight_moves(x, y)
                    item.add_current_moves(m)
                elif item.type == "Pawn":
                    m = self.logic.get_pawn_moves(x, y)
                    item.add_current_moves(m)
                else:
                    vectors = MOVESETS[item.type]
                    m = self.logic.get_rbqk_moves(vectors, x, y)
                    item.add_current_moves(m)

    def change_current_player(self, player):
        self.current_player = player
        self.logic.current_player = player

    def select_coord(self, msg: str) -> tuple[int, int]:
        """asks for valid chess coordinates"""
        while True:
            ipt = input(msg)
            if not self.logic.is_chess_coord(ipt):
                print("Invalid coordinates")
                continue
            return self.board.parse_chess_coord(ipt)


# Outside Functions
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
