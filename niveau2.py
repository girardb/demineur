from Minesweeper import Minesweeper


if __name__ == '__main__':
    print("To reveal a tile, use : 'R (x,y)'")
    print("To flag a tile, use : 'F (x,y)'")
    print('Good Luck!\n')
    print('Write the height of the grid.')
    HEIGTH_OF_GRID = int(input())
    print('Write the length of the grid.')
    LENGTH_OF_GRID = int(input())
    print('Write the number of mines in the grid.')
    print("If you write '-1', an appropriate number of mines will be generated for the size of the grid.")
    NUMBER_OF_MINES = int(input())

    if NUMBER_OF_MINES == -1:
        NUMBER_OF_MINES = None
    elif NUMBER_OF_MINES > LENGTH_OF_GRID*HEIGTH_OF_GRID:
        NUMBER_OF_MINES = None
        print("The number you wrote is too large. We'll put the appropriate number of mines in the grid.")

    game = Minesweeper()
    game.play_a_game(LENGTH_OF_GRID, HEIGTH_OF_GRID, NUMBER_OF_MINES)
