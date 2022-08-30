from copy import deepcopy
from typing import TypeAlias
from classes import Piece, King, Queen, Bishop, Knight, Rook, Pawn

# vars
padding = '\t\t'    # Just used for cli print
Vector: TypeAlias = tuple[int, int]
ChessArray: TypeAlias = list[list[Piece | str],]

# functions
def get_start_board() -> ChessArray:
    # TODO: Rework loading the board and
    """ creates start board """
    board = [
        [
            Rook('black'), Knight('black'), Bishop('black'), Queen('black'),
            King('black'), Bishop('black'), Knight('black'), Rook('black')
        ],
        [
            Pawn('black'), Pawn('black'), Pawn('black'), Pawn('black'),
            Pawn('black'), Pawn('black'), Pawn('black'), Pawn('black')
        ],
            ['<>','<>','<>','<>','<>','<>','<>','<>'],
            ['<>','<>','<>','<>','<>','<>','<>','<>'],                                                              
            ['<>','<>','<>','<>','<>','<>','<>','<>'],
            ['<>','<>','<>','<>','<>','<>','<>','<>'],
        [
            Pawn('white'), Pawn('white'), Pawn('white'), Pawn('white'),
            Pawn('white'), Pawn('white'), Pawn('white'), Pawn('white')
        ],
        [
            Rook('white'), Knight('white'), Bishop('white'), Queen('white'),
            King('white'), Bishop('white'), Knight('white'), Rook('white')
        ],
    ]
    return board

def draw_board(board) -> None:
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
def belongs_to_player(board: ChessArray, player_color: str, y: int, x: int) -> bool:
    """ Checks if given item in array belongs to given player."""
    if board[y][x] == '<>':
        return False

    elif board[y][x].color != player_color.lower():
        return False

    elif board[y][x].color == player_color.lower():
        return True

    else:
        print("Something happend w/ belongs_to_player()")                   # DEBUG      

# These three are linked
def get_vecs_on_mt_board(board: ChessArray, piece: Piece, oy: int, ox: int,
    ) -> dict:
    """ Returns all possible vectors the given piece has on a empty board
        values are sorted by directions. Each inner list is is in ascending order. """
    
    piece_vectors = {piece: []}
    vectors = piece.my_vectors()

    for v in vectors:
        direction = []
        for s in range(1, piece.range + 1):
            y = v[0] * s
            x = v[1] * s
            
            if ox + x < 0 or oy + y < 0:
                # if x is negative it wraps around list
                break

            if ox + x > 7 or oy + y > 7:
                break

            try:
                if board[oy + y][ox + x]:
                    pass
            except IndexError:
                break

            direction.append((y, x))

        if direction != []:
            piece_vectors[piece].append(direction)

    return piece_vectors

def get_unblocked_vecs(board: ChessArray, vectors: list[list[Vector,]],  
    oy: int, ox: int
    ) -> list[Vector,]:
    """ Check which vectors are unblocked from the given all_free_vectors list
        the given input should look this : [[(...),(...)], [(...),(...)], ... ]
        each inner list represents a directions"""

    unblocked_vectors = []
    for directions in vectors:
        # e.g [(...), (...), ...]
        for vec in directions:
            vecy, vecx = vec
            testy, testx = oy + vecy, ox + vecx
            test_tile = board[testy][testx]

            if testx < 0 or testy < 0:
                # dont check for negative idx 
                continue

            if test_tile == '<>':
                unblocked_vectors.append(vec)
                continue 
            
            if test_tile.color == board[oy][ox].color:
                break
                
            elif test_tile.color != board[oy][ox].color:
                unblocked_vectors.append(vec)
                # cut off here because piece behind them cant be captured
                break

            else:
                print(f"Error: skipped collision")

    return unblocked_vectors
        
def get_pawn_diagonals(board: ChessArray, piece: Piece, oy: int, ox: int) -> list[Vector,]:
    """Returns list of possible capture vectors for a Pawn"""
    capture_vectors = piece.capture_vectors()
    vecs = []
    for cv in capture_vectors:
        try:
            newpos = board[oy + cv[0]][ox + cv[1]]
        except IndexError:
            continue

        if newpos == '<>':
            continue
        
        elif newpos.color != piece.color:
            vecs.append(cv)
        
        else:
            print('Something happend in get_pawn_diagonals()')                    # DEBUG
    return vecs

def all_unblocked_vecs(board) -> dict[Piece, list[Vector]]:
    """ """
    # TODO: Something wrong with Pawns they can capture when the move forward
    all_vecs = {}
    for y, row in enumerate(board):
        for x, tile in enumerate(row):
            if tile == '<>':
                continue

            p = board[y][x]

            piece_vectors = get_vecs_on_mt_board(board, p, y, x)
            unblocked_vecs = get_unblocked_vecs(board, piece_vectors[p], y, x)

            
            if p.name == 'Pawn':
                # Pawns Capture Vecs
                cap_vectors = get_pawn_diagonals(board, p, y, x)

                if cap_vectors != []:
                    unblocked_vecs += cap_vectors

            all_vecs.setdefault(p, unblocked_vecs)

    return all_vecs
    
def get_piece_idx(board: ChessArray, piece) -> tuple[int, int]:
    """ Returns the first occurrence of a piece."""
    for y, row in enumerate(board):
        for x, tile in enumerate(row):
            if piece == tile:
                return y, x

def king_check(board: ChessArray, color: str, all_vecs: dict, king_pos: tuple[int, int]) -> bool:
    """ check if the given KING w/ COLOR is checked by the OPPOSITE COLOR"""
    for k, v in all_vecs.items():
        if k.color == color.lower() or v == []:
            # v == [] means cant move
            continue

        for vec in v:
            y, x = get_piece_idx(board, k)

            if (y + vec[0], x + vec[1]) == king_pos:
                return True

    return False

    












# Board funcs
def highlight_viable_mvs(vectors: tuple[Vector,...], board: ChessArray,
    y: int, x: int,
    ) -> None:
    """ fills all possible tiles where piece can move with XX's
    this function is used later for the GUI"""
    for vector in vectors:
        vecy, vecx = vector[0], vector[1]
        board[y + vecy][x + vecx] = "XX"
    draw_board(board)

def move_piece(board: ChessArray, ny: int, nx: int, oy: int, ox: int) -> Piece | None:
    board[ny][nx], board[oy][ox] = board[oy][ox], board[ny][nx]
    if board[oy][ox] == '<>':
        return None
    captured_piece = board[oy].pop(ox)
    board[oy].insert(ox, '<>')
    return captured_piece
    
#----------------------------------------------------------------------

def main():
    # STAGE 0: Setup
    board = get_start_board()
    captured_pieces = {'White': [], 'Black': []}
    
    while True:
        turn_counter = 1            
        while True:
            # STAGE 1:          Turn Starts
            draw_board(board)
            
            if turn_counter % 2 == 1: 
                current_player = 'White'
                opposite_player = 'Black'
            # odd = White / even = Black
            else: 
                current_player = 'Black'
                opposite_player = 'White'

            # STAGE 2:          Player Picks Piece
            while True:
                selected_tile = input(f"{current_player}'s Turn: " )
                
                if ipt_checker(selected_tile):
                    if selected_tile[0].isdigit(): 
                        selected_tile = selected_tile[1] + selected_tile[0]
                    break

            oy, ox = chess_idx_to_lst(selected_tile)
            if not belongs_to_player(board, current_player, oy, ox):
                print('Invalid target!')
                continue
            
            piece: Piece = board[oy][ox]

            # STAGE 3:          Get All Vectors of All Pieces
            all_vecs = all_unblocked_vecs(board)

            for k, v in all_vecs.items():                                               # DEBUG
                print(k.name + ' ' + k.color.upper(), end= ', ')                        #    
                print(v)                                                                #
            print(f">>>> {all_vecs[piece]}")                                            # DEBUG

            if all_vecs[piece] == []:
                print(f"{piece} can't go anywhere")
                continue

            # STAGE 3.1:        Checking if move creates KING CHECKED
            # Getting King Positions
            for p in all_vecs:
                if p.name == 'King':
                    if p.color == 'white':
                        white_king_pos = get_piece_idx(board, p)
                    else:
                        black_king_pos = get_piece_idx(board, p)









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
            
            # STAGE 5:          Check Move Legality
            if hasattr(piece, "jumps"):
                if belongs_to_player(board, current_player, ny, nx):
                    print(
                        f"{piece} cant mv to {destination.upper()}, one of ur pieces on there"
                        )                                                               # DEBUG
                    continue

            vecy = ny - oy 
            vecx = nx - ox

            if (vecy, vecx) not in all_vecs[piece]:
                print(f"{piece} cannot move there!")                                    # DEBUG
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

            # STAGE 5
            # TODO: create a func that checks if king_checked
            # that function should take the piece and move it to the possible pos
            # AND if any enemy can move to the king discard piece vector
            # Right now you have to recalc all vectors when doing this 
            # so maybe you can calc it only once? Not that big of a priority right now
            # 


            # if king_checked(board, current_player):
            #     print('Check!')

            # Stage 10:          End Step 
            if not piece.first_mv:
                piece.made_first_move()

            turn_counter += 1

        break
    return

if __name__ == "__main__":
    main()