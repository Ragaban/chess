from copy import deepcopy
from csv import reader
from typing import TypeAlias

from classes import Piece, King, Queen, Bishop, Knight, Rook, Pawn, Empty, Marked

# vars
PADDING = '\t\t'    # Just used for cli print
Vector: TypeAlias = tuple[int, int]
ChessArray: TypeAlias = list[list[Piece | Empty],]




# functions
def generate_board(board) -> ChessArray:
    """ Read a csv file that holds the board state and generates the board"""
    piece_map = {'P': Pawn, 'R': Rook, 'N': Knight, 'B': Bishop, 'Q': Queen, 'K': King, '': Empty}
    for y, row in enumerate(board):
        for x, tile in enumerate(row):
            if tile == '':   
                board[y][x] = Empty()
                continue

            if tile[0] == 'w':          
                color = 'white'
            elif tile[0] == 'b':        
                color = 'black'

            board[y][x] = piece_map[tile[1]](color)

    return board

def draw_board(board):
    """ print out chess board in a nice way """
    print(end='\n\n\n')
    print(PADDING + ' A  B  C  D  E  F  G  H')
    row_num = 8
    for row in board:
        print(PADDING, end='')
        for idx, item in enumerate(row):
            print(item, end=' ')
            if len(row) - idx == 1:
                print(' ' + str(row_num))
                row_num -= 1

# Input funcs
def ipt_checker(string) -> bool:
    """ Checks if given string matches chess idx. """
    if len(string) != 2:
        return False

    if (string.isalnum()
            and not string.isdigit()
            and not string.isalpha()
        ):
        return True
    else:
        print('Something happend with ipt_checker()')
        return

def chess_idx_to_lst(board_pos: str) -> tuple:
    """ Converts chess board index to list index. Given arg needs this form "DIGIT/LETTER" """
    x_map = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
    board_y, board_x =  int(board_pos[1]), board_pos[0]
    x = x_map[board_x]
    y = -1 * board_y + 8         # this fn turns chess y idx to list y idx
    
    print(f'{board_pos} | ({y}, {x})')          # DEBUG
    return y, x

def lst_idx_to_chess(idx: tuple[int, int]) -> str:
    """ Reverse function to chess_idx_to_list(). Given arg needs this form "DIGIT/LETTER" """
    x_map = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
    lst_y, lst_x = idx
    x = x_map[lst_x]
    y = 8 - lst_y
    return f"{x.upper()}{y}"

# Piece funcs
def belongs_to_player(player_color: str, piece: Piece) -> bool:
    """ Checks if given item in array belongs to given player."""
    if piece.color == player_color.lower():
        return True
    elif piece.name == 'empty':
        return False
    elif piece.color != player_color.lower():
        return False

def discard_vecs_outside_board(piece: Piece, pos_y: int, pos_x: int) -> list[Vector]:
    """ Vectors that lead out of board are discarded """
    vectors = []        # all possible vectors on an empty board
    piece_vecs = piece.my_vectors()
    for vec in piece_vecs:
        for step in range(1, piece.range + 1):
            vec_y = step * vec[0]
            vec_x = step * vec[1]

            if pos_y + vec_y < 0 or pos_x + vec_x < 0:          # cycles around list
                break       
            if pos_y + vec_y > 7 or pos_x + vec_x > 7:          # 8 or higher -> IndexError 
                break

            vectors.append((vec))
    return vectors

def test_vectors(board: ChessArray, pos_y, pos_x, vecs) -> list[Vector]:
    """ Iterates through given vecs and returns list of vecs that are viable"""
    possible_vectors = []
    piece = board[pos_y][pos_x]
    for vec in vecs:
        vec_y, vec_x = vec
        new_pos_y, new_pos_x = pos_y + vec_y, pos_x + vec_x
        test_tile = board[new_pos_y][new_pos_x]

        # Knight Special Case
        if piece.name == 'Knight':
            if piece.color != test_tile.color:
                possible_vectors.append((vec))
                continue
            continue
        
        if test_tile.name != 'empty':                   # empty spots are class Empty with name "empty"
            if piece.color != test_tile.color:              # AND diff color
                if piece.name == 'Pawn':                        # BUT Pawn cant capture
                    break                                           # next direction
                possible_vectors.append((vec))         # capture enemy
                break                                           # next direction
            else:                                           # AND same color
                break                                           # next direction

        if test_tile.name == 'empty':
            possible_vectors.append((vec))
            continue

    return possible_vectors

def get_piece_idx(board: ChessArray, piece) -> tuple[int, int]:
    """ Returns the coord of a piece."""
    for y, row in enumerate(board):
        for x, tile in enumerate(row):
            if piece == tile:
                return y, x

def king_check(board: ChessArray, color: str, all_vecs: dict, king_pos: tuple[int, int]) -> bool:
    """ Checks if the given KING w/ COLOR is checked by the OPPOSITE COLOR"""
    # BUG: Doesnt Work somehow
    for piece, vecs in all_vecs.items():
        if piece.color == color.lower():
            continue

        for vec in vecs:
            y, x = get_piece_idx(board, piece)

            if (y + vec[0], x + vec[1]) == king_pos:
                return True
    return False


# Board funcs
def highlight_viable_mvs(vectors: tuple[Vector], board: ChessArray,y: int, x: int,):
    """ fills all possible tiles where piece can move with XX's
    this function is used later for the GUI"""
    for vector in vectors:
        vecy, vecx = vector[0], vector[1]
        board[y + vecy][x + vecx] = Marked()
    draw_board(board)

def move_piece(board: ChessArray, ny: int, nx: int, oy: int, ox: int) -> Piece | None:
    """ Moves 2 elements on the board. 
        If capture happens 1 piece is replaced with empty field '<>'"""
    board[ny][nx], board[oy][ox] = board[oy][ox], board[ny][nx]
    if board[oy][ox].name == 'empty':
        return None
    captured_piece = board[oy].pop(ox)
    board[oy].insert(ox, Empty())
    return captured_piece
    
#----------------------------------------------------------------------

def main():
    # STAGE 0: Setup
    file_name = 'Chess Board.csv'
    csv_board = []
    with open(file_name) as csvfile:
        tables = reader(csvfile)
        for row in tables:
            if len(row) > 8:
                row = row[:8]           # Cuts excess in the csv file
            csv_board.append(row)

    board = generate_board(csv_board)
    captured_pieces = {'White': [], 'Black': []}

    while True:
        # Stage 1:          Game Starts
        turn_counter = 1
        last_moves = []
        
        while True:
            # STAGE 1.1:          Turn Starts
            draw_board(board)
            
            if turn_counter % 2 == 1: 
                current_player = 'White'
                opposite_player = 'Black'
            else:
                current_player = 'Black'
                opposite_player = 'White'

            while True:
                # STAGE 2:          Player Picks Piece
                selected_tile = input(f"{current_player}'s Turn: " )
                if ipt_checker(selected_tile):
                    if selected_tile[0].isdigit(): 
                        # formatting e.g: 4A -> A4
                        selected_tile = selected_tile[1] + selected_tile[0]
                    break

            oy, ox = chess_idx_to_lst(selected_tile)
            if not belongs_to_player(current_player, board[oy][ox]):
                print('Invalid target!')
                continue
            
            piece: Piece = board[oy][ox]

            # STAGE 3:          Get All Vectors of All Pieces
            all_vecs = {}
            for pos_y, row in enumerate(board):
                for pos_x, tile in enumerate(row):
                    if tile.name == 'empty':
                        continue
                    if tile.name == 'King':
                        # USED FOR LATER when checking CHECK/CHECKMATE
                        if tile.color == 'white':
                            white_king_pos = pos_y, pos_x
                        else:
                            black_king_pos = pos_y, pos_x
                    
                    curnt_piece = board[pos_y][pos_x]           # curnt == current
                    curnt_piece_vecs = discard_vecs_outside_board(curnt_piece, pos_y, pos_x)
                    possible_vecs = test_vectors(board, pos_y, pos_x, curnt_piece_vecs)
                    all_vecs.update({curnt_piece: possible_vecs})

            for p, v in all_vecs.items():
                print(f"{p.name}|{p.color.upper()} : {v}")                                                                                                 

            if all_vecs[piece] == []:
                print(f"{piece} can't go anywhere")
                continue

            # STAGE 3.1:        Move Legality: Does MOVE create self check?
            # Running Throught all ally vecs 
            # STAGE 3.2:        Highlight Possible Moves        
            copied_board = deepcopy(board)                                                # DEBUG 
            highlight_viable_mvs(all_vecs[piece], copied_board, oy, ox)

            # STAGE 4:          Player Declares Destination
            while True:
                destination = input(f'Move {piece} ({selected_tile.upper()}) to: ')

                if ipt_checker(destination):
                    if destination[0].isdigit():
                        destination = destination[1] + destination[0]
                    
                    if selected_tile == destination:
                        print('You cannot not move!')
                        continue

                    break

            ny, nx = chess_idx_to_lst(destination)
            
            # STAGE 5:          Check Move Legality         # TODO: Redundant? coz of func get_piece_vectors
            if hasattr(piece, "jumps"):
                if belongs_to_player(current_player, board[ny][nx]):
                    print(
                        f"{piece} cant mv to {destination.upper()}, one of ur pieces on there"
                        )                                                               # DEBUG
                    continue

            vecy = ny - oy 
            vecx = nx - ox

            if (vecy, vecx) not in all_vecs[piece]:
                print(f"{piece} cannot move there!")
                continue

            # STAGE 6:          Move and Capture
            capture = move_piece(board, ny, nx, oy, ox)

            if capture is not None:
                captured_pieces[current_player].append(capture)                
            
            for i in captured_pieces[current_player]:
                print(i, end=' ')                                                       # DEBUG

            if current_player == 'White':
                king_pos = black_king_pos
            else: 
                king_pos = white_king_pos
            


            if king_check(board, opposite_player, all_vecs, king_pos):
                print("KING IS CHECKED")


            # Stage 10:          End Step 
            if not piece.first_mv:
                piece.made_first_move()

            last_moves.append(((oy, ox), (ny, nx)))         # used to revert moves
            turn_counter += 1

        break
    return

if __name__ == "__main__":
    main()