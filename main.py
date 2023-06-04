from csv import reader
from board import ChessBoard
from pieces import Piece, Pawn, Rook, Knight, Bishop, Queen, King

# CONSTS
# TODO: Maybe use a Path Object
CSV_FILE = './board_states/board_state.csv'
UPPER_LABEL = " A  B  C  D  E  F  G  H" 

# functions
def fill_pieces(board_list: list[list[str]]) -> list[list[Piece|None]]:
    piece_map = {'P': Pawn, 'R': Rook, 'N': Knight, 'B': Bishop, 'Q': Queen, 'K': King}
    for y, row in enumerate(board_list):
        for x, tile in enumerate(row):
            if tile == '':   
                board_list[y][x] = None
                continue

            if tile[0] == 'w':          
                color = 'white'
            elif tile[0] == 'b':        
                color = 'black'
            board_list[y][x] = piece_map[tile[1]](color)     # Piece(color)
    return board_list

def print_board(board_list: list[list[str]]):
    print(UPPER_LABEL)
    row_num = 8
    for row in board_list:
        for i, item in enumerate(row):
            if not item: item = '<>'
            print(f"{item}", end=' ')
            if len(row) - i == 1:
                print(' ' + str(row_num))
                row_num -= 1
    print(end='\n\n\n')

def highlight_viable_mvs(vector, board_list, y: int, x: int):
    """ Uses a deepcopied list of board_list """
    # TODO: Yoinked from old code not really fitted into new one
    vecy, vecx = vector[0], vector[1]
    board_list[y + vecy][x + vecx] = 'XX'
    fill_pieces(board_list)

def is_valid_coord(coord: str)-> bool:
    """checks if coord is 2 chars long and if 1st is between 'A-H' and 2nd '1-8'. more info: str comparison and ord()"""
    return len(coord) == 2 and 'A' <= coord[0] <= 'H' and '1' <= coord[1] <= '8'

def main():
    ...
    # TODO: Main Menu choose options
    # TODO: Set Opponent AI if exists
    # TODO: Set player1 and player2 colors

    # Game Init 
    # opponent_ai = 'medium'
    player_1 = 'white'
    player_2 = 'black'

    # Load the board        
    with open(CSV_FILE) as csvfile:
        tables = reader(csvfile)
        board_state = [row[:8] for row in tables]
        

    board = ChessBoard(board_state=board_state)
    print_board(board.board_state)

    # run_flag = True
    # while run_flag:

    ## TODO: Use this function to for calculations later 
    # TODO   return [(vector[0] * s, vector[1] * s) for s in range(1, self.scalar+1)]




if __name__ == '__main__':
    main()