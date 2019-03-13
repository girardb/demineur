from Board import Board

class InstructionError(Exception):
    pass

class OutOfBoundsError(Exception):
    pass

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

            correct_input = False
            while not correct_input:
                try:
                    vertical_position, horizontal_position, action = self.player_input(input())
                    correct_input = True
                except (InstructionError, OutOfBoundsError) as error:
                    print(error)
                    #print('You made an error')

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

    def start(self):
        print("To reveal a tile, use : 'x,y'")
        print("To flag a tile, use : 'x,y F'")
        print('Good Luck!\n')
        print('Write the height of the grid.')
        print("If you write '-1', the height of the grid will of standard height 9.")

        correct_input = False
        while not correct_input:
            try:
                height_of_grid = Minesweeper.check_grid_configuration_inputs(input())
                correct_input = True
            except InstructionError as error:
                print(error)
                print('You entered the height incorrectly. You should try again.')


        print('Write the length of the grid.')
        print("If you write '-1', the length of the grid will of standard length 9.")

        correct_input = False
        while not correct_input:
            try:
                length_of_grid = Minesweeper.check_grid_configuration_inputs(input())
                correct_input = True
            except InstructionError as error:
                print(error)
                print('You entered the length incorrectly. You should try again.')

        print('Write the number of mines in the grid.')
        print("If you write '-1', an appropriate number of mines will be generated for the size of the grid.")

        correct_input = False
        while not correct_input:
            try:
                number_of_mines = Minesweeper.check_grid_configuration_inputs(input(), length_of_grid=length_of_grid, height_of_grid=height_of_grid, mine=True)
                correct_input = True
            except InstructionError as error:
                print(error)
                print('you entered the number of mines incorrectly. You should try again.')

        self.play_a_game(length_of_grid, height_of_grid, number_of_mines)


    def check_grid_configuration_inputs(input, length_of_grid=None, height_of_grid=None, mine=None):
        if mine is True:
            if length_of_grid == None:
                length_of_grid = 9
            if height_of_grid == None:
                height_of_grid = 9

        if input == '-1':
            return None

        if not input.strip('-').isdigit() and input != '-1':
            raise InstructionError("This is not a number.")

        if int(input) <= 0 and input != '-1':
            raise InstructionError("You can't ask for a grid with negative or zero components.")

        if mine is True:
            if int(input) > length_of_grid*height_of_grid:
                raise InstructionError("This is way too many mines.")

        return int(input)


    def player_input(self, input):
        if input == 'quit':
            quit()

        player_move = input.split()
        position = player_move[0].strip('().').split(',')

        for i in position:
            if not i.strip('-').isdigit():
                raise InstructionError("The position input is not well formated.")

        if len(position) == 1:
            raise InstructionError("You have to specify both the x and y coordinate.")

        position = [int(x) for x in position]

        if position[0] >= self.board.grid_size[1] or position[0] < 0 or position[1] >=self.board.grid_size[0] or position[1] < 0:
            raise OutOfBoundsError("The specified index is out the grid's bounds.")

        action = None
        if len(player_move) == 2:
            if player_move[1] != 'f' and player_move[1] != 'F' and player_move[1] != 'r' and player_move[1] != 'R':
                raise InstructionError("The desired action is not well formated.")
            action = player_move[1]

        return [position[1], position[0], action]
