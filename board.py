# board class 
from pieces import Piece, Empty

class Board:
    # Takes an array 8x8
    captured_pieces = {
        'white': [],
        'black': []
        }
    def __init__(self, board_state: list[list[Piece|Empty]]):
        self.board_state = board_state

    def print_board_state(self):
        row_num = 8
        print(' A  B  C  D  E  F  G  H')
        for row in self.board_state:
            for idx, item in enumerate(row):
                print(item, end=' ')
                if len(row) - idx == 1:
                    print(f" {row_num}")
                    row_num -= 1
        print()

    def return_element(self, y, x):
        """Easier way to return from a 2d array"""
        return self.board_state[y][x]

    def move_piece(self):
        pass

    def capture_piece(self):
        pass

    def revert_board_state(self):
        pass

    def en_passant(self):
        pass

    def castling(self):
        pass