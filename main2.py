# Chess game in pygame
from csv import reader
from pathlib import Path
import pygame


# Vars & Constants
file_name = "Chess Board.csv"

dark_grey_tile_path = Path('./assets/square gray dark _png_64px.png')
light_grey_tile_path = Path('./assets/square gray light _png_64px.png')




SCREEN_SIZE = WIN_WIDTH, WIN_HEIGHT= (1000, 1000)
BOARD_COLOR = (200, 200, 200)
TILE_LENGTH = 64
TILE_GAP = 1 # 2px between each tile


def main():
    pygame.init()
    # logo = pygame.image.load("logo32x32.png")
    # pygame.display.set_icon(logo)
    pygame.display.set_caption("Chess")

    # main surface object
    main_window = pygame.display.set_mode(SCREEN_SIZE)
    running = True
    board = []

    with open(file_name) as csvfile:
        tables = reader(csvfile)
        for row in tables:
            board.append(row[:8])

    # main loop
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            dark_tile = pygame.image.load(dark_grey_tile_path)
            light_tile = pygame.image.load(light_grey_tile_path)


            # creating the board image
            ac = 0
            for i in range(8):
                for j in range(8):
                    if ac % 2 == 0:
                        main_window.blit(light_tile, (
                            #   this for the gaps           this is so the board is centered in window
                            j * (TILE_LENGTH + TILE_GAP) + (WIN_WIDTH - (TILE_LENGTH * 8 + TILE_GAP * 7)) / 2,
                            i * (TILE_LENGTH + TILE_GAP) + (WIN_HEIGHT - (TILE_LENGTH * 8 + TILE_GAP * 7)) / 2))
                        ac += 1
                    else:
                        main_window.blit(dark_tile, (
                            j * (TILE_LENGTH + TILE_GAP) + (WIN_WIDTH - (TILE_LENGTH * 8 + TILE_GAP * 7)) / 2,
                            i * (TILE_LENGTH + TILE_GAP) + (WIN_HEIGHT - (TILE_LENGTH * 8 + TILE_GAP * 7)) / 2))
                        ac += 1
                ac -= 1     # after each outer loop ac-1 for the alternating pattern between row



            

            pygame.display.update()



if __name__=="__main__":
    main()