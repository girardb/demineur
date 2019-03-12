from Minesweeper import Minesweeper

game = Minesweeper()
game.create_board(9, 9, 3)
game.board.create_random_grid()
game.board.print_board_seen_by_user()
game.board.print_board_hidden_from_user()

here = input()
here = list(here)
x = int(here[0])
y = int(here[1])
game.board.update_board((x,y))
game.board.print_board_seen_by_user()
