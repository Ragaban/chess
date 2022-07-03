class Piece:
    def __init__(self, color : str):
        self.color = color
        #self.pos = pos

    def __repr__(self):
        return self.name + self.color

    def move(self):
        pass

class King(Piece):
    name = "K"

class Queen(Piece):
    name = "Q"

class Bishop(Piece):
    name = "B"

class Knight(Piece):
    name = "G"

class Rooke(Piece):
    name = "R"

class Pawn(Piece):
    name = "P"


chess_board = [
    #a b c d e f g h
    [Rooke('b'), Knight('b'), Bishop('b'), Queen('b'), King('b'), Bishop('b'), Knight('b'), Rooke('b')],    # 8
    [Pawn('b'), Pawn('b'), Pawn('b'), Pawn('b'), Pawn('b'), Pawn('b'), Pawn('b'), Pawn('b')],               # 7
    ['<>','<>','<>','<>','<>','<>','<>','<>'],                                                              # 6
    ['<>','<>','<>','<>','<>','<>','<>','<>'],                                                              # 5
    ['<>','<>','<>','<>','<>','<>','<>','<>'],                                                              # 4
    ['<>','<>','<>','<>','<>','<>','<>','<>'],                                                              # 3
    [Pawn('w'), Pawn('w'), Pawn('w'), Pawn('w'), Pawn('w'), Pawn('w'), Pawn('w'), Pawn('w')],               # 2
    [Rooke('w'), Knight('w'), Bishop('w'), Queen('w'), King('w'), Bishop('w'), Knight('w'), Rooke('w')],    # 1
]



def draw_board(board):
    print( ' A  B  C  D  E  F  G  H')
    row_num = 8
    for row in board:
        for idx, item in enumerate(row):
            print(item, end=' ')
            if len(row) - idx == 1:
                print(' ' + str(row_num))
                row_num -= 1



def convert_to_chess_index():
    """ turn list indices to chess board indices"""
    pass


def main():
    player_turn = True # True = P1 False = P2
    
    while True:
        draw_board(chess_board)
        selected_piece = input(': ' )


        
        
        if player_turn: player_turn = False
        else: player_turn = True
        break

main()