class Piece:
    def __init__(self, color : str):
        self.color = color
        #self.pos = pos

    def __repr__(self):
        return self.color + self.name[0] 

    def move(self):
        pass

class King(Piece):
    name = "King"

class Queen(Piece):
    name = "Queen"

class Bishop(Piece):
    name = "Bishop"

class Knight(Piece):
    name = "Knight"
    def __repr__(self):
        return self.color + "N"

class Rook(Piece):
    name = "Rook"

class Pawn(Piece):
    name = "Pawn"


chess_board = [
    #a b c d e f g h
    [Rook('b'), Knight('b'), Bishop('b'), Queen('b'), King('b'), Bishop('b'), Knight('b'), Rook('b')],    # 8
    [Pawn('b'), Pawn('b'), Pawn('b'), Pawn('b'), Pawn('b'), Pawn('b'), Pawn('b'), Pawn('b')],               # 7
    ['<>','<>','<>','<>','<>','<>','<>','<>'],                                                              # 6
    ['<>','<>','<>','<>','<>','<>','<>','<>'],                                                              # 5
    ['<>','<>','<>','<>','<>','<>','<>','<>'],                                                              # 4
    ['<>','<>','<>','<>','<>','<>','<>','<>'],                                                              # 3
    [Pawn('w'), Pawn('w'), Pawn('w'), Pawn('w'), Pawn('w'), Pawn('w'), Pawn('w'), Pawn('w')],               # 2
    [Rook('w'), Knight('w'), Bishop('w'), Queen('w'), King('w'), Bishop('w'), Knight('w'), Rook('w')],    # 1
]

padding = '\t\t'


def draw_board(board):
    print( padding + ' A  B  C  D  E  F  G  H')
    row_num = 8
    for row in board:
        print(padding)
        for idx, item in enumerate(row):
            print(item, end=' ')
            if len(row) - idx == 1:
                print(' ' + str(row_num))
                row_num -= 1

def convert_to_chess_index(board_pos: str) -> tuple:
    """ turn chess indices to list board indices"""
    x, y = board_pos[0], int(board_pos[1]) # x y = 'D5'
    match x.lower():
        case 'a': x = 0
        case 'b': x = 1
        case 'c': x = 2
        case 'd': x = 3
        case 'e': x = 4
        case 'f': x = 5
        case 'g': x = 6
        case 'h': x = 7

    # f(x) = -1 * x + 8
    y = -1 * y + 8
    return x, y
    



def move():
    pass

def main():

    while True: # main-game loop
        draw_board(chess_board)
        turn = 1 # odd turns white & even turns black

        while True: # Player Turn
            
            if turn % 2 == 1: current_player = 'White'
            else: current_player = 'Black'
            
            selected_piece = input(f"{current_player}'s Turn: " ) # TODO: Input validation
            x, y = convert_to_chess_index(selected_piece)
            piece = chess_board[y][x]
            if piece != '<>' and piece.color == current_player[0].lower(): # first check for empty space '<>'
                print('valid') # DEBUG
                move()
            else:
                print('invalid') # DEBUG
                continue 
            
            turn += 1

        # check where piece can move 
        # give options where to move
        # check if move was valid
        # check if new pos is occupied
        # move piece


        
        # check for win
        
        break

main()