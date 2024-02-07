from class_pieces import ChessPiece


class ChessBoard:
    blk_sqr = "■"
    wht_sqr = "□"

    def __init__(self):
        self.board = [
            [None for _ in range(8)] for _ in range(8)
        ]  # 8x8 2d list filled with None

    def __getitem__(self, tup) -> None | ChessPiece:
        """You can add an item by using board[(x, y)]"""
        x, y = tup
        return self.board[y][x]

    def set_item(self, item: ChessPiece | None, x: int, y: int):
        self.board[y][x] = item

    def remove_item(self, x, y) -> ChessPiece | None:
        item = self.board[y].pop(x)
        self.board[y].insert(x, None)
        return item

    def where_is_all(self) -> list:
        all = []
        for y, row in enumerate(self.board):
            for x, piece in enumerate(row):
                if not piece:
                    continue

                all.append(((x, y), piece))
        return all

    def prt_board(self, marked_sqrs=[]):
        # TODO add marked_sqrs for move indication
        print("   A  B  C  D  E  F  G  H\n  ________________________")
        for i, row in enumerate(self.board):
            for j, item in enumerate(row):
                if j == 0:
                    print(f"{8-i}", end="| ")
                if (j, i) in marked_sqrs:
                    print("■", end=" ")
                elif not item:
                    print("□", end=" ")
                else:
                    print(item, end=" ")
            print()
