import pygame
import pygame.locals
from csv import reader
from board import ChessBoard
from pieces import Piece, Pawn, Rook, Knight, Bishop, Queen, King  #! Needed?


# TODO: Maybe use a Path Object
CSV_FILE = "./board_states/board_state.csv"
piece_symbols = {
    "w": {"P": "♙", "R": "♖", "N": "♘", "B": "♗", "Q": "♕", "K": "♔"},
    "b": {"P": "♟︎", "R": "♜", "N": "♞", "B": "♝", "Q": "♛", "K": "♚"},
}
wht_sqr = "▱"
blk_sqr = "▰"


def print_board(board_state):
    """prints board state on cli with special utf8 chars. alternate_count is used for the pattern on a chess board"""
    alternate_count = 0
    for row in board_state:
        for item in row:
            if item == "":
                print(wht_sqr if alternate_count % 2 == 0 else blk_sqr, end=" ")
                alternate_count += 1
            else:
                print("" + piece_symbols[item[0]][item[1]], end=" ")
        alternate_count -= 1
        print()


# def highlight_viable_mvs(vector, board_list, y: int, x: int):
#     """ Uses a deepcopied list of board_list """
#     #! Yoinked from old code not really fitted into new one
#     vecy, vecx = vector[0], vector[1]
#     board_list[y + vecy][x + vecx] = 'XX'
#     fill_pieces(board_list)


def is_valid_coord(coord: str) -> bool:
    """checks if coord is 2 chars long and if 1st is between 'A-H' and 2nd '1-8'. more info: str comparison and ord()"""
    return len(coord) == 2 and "A" <= coord[0] <= "H" and "1" <= coord[1] <= "8"


def main():
    # TODO: Main Menu choose options
    # TODO: Set Opponent AI if exists
    # TODO: Set player1 and player2 colors

    # Game Init
    # TODO: In the future add maybe com ai
    player_1 = "white"
    player_2 = "black"

    # Load the board
    with open(CSV_FILE, "r") as csvfile:
        tables = reader(csvfile)
        board_state = [row[:8] for row in tables]

    board = ChessBoard()
    board.set_board_state(board_state)

    turn = 0
    run_flag = True
    while run_flag:
        prtable_board_state = board.get_board_state()
        print_board(prtable_board_state)

        # player input
        # check if player input is valid
        #   check if piece is owned by player
        #   check if move is valid one
        #       piece can move there?
        #       does moving create own mate?
        #

        turn += 1
        run_flag = False
    return

    ## TODO: This function down here returns all vectors multiplied with the scalar of a Piece NOT USED for PAWN
    ## TODO: Scalars have been removed from Piece Objects.
    # TODO   return [(vector[0] * s, vector[1] * s) for s in range(1, self.scalar+1)]


if __name__ == "__main__":
    main()
