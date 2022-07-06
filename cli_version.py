from classes import Piece, King, Queen, Bishop, Knight, Rook, Pawn

# vars
padding = '\t\t'

# functions
def get_start_board():
    # TODO: Rework loading the board idk
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
    for y, row in enumerate(board):
        for x, item in enumerate(row):
            if isinstance(item, Piece):
                item.update_pos(x, y)
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
    """ turn chess indices 'D4' to list indices"""
    board_x, board_y = board_pos[0], int(board_pos[1])
    match board_x.lower():
        case 'a': x = 0
        case 'b': x = 1
        case 'c': x = 2
        case 'd': x = 3
        case 'e': x = 4
        case 'f': x = 5
        case 'g': x = 6
        case 'h': x = 7

    # f(x) = -1 * x + 8
    y = -1 * board_y + 8
    return x, y
    
def check_move_legality(newpos, piece : Piece, board) -> bool:
    new_x, new_y = newpos
    old_x, old_y = piece.pos 
    for i, dir in enumerate(piece.pos):
        xrange = piece.range - old_x
        yrange = piece.range - old_y
        #(1, 1), (-1, 1), (1, -1), (-1, -1) Bishop
        for num in range(1, piece.range +1):
            x, y = dir # e.g dir = (1, 1)
            xdir, ydir = x * num, y * num


            if isinstance(board[old_y + ydir][old_x + xdir], Piece) and board[old_y + ydir][old_x + xdir] != board[new_y][new_x]:
                #if tested space is a Piece AND tested space IS NOT destination MEANS BLOCKED WAY
                break

            if board[old_y + ydir][old_x + xdir] == board[new_y][new_x]:
                return True

    return False

def main():
    current_board = get_start_board()
    breakpoint()
    while True:
        turn = 1 # odd turns white & even turns black
        while True: # Player Turn actual main loop
            draw_board(current_board)
            if turn % 2 == 1: current_player = 'White' 
            else: current_player = 'Black'
            
            selected_field = input(f"{current_player}'s Turn: " ) # TODO: Input validation
            x,y = oldpos = convert_to_chess_index(selected_field) 
            piece : Piece = current_board[y][x]

            if piece == '<>' or piece.color != current_player[0].lower():
                print('invalid target') # DEBUG
                continue

            destination = input(f'Where to move: ') # TODO: Input validation
            if destination == selected_field: 
                continue
            newpos = convert_to_chess_index(destination)
            
            if not check_move_legality(newpos, piece, current_board):
                continue

            turn += 1

        # check where piece can move 
        # give options where to move
        # check if move was valid
        # check if new pos is occupied
        # move piece
        # check for win
        
        break

if __name__ == "__main__":
    main()