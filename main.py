from classes import Piece, King, Queen, Bishop, Knight, Rook, Pawn
from csv import reader
from typing import TypeAlias
import sys, pygame

Vector: TypeAlias = tuple[int, int]
ChessArray: TypeAlias = list[list[Piece | str],]
SIZE = (1200, 720)





def generate_board() -> ChessArray:
    """ Read a csv file that holds the board state and generates the board"""
    board = []

    with open('Chess Board.csv') as csvfile:
        tables = reader(csvfile)
        for row in tables:
            if len(row) > 8:
                row = row[:8]
            board.append(row)

    for y, row in enumerate(board):
        for x, tile in enumerate(row):
            if tile == '':   
                board[y][x] = '<>'
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

def main():
    pygame.init()
    pygame.display.set_caption("Chess")

    screen = pygame.display.set_mode(SIZE)
    board = generate_board()

    brown_sqr = pygame.image.load("assets/128h/square brown dark_png_128px.png")
    brown_sqr = pygame.transform.scale(brown_sqr, (64, 64))
    b_bishop = pygame.image.load("assets/128h/b_bishop_png_128px.png")

    # GAME LOOP
    while True:
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                sys.exit()


            pygame.display.flip()       # update screen


if __name__ == "__main__":
    main()
