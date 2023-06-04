from dataclasses import dataclass
from pieces import Piece, Pawn, Rook, Knight, Bishop, Queen, King

@dataclass
class ChessBoard:
    """A chess board is divided into files(column) and ranks(rows)"""
    file_to_x = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7}
    x_to_file = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H'}

    board_state: list[list[str]]
    captured_pieces = {'white': [], 'black': []}

    move_history = []


    def swap_coord_ctl(self, chess_coord: tuple[str, str]) -> tuple[int, int]:
        """ Turns rank and file into x, y coordinates:  A8 -> (0,0), A1 -> (0, 7)"""
        x = self.file_to_x[chess_coord[0]]
        y = -1 * int(chess_coord[1]) + 8
        return y, x
    
    def swap_coord_ltc(self, list_coord: tuple[int, int]) -> tuple[str, str]:
        """ Turns y, x coord into rank and file. Reverse func to swap_coord_ctl"""
        rank = str(8 - list_coord[0])
        file = self.x_to_file[list_coord[1]]
        return file, rank
    
    
    def promote_piece(self, coord: tuple[int, int], choice):
        raise NotImplementedError