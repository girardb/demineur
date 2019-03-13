"""Creates the Minesweeper class in order to play a game of Minesweeper.

The classes of Minesweeper, InstructionError and OutOfBoundsError are created
to allow a user to play a game of Minesweeper on his console and to be corrected
when his inputs are not in the right format.
"""
from Board import Board

class InstructionError(Exception):
    """Type of error that is raised when the user enters a wrong input."""
    pass

class OutOfBoundsError(Exception):
    """Type of error that is raised when the user asks for a tile that is out of bounds."""
    pass

class Minesweeper:
    """Used to create an instance of a Minesweeper game.

    This class allows the initialization of a Minesweeper board/grid
    and gives methods to interact with said board. A game begins
    by running the Minesweeper.start() method.
    """
    def __init__(self):
        """Initializes a blank Minesweeper board."""
        self.board = None

    def create_board(self, grid_length, grid_height, number_of_mines):
        """Creates the board that will be used for the remaining of the game."""
        self.board = Board(grid_length, grid_height, number_of_mines)

    def play_a_game(self, grid_length=9, grid_height=9, number_of_mines=None):
        """The user will play the already started game of Minesweeper.

        This method calls Minesweeper.create_board() method to initialize the board
        with the user inputs and then randomizes the board and changes its tiles
        where there are 0 mines nearby to be blank tiles. Then, until the game is won
        or the user lost, the user is asked for inputs to uncover tiles from the grid.
        """
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
        """Start a game of Minesweeper.

        This method shows the basic commands used to play a Minesweeper game and
        asks for three inputs. The user inputs will be used to initialize the
        board with the wanted height, length and number of mines on the board.
        Then, it will call the method Minesweeper.play_a_game() to play the game
        and initialize the board.
        """
        print("To reveal a tile, use : 'x,y'")
        print("To flag a tile, use : 'x,y F'")
        print('Good Luck!\n')
        print('Write the height of the grid.')
        print("If you write '-1', the height of the grid will of standard height 9.")

        correct_input = False
        while not correct_input:
            try:
                height_of_grid = check_grid_configuration_inputs(input())
                correct_input = True
            except InstructionError as error:
                print(error)
                print('You entered the height incorrectly. You should try again.')


        print('Write the length of the grid.')
        print("If you write '-1', the length of the grid will of standard length 9.")

        correct_input = False
        while not correct_input:
            try:
                length_of_grid = check_grid_configuration_inputs(input())
                correct_input = True
            except InstructionError as error:
                print(error)
                print('You entered the length incorrectly. You should try again.')

        print('Write the number of mines in the grid.')
        print("If you write '-1', an appropriate number of mines will be generated for the size of the grid.")

        correct_input = False
        while not correct_input:
            try:
                number_of_mines = check_grid_configuration_inputs(input(), length_of_grid=length_of_grid, height_of_grid=height_of_grid, mine=True)
                correct_input = True
            except InstructionError as error:
                print(error)
                print('you entered the number of mines incorrectly. You should try again.')

        self.play_a_game(length_of_grid, height_of_grid, number_of_mines)

    def player_input(self, user_input):
        """Validates that the user inputs are in the right format.

        Validates that the user inputs are in the right format when the user
        is playing the Minesweeper game.
        """
        if user_input == 'quit':
            quit()

        player_move = user_input.split()
        position = player_move[0].strip('().').split(',')

        for i in position:
            if not i.strip('-').isdigit():
                raise InstructionError("The position input is not well formated.")

        if len(position) == 1:
            raise InstructionError("You have to specify both the x and y coordinate.")

        position = [int(x) for x in position]

        if position[0] >= self.board.grid_size[1] or position[0] < 0 or position[1] >= self.board.grid_size[0] or position[1] < 0:
            raise OutOfBoundsError("The specified index is out the grid's bounds.")

        action = None
        if len(player_move) == 2:
            if player_move[1] != 'f' and player_move[1] != 'F' and player_move[1] != 'r' and player_move[1] != 'R':
                raise InstructionError("The desired action is not well formated.")
            action = player_move[1]

        return [position[1], position[0], action]

def check_grid_configuration_inputs(user_input, length_of_grid=None,
                                    height_of_grid=None, mine=None):
    """Validates that the user inputs are in the right format.

    Validates that the user inputs are in the right format when the user is
    configuring the settings for the Minesweeper board.
    """
    if mine is True:
        if length_of_grid is None:
            length_of_grid = 9
        if height_of_grid is None:
            height_of_grid = 9

    if user_input == '-1':
        return None

    if not user_input.strip('-').isdigit() and user_input != '-1':
        raise InstructionError("This is not a number.")

    if int(user_input) <= 0 and user_input != '-1':
        raise InstructionError("You can't ask for a grid with negative or zero components.")

    if mine is True:
        if int(user_input) > length_of_grid*height_of_grid:
            raise InstructionError("This is way too many mines.")

    return int(user_input)
