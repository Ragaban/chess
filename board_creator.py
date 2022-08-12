## create a board state with GUI and save it as a file 
import os
import PySimpleGUI as sg

path = os.path.abspath('./assets/128h')

b_pawn = path + '/' + 'b_pawn_png_128px.png' 
b_rook = path + '/' + 'b_rook_png_128px.png'
b_knight = path + '/' + 'b_knight_png_128px.png'
b_bishop = path + '/' + 'b_bishop_png_128px.png'
b_queen = path + '/' + 'b_queen_png_128px.png'
b_king = path + '/' + 'b_king_png_128px.png'


board = [
    [
        sg.Image(b_rook), sg.Image(b_knight), sg.Image(b_bishop), sg.Image(b_queen), 
        sg.Image(b_king), sg.Image(b_bishop), sg.Image(b_knight), sg.Image(b_rook), 
        ],
    [
        sg.Image(b_pawn), sg.Image(b_pawn), sg.Image(b_pawn), sg.Image(b_pawn), 
        sg.Image(b_pawn), sg.Image(b_pawn), sg.Image(b_pawn), sg.Image(b_pawn), ],
    [],
    [],
    [],
    [],
    [],
    [],
]


layout = [
    board,
    [sg.Button('EXIT', key='-EXIT-')]
    ] 

window = sg.Window('Board Gen', layout)    

while True:
    event, values = window.read()    
    if event in (sg.WIN_CLOSED, '-EXIT-'):
        break


window.close()
print(f'{window} closed')