from exceptions import NegIndexError
from pieces_and_board import ChessBoard


class GameLogic:
    def __init__(self, board: ChessBoard):
        self.board = board

    def is_chess_coord(self, ipt: str) -> bool:
        if len(ipt) == 2:
            return True
        if 97 < ord(ipt[0].lower()) < 105:
            return True
        if 49 < ord(ipt[1]) < 57:
            return True
        return False

    def is_point_oob(self, x, y) -> bool:
        """oob = Out of Bonds"""
        try:
            if x < 0 or y < 0:
                raise NegIndexError
            self.board[(x, y)]
            return False
        except (IndexError, NegIndexError):
            return True

    def is_same_color(self, piece1, piece2) -> bool:
        return piece1.color == piece2.color

    # TODO maybe combine get_moves funcs. They share a lot of logic

    def get_moves_rbqk(self, piece, vectors, x1, y1):
        m = []
        for v in vectors:
            s = 0  # scalar
            while True:
                s += 1
                x2, y2 = x1 + v[0] * s, y1 + v[1] * s
                if self.is_point_oob(x2, y2):
                    break

                item = self.board[(x2, y2)]

                if item == None:
                    m.append(v)

                elif not self.is_same_color(item, piece):
                    m.append(v)

                else:
                    break

                if not piece.ranged:  # only for king
                    break

        return m

    def get_moves_knight(self, piece, vectors, x1, y1) -> list:
        m = []
        for v in vectors:
            x2, y2 = x1 + v[0], y1 + v[1]
            if self.is_point_oob(x2, y2):
                continue

            item = self.board[(x2, y2)]

            if item == None:
                m.append(v)

            elif not self.is_same_color(item, piece):
                m.append(v)

            else:
                continue
        return m

    def get_moves_pawn(self, piece, v, x1, y1) -> list:
        d = piece.direction
        m = []
        for s in range(1, 3):
            x2 = x1 + v[0] * s
            y2 = y1 + v[1] * s * d
            if self.is_point_oob(x2, y2):
                break

            item = self.board[(x2, y2)]
            if item != None:
                break
            m.append(v)

            if piece.first_move:
                break
        return m

    def get_attack_moves_pawn(self, piece, vectors, x1, y1) -> list:
        d = piece.direction
        m = []
        for v in vectors:
            x2 = x1 + v[0]
            y2 = y1 + v[1] * d

            if self.is_point_oob(x2, y2):
                continue
            item = self.board[(x2, y2)]

            if item == None:
                continue

            if not self.is_same_color(item, piece):
                m.append(v)
        return m
