from Board import Board

class Minesweeper:
    def __init__(self):
        self.board = None

    def play_a_game(self, grid_length=9, grid_height=9, number_of_mines=None):
        self.board = Board(grid_length, grid_height, number_of_mines)
        self.board.create_random_grid()
        print(f'\nFlags left = {self.board.flags_count}')
        self.board.print_board_seen_by_user()
        print('')

        while self.board.game_won is False and self.board.bomb_hit is False:
            move = input().split()
            if len(move) == 1:
                position = move[0].strip('().').split(',')
                horizontal_position = int(position[0])
                vertical_position = int(position[1])
                action = None

            elif len(move) == 2:
                position = move[1].strip('().').split(',')
                horizontal_position = int(position[0])
                vertical_position = int(position[1])
                action = move[0]

            self.board.update_board((vertical_position, horizontal_position), action)
            if self.board.bomb_hit is True:
                break
            if self.board.game_won is True:
                print('You won.')
                self.board.print_board_hidden_from_user()
                break
            print(f'\nFlags left = {self.board.flags_count}')
            self.board.print_board_seen_by_user()
            print('')
