from pieces_and_board import MOVESETS, ChessBoard, ChessPiece
from class_gamelogic import GameLogic

from exceptions import NegIndexError


class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.captured_pieces = []

    def __str__(self):
        return self.color

    def capture_piece(self, p: ChessPiece):
        self.capture_piece.append(p)


class Game:
    messages = [
        "Choose a piece (a1-h8): ",
        "Choose where to move (a1-h8): ",
    ]

    def __init__(self, board: ChessBoard, p1: Player, p2: Player):
        self.board = board
        self.p1 = p1
        self.p2 = p2
        self.set_current_player(p1)
        self.logic = GameLogic(self.board)

    def run(self):
        # Gameplay Loop
        # Before Game Start
        move_history = []  # all the moves made in a game
        turn = 1

        while True:
            self.add_moves_to_all_pieces()

            ## REMOVE THIS BLOCK
            for row in self.board.board:
                for item in row:
                    if item:
                        print(f"{item} - {item.moves_current}")

            ##

            # Turn Start
            if turn % 2 == 1:
                self.set_current_player(self.p1)
            else:
                self.set_current_player(self.p2)

            print(f"Turn: {turn}, {self.current_player}'s turn")
            self.board.prt_board()

            # Player Decision Time
            while True:
                # Choose your piece
                pos1 = self.select_coord(self.messages[0])
                item = self.board[*pos1]
                if not item:
                    print(f"{item}")
                    continue
                piece = item
                # del item
                # TODO: this gets repeated
                if piece.color.lower() != self.current_player.color.lower():
                    print(f"Wrong Color {piece.color} {self.current_player.color}")
                    continue

                # Choose where to go
                pos2 = self.select_coord(self.messages[1])
                v = self.calc_vec(pos2, pos2)
                if v not in piece.moves_current:
                    print(f"{v} . {piece.moves_current}")
                    continue

                break

            removed_item = self.board.remove_piece(*pos2)
            self.board.set_piece(piece, *pos2)
            if removed_item:
                self.current_player.capture_piece(removed_item)

            # End Step
            turn += 1

    def calc_vec(self, p1, p2):
        "p1 is our end point and p2 is our starting point"
        x1, y1 = p1
        x2, y2 = p2
        vx = x1 - x2
        vy = y1 - y2
        return vx, vy

    def add_moves_to_all_pieces(self):
        #! TODO only knights work get moves.
        for y, row in enumerate(self.board.board):
            for x, item in enumerate(row):
                if not item:
                    continue
                piece = item  # now we know it's not None
                vectors = MOVESETS[item.type]

                if piece.type == "Knight":
                    m = self.logic.get_moves_knight(piece, vectors, x, y)
                    piece.add_current_moves(m)
                elif piece.type == "Pawn":
                    m = self.logic.get_moves_pawn(piece, vectors[0], x, y)
                    m2 = self.logic.get_attack_moves_pawn(piece, vectors[1], x, y)
                    piece.add_current_moves(m)
                else:
                    valid_moves = self.logic.get_moves_rbqk(piece, vectors, x, y)
                    piece.add_current_moves(valid_moves)

    def set_current_player(self, player: Player):
        self.current_player = player

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
