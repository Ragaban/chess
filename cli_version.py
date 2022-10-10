from copy import deepcopy
from csv import reader
from typing import TypeAlias

from classes import Piece, King, Queen, Bishop, Knight, Rook, Pawn, Empty, Marked

# vars
padding = '\t\t'    # Just used for cli print
Vector: TypeAlias = tuple[int, int]
ChessArray: TypeAlias = list[list[Piece | Empty],]

# functions
def generate_board() -> ChessArray:
    """ Read a csv file that holds the board state and generates the board"""
    # TODO: check for corrupted conditions -> if tile[1] == '?' what then
    board = []

    with open('Chess Board.csv') as csvfile:           # OG FILE NAME 'Chess Board.csv'
        tables = reader(csvfile)
        for row in tables:
            if len(row) > 8:
                row = row[:8]
            board.append(row)

    for y, row in enumerate(board):
        for x, tile in enumerate(row):
            if tile == '':   
                board[y][x] = Empty()
                continue

            if tile[0] == 'w':          
                col = 'white'
            elif tile[0] == 'b':        
                col = 'black'

            if tile[1] == 'P':      
                board[y][x] = Pawn(col)
                continue
            elif tile[1] == 'R':    
                board[y][x] = Rook(col)
                continue
            elif tile[1] == 'N':    
                board[y][x] = Knight(col)
                continue
            elif tile[1] == 'B':    
                board[y][x] = Bishop(col)
                continue
            elif tile[1] == 'Q':    
                board[y][x] = Queen(col)
                continue
            elif tile[1] == 'K':    
                board[y][x] = King(col)
                continue
    return board

def draw_board(board):
    """ print out chess board in a nice way """
    print(end='\n\n\n')
    print( padding + ' A  B  C  D  E  F  G  H')
    row_num = 8
    for row in board:
        print(padding, end='')
        for idx, item in enumerate(row):
            print(item, end=' ')
            if len(row) - idx == 1:
                print(' ' + str(row_num))
                row_num -= 1

# Input funcs
def ipt_checker(string) -> bool:
    """ checks if given string matches chess idx"""
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
    """ Converts chess board index to list index """
    board_y, board_x =  int(board_pos[1]), board_pos[0]
    match board_x.lower():
        case 'a': x = 0
        case 'b': x = 1
        case 'c': x = 2
        case 'd': x = 3
        case 'e': x = 4
        case 'f': x = 5
        case 'g': x = 6
        case 'h': x = 7

    # this func turns chess board y index to list y index
    y = -1 * board_y + 8
    print(f'{board_pos} | ({y}, {x})')          # DEBUG:
    return y, x

def lst_idx_to_chess(idx: tuple[int, int]) -> str:
    """ Reverse function to chess_idx_to_list() """
    lst_y, lst_x = idx
    match lst_x:
        case 0: x = 'a'
        case 1: x = 'b'
        case 2: x = 'c'
        case 3: x = 'd'
        case 4: x = 'e'
        case 5: x = 'f'
        case 6: x = 'g'
        case 7: x = 'h'

    y = 8 - lst_y
    return f"{x.upper()}{y}"

# Piece funcs
def belongs_to_player(
    board: ChessArray, 
    player_color: str, 
    y: int, x: int
) -> bool:
    """ Checks if given item in array belongs to given player."""
    if board[y][x].name == 'empty':
        return False

    elif board[y][x].color != player_color.lower():
        return False

    elif board[y][x].color == player_color.lower():
        return True


def get_piece_vectors(board: ChessArray, piece: Piece, oy: int, ox: int) -> list[Vector]:
    legal_vectors = []
    piece_vecs = piece.my_vectors()
    if piece.name == 'Pawn':
        cap_vec = piece.capture_vectors()

    for vec in piece_vecs:
        for step in range(1, piece.range + 1):
            ny = step * vec[0]
            nx = step * vec[1]
            testy, testx = oy + ny, ox + nx

            if testy < 0 or testx < 0:          # wraps around list
                break       
            if testy > 7 or testx > 7:          # 8 or higher -> IndexError 
                break
            
            test_tile = board[testy][testx]

            # Knight Special Case
            if piece.name == 'Knight':
                if piece.color != test_tile.color:
                    legal_vectors.append((ny, nx))
                    continue
                
            if test_tile.name != 'empty':                   # next tile not empty
                if piece.color != test_tile.color:              # AND diff color
                    if piece.name == 'Pawn':                        # BUT Pawn cant capture
                        break                                           # next direction
                    legal_vectors.append((ny, nx))               # capture enemy
                    break                                           # next direction
                else:                                           # AND same color
                    break                                           # next direction

            if test_tile.name == 'empty':
                legal_vectors.append((ny, nx))
                continue
            
    #TODO Pawn Capture Vectors

    return {piece: legal_vectors}




def get_piece_idx(board: ChessArray, piece) -> tuple[int, int]:
    """ Returns the coord of a piece."""
    for y, row in enumerate(board):
        for x, tile in enumerate(row):
            if piece == tile:
                return y, x

def king_check(
    board: ChessArray, 
    color: str, 
    all_vecs: dict, 
    king_pos: tuple[int, int]
) -> bool:
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
def highlight_viable_mvs(
    vectors: tuple[Vector,...], 
    board: ChessArray,
    y: int, 
    x: int,
):
    """ fills all possible tiles where piece can move with XX's
    this function is used later for the GUI"""
    for vector in vectors:
        vecy, vecx = vector[0], vector[1]
        board[y + vecy][x + vecx] = Marked()
    draw_board(board)

def move_piece(
    board: ChessArray, 
    ny: int, 
    nx: int, 
    oy: int, 
    ox: int
) -> Piece | None:
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
    board = generate_board()
    captured_pieces = {'White': [], 'Black': []}
    while True:
        turn_counter = 1
        last_moves = []   
        while True:
            # STAGE 1:          Turn Starts
            draw_board(board)
            
            if turn_counter % 2 == 1: 
                current_player = 'White'
                opposite_player = 'Black'
            else: 
                current_player = 'Black'
                opposite_player = 'White'

            # STAGE 2:          Player Picks Piece
            while True:
                selected_tile = input(f"{current_player}'s Turn: " )
                
                if ipt_checker(selected_tile):
                    if selected_tile[0].isdigit(): 
                        # formatting e.g: 4A -> A4
                        selected_tile = selected_tile[1] + selected_tile[0]
                    break

            oy, ox = chess_idx_to_lst(selected_tile)
            if not belongs_to_player(board, current_player, oy, ox):
                print('Invalid target!')
                continue
            
            piece: Piece = board[oy][ox]

            # STAGE 3:          Get All Vectors of All Pieces
            all_vecs = {}
            for y, row in enumerate(board):
                for x, tile in enumerate(row):
                    if tile.name == 'empty':
                        continue

                    if tile.name == 'King':
                        # USED FOR LATER when checking CHECK/CHECKMATE
                        if tile.color == 'white':
                            white_king_pos = y, x
                        else:
                            black_king_pos = y, x
                    
                    p = board[y][x]
                    p_vecs = get_piece_vectors(board, p, y, x)


                    all_vecs.update(p_vecs)


            for k, v in all_vecs.items():                                               # DEBUG
                print(k.name + ' ' + k.color.upper(), end= ', ')                        #    
                print(v)                                                                #
            print(f"{piece} >>>> {all_vecs[piece]}")                                    # DEBUG

            if all_vecs[piece] == []:
                print(f"{piece} can't go anywhere")
                continue

            # STAGE 3.1:        Move Legality: Does MOVE create self check?
            # Running Throught all ally vecs 




            # STAGE 3.2:        Highlight Possible Moves        
            test_board = deepcopy(board)                                                # DEBUG 
            highlight_viable_mvs(all_vecs[piece], test_board, oy, ox)

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
                if belongs_to_player(board, current_player, ny, nx):
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