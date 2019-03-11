from Minesweeper import Minesweeper

game = Minesweeper()
game.create_board(3, 3, 1)
game.board.create_random_grid()
game.board.print_board_seen_by_user()
game.board.print_board_hidden_from_user()
