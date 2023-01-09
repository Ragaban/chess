# main game loop
from csv import reader
from board import Board
from pieces import Piece, King, Queen, Bishop, Knight, Rook, Pawn, Empty


def convert_board_elements(board_state: list[list[str]]) -> list[list[Piece|Empty]]:
    """Turns strings in a 2D array into their respective Piece() or Empty().
    """
    piece_map = {'K': King, 'Q': Queen, 'B': Bishop, 'N': Knight, 'R': Rook, 'P': Pawn, '': Empty}
    color_map = {'b': 'black', 'w': 'white'}
    for y, row in enumerate(board_state):
        for x, item in enumerate(row):
            if item == '':  
                board_state[y][x] = piece_map[item]()
            else:
                color = color_map[item[0]]
                board_state[y][x] = piece_map[item[1]](color)
    return board_state

def is_valid_chess_coord(coord: str)-> bool:
    """This func checks if the unicode numbers of the input coord are 
    between 'A'-'H' and '1'-'8'
    """
    return len(coord) == 2 and 'A' <= coord[0] <= 'H' and '1' <= coord[1] <= '8'

def chess_to_array(coord: str) -> tuple[int]:
    """Turns chess coord to array coord -> y, x
    """
    x_map = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7}
    board_x, board_y =  coord[0], int(coord[1])
    x = x_map[board_x]
    y = -1 * board_y + 8         # this fn turns chess y idx to list y idx
    return y, x

def array_to_chess(coord: tuple[int, int]) -> str:
    """Reverse function to chess_to_array"""
    x_map = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H'}
    coord_y, coord_x = coord
    x = x_map[coord_x]
    y = 8 - coord_y
    return f"{x.upper()}{y}"



def main():
    """Main Game Loop and game logic"""
    board_state_filename = 'board_state.csv'

    with open(board_state_filename) as csv_file:
        tables = reader(csv_file)
        board_state_unconverted = [row[:8] for row in tables]   # cutting off excess

    board = Board(convert_board_elements(board_state_unconverted))

    running = True
    while running:

        turn_counter = 1
        board.print_board_state()
        if turn_counter % 2 == 0:
            current_player, opponent  = 'black', 'white'
        else:
            current_player, opponent  = 'white', 'black'

        print(f"Player {current_player.capitalize()} choose a piece to move")
        
        while True:
            # INPUT VALIDATION: is ipt on chess board & players piece
            chess_coord = input("> ").capitalize
            if is_valid_chess_coord(chess_coord):
                oldy, oldx = chess_to_array(chess_coord)
                if board.board_state[oldy][oldx].color == current_player:
                    break
            
        selected_piece: Piece = board.return_element(oldy, oldx)

        while True:
            # INPUT VALIDATION
            print("Where would you like to move?")
            destin_coord = input("> ").capitalize()
            if is_valid_chess_coord(destin_coord):
                newy, newx = chess_to_array(destin_coord)

            
                
            



        break
    return


if __name__ == '__main__':
    main()