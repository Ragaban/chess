# main game loop
from csv import reader
from board import ChessBoard
from pieces import Piece, King, Queen, Bishop, Knight, Rook, Pawn, Empty


def convert_board_elements(board_state: list[list[str]]) -> list[list[Piece|Empty]]:
    """ Turns strings in a 2D array into their respective objs (Piece and Empty) """
    piece_map = {'K': King, 'Q': Queen, 'B': Bishop, 'N': Knight, 'R': Rook, 'P': Pawn, '': Empty}
    color_map = {'b': 'black', 'w': 'white'}
    for y, row in enumerate(board_state):
        for x, item in enumerate(row):

            if item == '':  
                board_state[y][x] = piece_map[item]()   # Empty no color needed

            else:
                color = color_map[item[0]]
                board_state[y][x] = piece_map[item[1]](color)

    return board_state

def is_valid_chess_coord(coord: str)-> bool:
    """ This func checks if the unicode numbers of the input coord are between 'A'-'H' and '1'-'8' """
    return len(coord) == 2 and 'A' <= coord[0] <= 'H' and '1' <= coord[1] <= '8'



def main():
    """ Main Game Loop and game logic """
    board_state_filename = 'board_state.csv'

    with open(board_state_filename) as csv_file:
        tables = reader(csv_file)
        board_state_unconverted = [row[:8] for row in tables]

    board = ChessBoard(convert_board_elements(board_state_unconverted))
    turn_counter = 1
    
    running = True
    while running:

        print(turn_counter)
        board.print_board_state()

        if turn_counter % 2 == 0:
            current_player, opponent  = 'black', 'white'
        else:
            current_player, opponent  = 'white', 'black'

        print(f"Player {current_player.capitalize()} choose a piece")
        
        while True:
            # INPUT VALIDATION: is ipt on chess board & players piece
            chess_coord = input(">> ").capitalize()
            if is_valid_chess_coord(chess_coord):
                oldy, oldx = board.chess_to_array(chess_coord)
                if board.board_state[oldy][oldx].color == current_player:
                    break
                print("XX")

        selected_piece: Piece = board.return_element(y=oldy, x=oldx)

        # This code block calculates every legal vector on the board
        pieces_and_vectors = {}
        for row in board.board_state:
            for piece in row:
                if piece.name == 'empty':
                    continue

                y, x = board.get_index(piece)
                piece_vectors = []
                for base_vector in piece.vectors:           # loop is for a direction (0,1)->(0,7) easier to cutoff
                    for vector in piece.get_scalarized_vectors(base_vector):      # Loop over a DIRECTION IMPORTANT
                        ny, nx = y + vector[0], x + vector[1]

                        if ny not in range(8) or nx not in range(8):        # discard vecs out of bounds
                            continue

                        if isinstance(piece, Pawn):
                            if board.board_state[ny][nx].color == None:
                                piece_vectors.append(vector)
                                continue
                            else: 
                                break      # cant capture with base vectors

                        elif board.board_state[ny][nx].color != piece.color:
                            piece_vectors.append(vector)
                            if board.board_state[ny][nx].color == None:
                                continue        # fetch next vec in this direction
                            else: 
                                break         # enemy captured finished

                        break           # this direction is finished

                pieces_and_vectors.update({piece: piece_vectors})

        [print(f"{k} -> {v}") for k,v in pieces_and_vectors.items()]    # DEBUG

        if not pieces_and_vectors[selected_piece]:
            # no moves == []
            continue

        highlights = [(v[0] + oldy, v[1] + oldx) for v in pieces_and_vectors[selected_piece]]
        board.print_board_state(highlights=highlights)


        while True:
            # INPUT VALIDATION
            # NOTE: Should i check if chess_coord == destin_coord here?
            print(f"{chess_coord} ->")
            destin_coord = input(">> ").capitalize()
            if is_valid_chess_coord(destin_coord):
                newy, newx = board.chess_to_array(destin_coord)
                break
            elif destin_coord == chess_coord:
                print("XX")
                continue
            print("XX")

        selected_move = (newy - oldy, newx - oldx)




        if selected_move not in pieces_and_vectors[selected_piece]:
            print(f"{selected_piece} cannot move there.")
            continue
        
        captured_piece = board.move_piece(ny=newy, nx=newx, ox=oldx, oy=oldy)
            
        if captured_piece:
            board.add_captured_piece(captured_piece, current_player)

        turn_counter += 1

    return


if __name__ == '__main__':
    main()