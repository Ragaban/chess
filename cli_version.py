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
    ) -> list[list[list[Vector,],]]:
    """ Returns all possible vectors the given piece has on the board w/o collision
        Return -> list is sorted by directions. Each inner list is is in ascending order. """
    
    board_vectors = []
    vectors = piece.my_vectors()

    for v in vectors:
        direction = []
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
            direction.append((y, x))
        if direction == []:
            continue
        board_vectors.append(direction)
    return board_vectors

def check_path_blocked(vectors: list[list[Vector,]], board: ChessArray, 
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

            if test_tile == '<>':
                unblocked_vectors.append(vec)

            elif (test_tile != '<>'
                    and test_tile.color == board[oy][ox].color):
                break
                
            elif (test_tile != '<>'
                    and test_tile.color != board[oy][ox].color):
                unblocked_vectors.append(vec)

            else:
                print(f"Error: skipped collision")

    return unblocked_vectors
        
def pawn_diag(piece, board, oy, ox) -> list[Vector,]:
    """Returns list of possible capture vectors for a Pawn"""
    capture_vectors = piece.capture_vectors()
    vecs = []
    for cv in capture_vectors:
        newpos = board[oy + cv[0]][ox + cv[1]]
        if newpos == '<>':
            continue
        elif newpos.color == piece.color:
            continue
        elif newpos.color != piece.color:
            vecs.append(cv)
    return vecs
    

def collision_check_knight(piece: Piece, board: ChessArray, ny: int, nx: int
    ) -> bool:
    """ Checks if destination has enemy or is empty"""
    if (board[ny][nx] == '<>' 
            or board[ny][nx].color != piece.color): 
        # new pos empty and enemy there             
        print(f"{piece} no collision {board[ny][nx]}")                      # DEBUG
        return True
    else:
        newpos = lst_idx_to_chess((ny,nx))
        print(
            f"{piece} collison on {board[ny][nx]} {newpos}")                # DEBUG
        return False

def highlight_viable_mvs(vectors: tuple[Vector,...], board: ChessArray,
    y: int, x: int,
    ) -> None:
    """ fills all possible tiles where piece can move with XX's
    this function is used later for the GUI"""
    for vector in vectors:
        vecy, vecx = vector[0], vector[1]
        board[y + vecy][x + vecx] = "XX"
    print("HIGHLIGHT VIABLE MOVES")
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
    # STAGE 0: Initialization
    current_board = get_start_board()
    while True:
        caputured_pieces = {'White': [], 'Black': []}
        turn_counter = 1            # odd White even Black
        while True:
            # STAGE 1:          Beginning of Turn
            draw_board(current_board)
            if turn_counter % 2 == 1: current_player = 'White'
            else: current_player = 'Black'

            # STAGE 2:          Player Grabs Piece
            # TODO: Input validation
            selected_tile = input(f"{current_player}'s Turn: " )
            oy, ox = chess_idx_to_lst(selected_tile)
            piece: Piece = current_board[oy][ox]

            
            # STAGE 2.1:        Validating Grabbed Piece
            if current_board[oy][ox] == '<>':
                print(f"{selected_tile} is empty, choose another field!")
                continue

            if current_board[oy][ox].color != current_player.lower():
                print(f"{current_player}, {piece} does not belong to you!")
                continue
            
            # STAGE 2.2:        Check Where Grabbed Piece Can Move

            all_vecs = all_board_vectors(piece, current_board, oy, ox)
            print(f"all_possible_vecs --> {all_vecs}")                      # DEBUG

            unblocked_vecs = check_path_blocked(all_vecs, current_board, oy, ox)

            # STAGE 2.2.1:      Check Pawns Move Diag Move
            if piece.name == 'Pawn' and piece.fm: 
                cap_vectors = pawn_diag(piece, current_board, oy, ox)
                print(f"Diag Vec: {cap_vectors}")                           # DEBUG
                if cap_vectors != []:
                    unblocked_vecs += cap_vectors

            print(f"these vecs are unblocked: {unblocked_vecs}")            # DEBUG

            if unblocked_vecs == []:
                print(f"{piece} can't go anywhere")
                continue


            test_board = deepcopy(current_board)                            # DEBUG 
            highlight_viable_mvs(unblocked_vecs, test_board, oy, ox)        # AND GUI RELATED

            # STAGE 3:          Player declares destination
            # TODO: Input validation
            destination = input(f'Move {piece} ({selected_tile.upper()}) to: ')
            ny, nx = chess_idx_to_lst(destination)
            vecy, vecx = ny - oy, nx - ox
            vec = (vecy, vecx)
            
            # STAGE 3.2:        Validating Move
            if oy == ny and ox == nx:
                # Not moving is not legal
                continue

            # TODO: Think if this code block is gonna be used later 
            # pawn_diag() not compatible with it and 
            # lst_form_of_av = []        
            # for direction in all_vecs:
            #     for item in direction:
            #         # turns av: list[list[tuple]] -> list[tuple] for comparision
            #         lst_form_of_av.append(item)

            # if vec not in lst_form_of_av:
            #     print(f"{destination.upper()} not in {piece}'s range")
            #     continue

            # Check if knight moved.
            if hasattr(piece, "jumps"):
                if not collision_check_knight(piece, current_board, ny, nx):
                    print(
                        f"{piece} cant mv to {destination.upper()}, one of ur pieces on there"
                        )                                                   # DEBUG
                    continue

            if vec not in unblocked_vecs:
                print(f"{piece} cannot move there!")                                # DEBUG
                continue

            # Stage 4:          Move and Capture
            # TODO: PAWN CLASS NEEDS THE DIAGONAL CAPTURE

            capture = move_piece(current_board, ny, nx, oy, ox)
            if capture is not None:
                caputured_pieces[current_player].append(capture)                
            
            print(caputured_pieces.values())                                # DEBUG

            if not piece.fm:
                # Checks if piece made its first move     
                piece.made_first_move()
            turn_counter += 1

        break
    return

if __name__ == "__main__":
    main()