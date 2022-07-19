from locale import normalize
from shutil import move
from classes import Piece, King, Queen, Bishop, Knight, Rook, Pawn

# vars
padding = '\t\t'

# functions
def get_start_board():
    # TODO: Rework loading the board and
    """creates start board"""
    board = [
    [Rook('b'), Knight('b'), Bishop('b'), Queen('b'), King('b'), Bishop('b'), Knight('b'), Rook('b')],      # 8
    [Pawn('b'), Pawn('b'), Pawn('b'), Pawn('b'), Pawn('b'), Pawn('b'), Pawn('b'), Pawn('b')],               # 7
    ['<>','<>','<>','<>','<>','<>','<>','<>'],                                                              # 6
    ['<>','<>','<>','<>','<>','<>','<>','<>'],                                                              # 5
    ['<>','<>','<>','<>','<>','<>','<>','<>'],                                                              # 4
    ['<>','<>','<>','<>','<>','<>','<>','<>'],                                                              # 3
    [Pawn('w'), Pawn('w'), Pawn('w'), Pawn('w'), Pawn('w'), Pawn('w'), Pawn('w'), Pawn('w')],               # 2
    [Rook('w'), Knight('w'), Bishop('w'), Queen('w'), King('w'), Bishop('w'), Knight('w'), Rook('w')],      # 1
    ]
    # OLD: used when Piece had attr posx posy
    # for y, row in enumerate(board):
    #     for x, item in enumerate(row):
    #         if isinstance(item, Piece):
    #             item.update_pos(x, y)
    return board

def draw_board(board):
    """draws board on std oupt"""
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
    """Returns -> list index y, x"""
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

    # this func turns chess board y index to lst y index
    y = -1 * board_y + 8
    print(f'{board_pos} | ({y}, {x})') # DEBUG: 
    return y, x
    
def lst_idx_to_chess(idx):
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
    return y, x

def check_colinearity(piece : Piece, oy: int, ox: int, ny: int, nx: int) -> bool:
    """
    checks if one vector in piece.vec is colinear to the vector of point piece to point destination.
    PS: Ask EYDEE how he would do this function. Problem: dont want to use cls method active_move to pseudo return vec
    """
    # TODO: Implement Knight moveset
    vecy = ny - oy
    vecx = nx - ox
    for scalar in range(1, piece.range+1):
        vec = (vecy/scalar, vecx/scalar)
        if vec in piece.vec:
            vec = (int(vecy/scalar), int(vecx/scalar)) # convert it to int because list indices later
            piece.active_move(vec)
            print("vec found! active_move called") # DEBUG
            return True
    print("vec not found! Invalid move") # DEBUG
    return False
    
def check_collision(piece : Piece, board : list[list[any]], oy : int, ox : int, ny : int, nx : int) -> bool:
    """ check_collision takes the self.active_vec from piece and checks if any pieces are in its way
        to its destination   
    """
    # TODO: find a better way to store the valid vec in the fn check_colineartiy() and giving 
    if hasattr(piece, "jumps"):
        piece.rm_active_vec() # not used by the stupid Knight
        if board[ny][nx] == '<>' or board[ny][nx].color != piece.color:
            
            return True
        else: 
            return False
        

    vecy, vecx = move_vec = piece.active_vec # eg move_vec = (0, 4) or (3, 3)
    piece.rm_active_vec()
    # we just have to iterate the amount of the highest num in move_vec
    # set comprehension down there gets the highest num from a tuple with 0 in it or with 2 same values
    for stp in range(1, piece.range+1):
        try_y, try_x = oy + (vecy*stp), ox + (vecx*stp)
        tryyx = try_y, try_x
        newpos = ny, nx
        # next step empty AND NOT destination -> NEXT TILE
        if board[try_y][try_x] == '<>' and tryyx != newpos:
            print(f"this tile is {board[try_y][try_x]}") # DEBUG
            continue
        # next step a piece AND NOT destination -> BLOCKED
        if board[try_y][try_x] != '<>' and tryyx != newpos:
            print(f"the path is blocked by {board[try_y][try_x]} at {lst_idx_to_chess((try_y, try_x))}") # DEBUG
            return False # BLOCKED
        # next step empty AND destination -> REACHED DESTINATION
        elif board[try_y][try_x] == '<>' and tryyx == newpos:
            print(f"REACHED DESTINTY at {lst_idx_to_chess((try_y, try_x))}") # DEBUG
            return True
        # next step a piece AND destination AND piece has diff color -> REACHED DESTINATION AND KILLS ENEMY
        elif board[try_y][try_x] != '<>' and try_y == ny and try_x == ny and board[try_y][try_x].color != piece.color:
            print(f"Captured enemy piece at {lst_idx_to_chess((try_y, try_x))}")
            return True

def main():
    current_board = get_start_board()
    #breakpoint() #DEBUG
    while True:
        turn_counter = 1 # odd turns white & even turns black
        while True: 
            # Player Turn actual main loop
            draw_board(current_board)
            if turn_counter % 2 == 1: current_player = 'White' 
            else: current_player = 'Black'
            
            selected_field = input(f"{current_player}'s Turn: " ) # TODO: Input validation
            y, x = chess_idx_to_lst(selected_field)
            piece : Piece = current_board[y][x]
            # check if right piece is grabbed
            if piece == '<>' or piece.color != current_player[0].lower():
                print('invalid target') # DEBUG
                continue
            
            destination = input(f'Move {piece} ({selected_field}) to: ') # TODO: Input validation
            ny, nx = chess_idx_to_lst(destination)
            # check move validity
            if y == ny and x == nx:
                continue
            if not check_colinearity(piece, y, x, ny, nx):
                print(f"{piece} on {selected_field} can't move to {destination}") # DEBUG
                continue
            if not check_collision(piece, current_board, y, x, ny, nx):
                continue

            current_board[ny][nx], current_board[y][x] = current_board[y][x], current_board[ny][nx]
            
            draw_board
            turn_counter += 1

        # check where piece can move 
        # give options where to move
        # check if move was valid
        # check if new pos is occupied
        # move piece
        # check for win
        
        break

if __name__ == "__main__":
    main()