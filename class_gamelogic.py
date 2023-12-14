import re

from exceptions import NegIndexError
from class_board import ChessBoard


class GameLogic:
    def __init__(self, board: ChessBoard):
        self.board = board
        self.re_coord = re.compile("([a-h]\d|[A-H]\d)")  # matching chess notation

    def is_chess_coord(self, ipt: str) -> bool:
        if self.re_coord.match(ipt):
            return True
        return False

    def is_point_oob(self, x, y) -> bool:
        """oob = Out of Bonds."""
        try:
            if x < 0 or y < 0:
                raise NegIndexError
            self.board[(x, y)]
            return False
        except (IndexError, NegIndexError):
            return True

    def is_same_color(self, color1, color2) -> bool:
        return color1.lower() == color2.lower()

    # TODO maybe combine get_moves funcs. They share a lot of logic

    def get_moves_rbqk(self, piece, vectors, x1, y1):
        m = []
        for v in vectors:
            s = 0  # scalar
            while True:
                s += 1
                x2 = x1 + v[0] * s
                y2 = y1 + v[1] * s
                if self.is_point_oob(x2, y2):
                    break

                test_sqr = self.board[(x2, y2)]

                if test_sqr == None:
                    m.append((v[0] * s, v[1] * s))

                elif not self.is_same_color(test_sqr.color, piece.color):
                    m.append((v[0] * s, v[1] * s))

                else:
                    break

                if piece.type == "King":
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

            elif not self.is_same_color(item.color, piece.color):
                m.append(v)

            else:
                continue
        return m

    def get_moves_pawn(self, piece, x1, y1, s) -> tuple:
        d = piece.direction
        x2 = x1 + 0  # x never changes when moving forward
        y2 = y1 + 1 * d * s
        if self.is_point_oob(x2, y2):
            return []
        return [(0, 1 * d * s)]

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

            if not self.is_same_color(item.color, piece.color):
                m.append(v)
        return m
