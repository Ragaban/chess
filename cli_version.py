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

def convert_to_chess_index(board_pos: str) -> tuple:  
    """Returns -> y, x"""
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

    # this func turns chess board index to lst index
    y = -1 * board_y + 8
    print(f'{board_pos} | ({y}, {x})') # DEBUG: 
    return y, x
    
def move_valid(oldpos, newpos, board) -> bool:
    oy, ox  = oldpos
    ny, nx = newpos
    piece = board[oy][ox]

    if hasattr(piece, "jumps"):
        print("Knight move check not implemented yet")
        return False
    if oldpos == newpos: 
        return False
    #breakpoint()

    ## directions k = (0, 1) and v = bool. If v is untrue this way is blocked and skipped
    directions = {}
    for item in piece.dir:
        directions.setdefault(item, True)
    
    for stp in range(1, piece.range+1):
        for dir in directions:
            if directions[dir] == False:
                continue
            ydir, xdir = dir[0], dir[1]


            try_y, try_x = oy + (ydir*stp), ox + (xdir*stp)
            
            # dont check for negative because then it wraps around the list
            if try_y < 0 or try_x < 0:
                continue
            
            try: # cant check .color if space is empty so check that before
                if board[try_y][try_x] != '<>' and board[try_y][try_x].color == board[oy][ox].color:
                    directions[dir] = False
                    continue
                # If a direction is blocked then that direction should be omitted from the list
                # 

            except IndexError:
                directions[dir] = False
                continue
                # if old pos + direction * step = new pos 
            if oy + (ydir*stp) == ny and ox + (xdir*stp) == nx:
                return True 

    print("Invalid move") # DEBUG:
    return False



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
            y, x = oldpos = convert_to_chess_index(selected_field)
            piece : Piece = current_board[y][x]

            if piece == '<>' or piece.color != current_player[0].lower():
                # check if picked item is empty or player color 
                print('invalid target') # DEBUG
                continue
            
            destination = input(f'Move {piece} ({selected_field}) to: ') # TODO: Input validation
            ny, nx = newpos = convert_to_chess_index(destination)
            if not move_valid(oldpos, newpos, current_board):
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