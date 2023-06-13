from dataclasses import dataclass, field
from pieces import Piece, Pawn, Rook, Knight, Bishop, Queen, King


@dataclass
class ChessBoard:
    """TO BE FILLED"""

    ranks = ("A", "B", "C", "D", "E", "F", "G", "H")
    files = ("8", "7", "6", "5", "4", "3", "2", "1")
    piece_map = {"P": Pawn, "R": Rook, "N": Knight, "B": Bishop, "Q": Queen, "K": King}
    captured_pieces = {"white": [], "black": []}
    move_history = []

    board_state: list[list[None | Piece]] = field(
        default_factory=lambda: [[None for _ in range(8)] for _ in range(8)]
    )  # src: https://stackoverflow.com/questions/53632152/why-cant-dataclasses-have-mutable-defaults-in-their-class-attributes-declaratio

    # Funcs that modify board
    def set_board_state(self, bs: list[list[str]]) -> None:
        # a read csv file is turned into board state ChessBoard can use
        for y, row in enumerate(bs):
            for x, tile in enumerate(row):
                if tile == "":
                    continue

                color = "white" if tile[0] == "w" else "black"

                piece = self.piece_map[tile[1]](color)
                self.set_piece(piece=piece, y=y, x=x)

    def set_piece(self, piece, y, x) -> Piece | None:
        # TODO Not sure if this is right. Test a data structure that saves game history
        """place piece at index y,x and return og item at [y][x]"""
        replaced_item, self.board_state[y][x] = self.board_state[y][x], piece
        return replaced_item

    def remove_piece(self, piece: Piece, y: int, x: int, ny: int, nx: int) -> Piece:
        # TODO same
        """removes item in [y][x] and replaces with None TODO Needs check before removing"""
        removed_piece, self.board_state[y][x] = self.board_state[y].pop(x), None
        return removed_piece  # type: ignore

    def promote_piece(self, y: int, x: int, choice: str):
        raise NotImplementedError

    # Funcs that convert data
    def rank_file_to_yx(self, rank, file: tuple[str, str]) -> tuple[int, int]:
        """Turns rank and file into x, y coordinates:  A8 -> (0,0), A1 -> (0, 7)"""
        return self.ranks.index(rank), self.files.index(file)

    def yx_to_rank_file(self, y: int, x: int) -> tuple[str, str]:
        """Turns y, x coord into rank and file. Reverse func to swap_coord_ctl"""
        return self.ranks[y], self.files[x]

    def get_board_state(self) -> list[list[str]]:
        """returns the board state as list[list[str] for external functions to use. Usually for print/draw functions"""
        board_state_str = [["" for _ in range(8)] for _ in range(8)]
        for y, row in enumerate(self.board_state):
            for x, item in enumerate(row):
                if item == None:
                    board_state_str[y][x] = ""
                else:
                    color_char, name_char = item.color[0], item.name[0]
                    board_state_str[y][x] = f"{color_char}{name_char}"
        return board_state_str
