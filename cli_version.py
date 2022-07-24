from copy import deepcopy
from typing import TypeAlias
from classes import Piece, King, Queen, Bishop, Knight, Rook, Pawn

# vars
padding = '\t\t'
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


def all_board_vectors( piece: Piece, board: ChessArray, oy: int, ox: int,
    ) -> list[list[tuple[Vector,...],]]:
    """ Returns all possible vectors the given piece has on the board w/o collision
        the list is sorted by directions. Each inner list is is in ascending order. """
    
    board_vectors = []
    for v in piece.vec:
        dir = []
        for s in range(1, piece.range + 1):
            y = v[0] * s
            x = v[1] * s
            
            if ox + x < 0:
                # if x is negative it wraps around list
                continue
            try:
                if board[oy + y][ox + x]:
                    pass
            except IndexError:
                continue
            dir.append((y, x))
        if dir == []:
            continue
        board_vectors.append(dir)
    return board_vectors

def check_path_blocked(vectors: list[list[Vector,]], board: ChessArray, oy: int, ox: int) -> list:
    """ Check which vectors are unblocked from the given all_free_vectors list
        the given input should look this : [[(...),(...)], [(...),(...)], ... ]
        each inner list represents a directions
    """
    unblocked_vectors = []

    for directions in vectors:
        # e.g [(...), (...), ...]
        for vec in directions:
            vecy, vecx = vec
            testy, testx = testyx = oy + vecy, ox + vecx
            test_tile = board[testy][testx]

            if test_tile == '<>':
                unblocked_vectors.append(vec)

            elif test_tile != '<>':
                break

            else:
                print(f"Error: test_tile: {test_tile}, vec: {vec}")

    return unblocked_vectors
        

def collision_check_knight(piece: Piece, board: ChessArray, ny: int, nx: int
    ) -> bool:
    """Checks if destination has enemy or is empty"""
    if (board[ny][nx] == '<>' 
            or board[ny][nx].color != piece.color): 
        # new pos empty and enemy there             
        print(f"{piece} no collision {board[ny][nx]}")      # DEBUG
        return True
    else:
        print(f"{piece} collison on {board[ny][nx]} {lst_idx_to_chess((ny, nx))}")       # DEBUG
        return False

def highlight_viable_mvs(vectors: tuple[Vector,...], board: ChessArray,
    y: int, x: int,
    ) -> None:
    """ fills all possible tiles where piece can move with XX's
    this function is used later for the GUI
    """
    for vector in vectors:
        vecy, vecx = vector[0], vector[1]
        board[y + vecy][x + vecx] = "XX"
    print("HIGHLIGHT VIABLE MOVES")
    draw_board(board)

#----------------------------------------------------------------------

def main():
    # STAGE 0: Initialization
    current_board = get_start_board()
    while True:
        turn_counter = 1            # odd White even Black
        
        while True:
            # STAGE 1: Beginning of Turn
            draw_board(current_board)
            if turn_counter % 2 == 1: current_player = 'White'
            else: current_player = 'Black'

            # STAGE 2: Player Grabs Piece
            # TODO: Input validation
            selected_tile = input(f"{current_player}'s Turn: " )
            oy, ox = chess_idx_to_lst(selected_tile)
            piece: Piece = current_board[oy][ox]

            
            # STAGE 2.1: Validating Piece
            if current_board[oy][ox] == '<>':
                print(f"{selected_tile} is empty, choose another field!")
                continue

            if current_board[oy][ox].color != current_player.lower():
                print(f"{current_player}, {piece} does not belong to you!")
                continue
            
            # STAGE 2.2: Check if piece can move
            all_vecs = all_board_vectors(piece, current_board, oy, ox)
            print(f"all_possible_vecs --> {all_vecs}")        # DEBUG

            unblocked_vecs = check_path_blocked(all_vecs, current_board, oy, ox)
            print(f"these vecs are unblocked: {unblocked_vecs}")      # DEBUG

            if unblocked_vecs == []:
                print(f"{piece} can't go anywhere")
                continue

            test_board = deepcopy(current_board)                            # DEBUG 
            highlight_viable_mvs(unblocked_vecs, test_board, oy, ox)        # AND GUI RELATED

            # STAGE 3: Player Moves Piece
            # TODO: Input validation
            destination = input(f'Move {piece} ({selected_tile.upper()}) to: ')
            ny, nx = chess_idx_to_lst(destination)


            vecy, vecx = ny - oy, nx - ox
            vec = (vecy, vecx)


            newlist = []        # turns av: list[list[tuple]] -> list[tuple] for comparasion
            for direction in all_vecs:
                for item in direction:
                    newlist.append(item)
            
            # STAGE 3.2: Validating Move
            if oy == ny and ox == nx:
            # Not moving is not legal
                continue

            if vec not in newlist:
                print(f"{destination.upper()} not in {piece}'s range")
                continue

            # Check if knight moved.
            if hasattr(piece, "jumps"):
                if not collision_check_knight(piece, current_board, ny, nx):
                    print(
                        f"{piece} cant mv to {destination.upper()}, one of ur pieces on there"
                        )           # DEBUG
                    continue

            if vec not in unblocked_vecs:
                print(f"{piece} is blocked")        # DEBUG
                continue


            # TODO: MOVE FUNCTION AND CAPTURED PIECE
            # TODO: PAWN CLASS NEEDS THE DIAGONAL CAPTURE
            current_board[ny][nx], current_board[oy][ox] = current_board[oy][ox], current_board[ny][nx]


            if not piece.fm:         
                piece.did_first_move()
            turn_counter += 1


        # move piece
        # check for win

        break

if __name__ == "__main__":
    main()