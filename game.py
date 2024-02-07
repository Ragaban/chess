from class_board import ChessBoard
from class_pieces import ChessPiece
from class_gamelogic import GameLogic

# from exceptions import NegIndexError

MOVESETS = {
    # Moves are in (x, y)
    "Pawn": ((0, 1), ((-1, 1), (1, 1))),
    "Rook": ((0, 1), (0, -1), (1, 0), (-1, 0)),
    "Knight": ((2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (-1, 2), (1, -2), (-1, -2)),
    "Bishop": ((1, 1), (-1, 1), (1, -1), (-1, -1)),
    "Queen": ((1, 1), (-1, 1), (1, -1), (-1, -1), (0, 1), (0, -1), (1, 0), (-1, 0)),
    "King": ((1, 1), (-1, 1), (1, -1), (-1, -1), (0, 1), (0, -1), (1, 0), (-1, 0)),
}


file_names = [
    "layout.csv",
    "layout_no_pawns.csv",
]

msgs = [
    "Choose a piece (a1-h8): ",
    "Choose where to move (a1-h8): ",
]


class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.pieces_captured = []

    def __str__(self):
        return self.color

    def capture_piece(self, p: ChessPiece):
        self.pieces_captured.append(p)


class Game:
    def __init__(self, board: ChessBoard, p1: Player, p2: Player):
        self.board = board
        self.p1 = p1
        self.p2 = p2
        self.current_player = p1
        self.logic = GameLogic(self.board)

        self.debug = True

    def run(self):
        move_history = []
        turn = 1

        # Turn Loop
        while True:
            self.calculate_all_possible_moves()
            self.debug_print_all_mvs()

            # Turn Start
            print(f"\nTurn: {turn}, {self.current_player}'s turn")
            self.board.prt_board()

            # Player Move
            pos1, piece = self.player_selects_piece(self.current_player)
            x1, y1 = pos1
            ms = piece.moves_current
            marked_sqrs = [(x1 + vx, y1 + vy) for vx, vy in ms]
            self.board.prt_board(marked_sqrs)
            pos2 = self.player_selects_destiny(pos1, piece)
            removed_item = self.move_piece(pos1, pos2)

            # End Step
            piece.set_has_moved_true()
            used_moved = (pos1, pos2, removed_item)
            move_history.append(used_moved)

            if removed_item:  # if its Piece
                self.current_player.capture_piece(removed_item)

            # End Step
            turn += 1
            self.change_current_player(turn)

    #################################################################################################

    # PLAYER INTERACTION

    def player_selects_piece(self, player):
        while True:
            ipt = input(f"\n{msgs[0]}")  # Select Piece
            if not self.logic.is_chess_coord(ipt):
                print(f"{ipt} is invalid")
                continue

            pos1 = self.parse_chess_coord(ipt)
            piece = self.board[*pos1]

            if not piece:  # piece can be either ChessPiece() or None
                continue

            if not self.logic.is_same_color(piece.color, player.color):
                print(f"{player.color} != {piece.color}")
                continue

            return pos1, piece

    def player_selects_destiny(self, pos1, piece):
        while True:
            ipt = input(f"\n{msgs[1]}")
            if not self.logic.is_chess_coord(ipt):
                print(f"{ipt} is invalid")
                continue

            pos2 = self.parse_chess_coord(ipt)
            vec = self.get_vec_btw_pts(*pos1, *pos2)
            if vec not in piece.moves_current:
                print("invalid move")
                continue
            return pos2

    def move_piece(self, pos1, pos2):
        piece = self.board.remove_item(*pos1)
        removed_item = self.board.remove_item(*pos2)
        self.board.set_item(piece, *pos2)
        return removed_item

    ###########################################################################################

    # CALCULATIONS

    def change_current_player(self, turn):
        if turn % 2 != 0:
            self.current_player = self.p1
        else:
            self.current_player = self.p2

    def get_vec_btw_pts(self, x1, y1, x2, y2):
        "p1 is our start point and p2 is our end point"
        vx = x2 - x1
        vy = y2 - y1
        return vx, vy

    def calculate_all_possible_moves(self):
        # TODO also king check missing. Can something move if it creates self check?
        coords_and_pieces = self.board.where_is_all()

        for coord, piece in coords_and_pieces:
            vectors = MOVESETS[piece.type]
            piece.del_current_moves()

            if piece.type in ("Knight", "King"):
                # pieces with range 1
                for vec in vectors:
                    if self.logic.is_valid_vector_rbqkn(vec, *coord, piece.color):
                        piece.add_move(vec)

            elif piece.type == "Pawn":
                # for baldy fuckboys *whispers under his breath "stupid pawns..."
                # "Pawn": ((0, 1), ((-1, 1), (1, 1))),
                d = piece.direction
                move_vector = (
                    vectors[0][0],
                    vectors[0][1] * d,
                )  # Pawn mv vec can be either (0, 1) or (0, -1) depending on color
                attack_vectors = vectors[1]

                if self.logic.is_valid_move_vector_pawn(move_vector, *coord):
                    piece.add_move(move_vector)

                if not piece.has_moved:
                    new_move_vector = move_vector[0], move_vector[1] * 2
                    if self.logic.is_valid_move_vector_pawn(new_move_vector, *coord):
                        piece.add_move(new_move_vector)

                for vec in attack_vectors:
                    # plus direction
                    vec = vec[0], vec[1] * d
                    if self.logic.is_valid_attack_vector_pawn(vec, *coord, piece.color):
                        piece.add_move(vec)

            else:
                # for pieces with infinite range
                for vec in vectors:
                    s = 0
                    while True:
                        s += 1
                        vx, vy = vec[0] * s, vec[1] * s
                        if self.logic.is_valid_vector_rbqkn(
                            (vx, vy), *coord, piece.color
                        ):
                            piece.add_move((vx, vy))

                        else:
                            break

    def parse_chess_coord(self, s: str) -> tuple[int, int]:
        """Turns Chess Coordinates (A1-H8) to 2d list coordinates"""
        m = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
        x = m[s[0].lower()]
        y = 8 - int(s[1])
        return x, y

    # DEBUG FUNCTIONS

    def debug_print_all_mvs(self):
        if not self.debug:
            return
        pieces_and_coords = self.board.where_is_all()
        for coord, piece in pieces_and_coords:
            print(f"{coord}, {piece.type}, {piece.moves_current}")


def get_layout(file_name) -> list[list[str]]:
    layout = []
    with open(file_name) as csv_file:
        for s in csv_file.readlines():
            s = s.strip()
            l = s.split(",")
            layout.append(l)
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
    for y, row in enumerate(layout):
        for x, item in enumerate(row):
            if not item:
                continue
            type = piece_map[item[1].lower()]
            color = colors[item[0].lower()]

            p = ChessPiece(type, color)
            b.set_item(p, x, y)


def main():
    board = ChessBoard()
    layout = get_layout(file_names[0])
    fill_board(board, layout)
    p1 = Player("Player1", "White")
    p2 = Player("Player2", "Black")

    game = Game(board, p1, p2)
    game.run()


if __name__ == "__main__":
    main()
