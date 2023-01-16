# board class 
from pieces import Piece, Empty

class ChessBoard:

    def __init__(self, board_state: list[list[Piece|Empty]]):
        self.board_state = board_state
        self.captured_pieces = {'white': [], 'black': []}


    def print_board_state(self, highlights=None):
        """ Visual representation of board_state.
        Args:
            highlights is a tuple of coordinates
         """
        row_num = 8
        print(' A  B  C  D  E  F  G  H')
        for y, row in enumerate(self.board_state):
            for x, item in enumerate(row):
                if highlights:
                    if (y,x) in highlights:
                        item = 'XX'
                print(item, end=' ')

                if len(row) - x == 1:
                    print(f" {row_num}")
                    row_num -= 1
        print()


    def return_element(self, y:int, x:int) -> Piece|Empty:
        """ More readable way to return element from a 2d array """
        return self.board_state[y][x]

    def get_index(self, e) -> tuple:
        """ Returns the index of an element in board_state """
        for y, row in enumerate(self.board_state):
            try:
                return y, row.index(e)
            except ValueError:
                continue
        raise NotImplementedError

    def move_piece(self, ny, nx, oy, ox) -> Piece | None:
        """ Swaps 2 elements on the board. If capture happens 1 piece is replaced with Empty()
        Args:
            (oy, ox) old position 
            (ny, nx) new position 
        """
        self.board_state[ny][nx], self.board_state[oy][ox] = self.board_state[oy][ox], self.board_state[ny][nx]
        if self.board_state[oy][ox].name == 'empty':
            return None

        captured_piece = self.board_state[oy].pop(ox)
        self.board_state[oy].insert(ox, Empty())
        return captured_piece

    def chess_to_array(self, coord: str) -> tuple[int, int]:
        """ Turns chess coord to array coord -> (y, x) """
        x_map = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7}
        x = x_map[coord[0]]
        y = -1 * int(coord[1]) + 8         # this fn turns chess y idx to list y idx
        return y, x

    def array_to_chess(self, coord: tuple[int, int]) -> str:
        """ Reverse function to chess_to_array """
        x_map = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H'}
        x = x_map[coord[1]]
        y = 8 - coord[0]
        return f"{x.upper()}{y}"

    def add_captured_piece(self, piece, color):
        self.captured_pieces[color].append(piece)


    def print_captured_pieces(self):
        pass

    def revert_board_state(self):
        pass

    def en_passant(self):
        pass

    def castling(self):
        pass


