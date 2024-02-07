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
        """This func is used for clarity. Some items have color in lowercase some in uppercase"""
        return color1.lower() == color2.lower()

    # TODO maybe combine get_moves funcs. They share a lot of logic

    def is_valid_vector_rbqkn(self, vec, x1, y1, color) -> bool:
        vx, vy = vec[0], vec[1]
        x2, y2 = x1 + vx, y1 + vy

        if self.is_point_oob(x2, y2):
            return False

        test_item = self.board[(x2, y2)]
        if not test_item:
            # vec points to empty space
            return True

        elif not self.is_same_color(test_item.color, color):
            # vec points to enemy piece
            return True

        # vec points to allied piece
        return False

    def is_valid_move_vector_pawn(self, vec, x1, y1) -> bool:
        vx, vy = vec[0], vec[1]
        x2, y2 = x1 + vx, y1 + vy

        if self.is_point_oob(x2, y2):
            return False

        test_item = self.board[(x2, y2)]
        if test_item:
            # vec points to space w/ an piece
            return False
        # vec points to empty space
        return True

    def is_valid_attack_vector_pawn(self, vec, x1, y1, color):
        vx, vy = vec[0], vec[1]
        x2, y2 = x1 + vx, y1 + vy

        if self.is_point_oob(x2, y2):
            return False

        test_item = self.board[(x2, y2)]
        if not test_item:
            # vec points empty space & can only attack enemy diag
            return False

        elif not self.is_same_color(test_item.color, color):
            # vec points to enemy
            return True

        return False
