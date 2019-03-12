from Board import Board

class Minesweeper:
    def __init__(self):
        self.board = None

    def create_board(self, grid_length, grid_height, number_of_mines):
        self.board = Board(grid_length, grid_height, number_of_mines)

    def play_a_game(self, grid_length=9, grid_height=9, number_of_mines=None):
        self.create_board(grid_length, grid_height, number_of_mines)
        self.board.create_random_grid()
        self.board.change_0s_to_blank_spaces()
        print(f'\nFlags left = {self.board.flags_count}')
        self.board.print_board_seen_by_user()
        print('')

        while not self.board.game_won and not self.board.bomb_hit:

            vertical_position, horizontal_position, action = Minesweeper.player_input(input())
            self.board.update_board((vertical_position, horizontal_position), action)
            if self.board.bomb_hit:
                break
            if self.board.game_won:
                print('You won.')
                self.board.print_board_hidden_from_user()
                break
            print(f'\nFlags left = {self.board.flags_count}')
            self.board.print_board_seen_by_user()
            print('')

    def player_input(input):
        player_move = input.split()
        position = player_move[0].strip('().').split(',')
        position = [int(x) for x in position]
        action = None
        if len(player_move) == 2:
            action = player_move[1]
        return [position[1], position[0], action]
