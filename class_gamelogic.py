from exceptions import NegIndexError
from main import Player
from pieces_and_board import ChessBoard, ChessPiece


class GameLogic:
    def __init__(self, board: ChessBoard):
        self.board = board

    def is_chess_coord(self, ipt: str) -> bool:
        if len(ipt) == 2 and (97 < ord(ipt.lower()) < 105):
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
        """run self.check_point_oob() before this func"""
        return piece1.color == piece2.color

    # TODO maybe combine get_moves funcs. They share a lot of similarities

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

    def get_pawn_moves(self, piece, vectors, x1, y1) -> list:
        d = 1  # direction the pawn is facing
        if piece.color == "white":
            d = -1
        mv = vectors[0]  # only used for moving forward
        attack_vectors = vectors[1]
        m = []
        s = 1
        while True:
            x2 = x1 + mv[0] * s
            y2 = y1 + mv[1] * s * d
            if self.is_point_oob(x2, y2):
                break

            item = self.board[(x2, y2)]
            if item != None:
                break
            m.append(mv)

            if not piece.moved and s <= 2:
                s += 1
            else:
                break

        for v in attack_vectors:
            x2 = x1 + v[0] * s
            y2 = y1 + v[1] * s * d
            item = self.board[(x2, y2)]
            if self.is_point_oob(x2, y2):
                continue

            if item == None:
                continue

            if not self.is_same_color(item, piece):
                m.append(v)

        return m
