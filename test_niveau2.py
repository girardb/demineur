import pytest
from Minesweeper import Minesweeper, InstructionError, OutOfBoundsError, check_grid_configuration_inputs

def create_standard_grid():
    game = Minesweeper()
    game.create_board(3, 3, 1)
    game.board.create_random_grid()
    game.board.change_0s_to_blank_spaces()
    return game

class TestPlayerInput(object):
    def test_player_input_1(self):
        game = create_standard_grid()
        assert game.player_input('0,0') == [0, 0, None]

    def test_player_input_2(self):
        game = create_standard_grid()
        with pytest.raises(InstructionError) as excinfo:
            game.player_input('0000aaaa aaaa')

    def test_player_input_3(self):
        game = create_standard_grid()
        with pytest.raises(InstructionError) as excinfo:
            game.player_input('a000aaa')

    def test_player_input_4(self):
        game = create_standard_grid()
        with pytest.raises(InstructionError) as excinfo:
            game.player_input('0,0 k')

    def test_player_input_5(self):
        game = create_standard_grid()
        with pytest.raises(InstructionError) as excinfo:
            game.player_input('00 f')

    def test_player_input_6(self):
        game = create_standard_grid()
        assert game.player_input('0,0 f') == [0, 0, 'f']

    def test_player_input_7(self):
        game = create_standard_grid()
        assert game.player_input('0,0 F') == [0, 0, 'F']

    def test_player_input_8(self):
        game = create_standard_grid()
        assert game.player_input('0,0 r') == [0, 0, 'r']

    def test_player_input_9(self):
        game = create_standard_grid()
        assert game.player_input('0,0 R') == [0, 0, 'R']

    def test_player_input_10(self):
        game = create_standard_grid()
        with pytest.raises(OutOfBoundsError) as excinfo:
            game.player_input('9,9')

    def test_player_input_11(self):
        game = create_standard_grid()
        with pytest.raises(InstructionError) as excinfo:
            game.player_input('')

    def test_player_input_12(self):
        game = create_standard_grid()
        with pytest.raises(InstructionError) as excinfo:
            game.player_input(' ')

class TestCheckGridConfigurationInput(object):
    def test_check_grid_configuration_input_1(self): # Negative height and length
        with pytest.raises(InstructionError) as excinfo:
            check_grid_configuration_inputs('-3')

    def test_check_grid_configuration_input_2(self): # Negative number of mines
        with pytest.raises(InstructionError) as excinfo:
            check_grid_configuration_inputs('-2', length_of_grid=9, height_of_grid=9, mine=True)


    def test_check_grid_configuration_input_3(self): # Number of mines > grid_length*grid_height
        with pytest.raises(InstructionError) as excinfo:
            check_grid_configuration_inputs('-7', length_of_grid=2, height_of_grid=2, mine=True)

    def test_check_grid_configuration_input_4(self): # Number of mines > grid_length*grid_height
        with pytest.raises(InstructionError) as excinfo:
            check_grid_configuration_inputs('7', length_of_grid=2, height_of_grid=2, mine=True)

    def test_check_grid_configuration_input_5(self): # Length NaN
        with pytest.raises(InstructionError) as excinfo:
            check_grid_configuration_inputs('aaa aa')

    def test_check_grid_configuration_input_6(self): # Height NaN
        with pytest.raises(InstructionError) as excinfo:
            check_grid_configuration_inputs('aaa')

    def test_check_grid_configuration_input_7(self): # Number of mines NaN
        with pytest.raises(InstructionError) as excinfo:
            check_grid_configuration_inputs(' aa', length_of_grid=9, height_of_grid=9, mine=True)

    def test_check_grid_configuration_input_8(self): # Appropriate number of mines
        assert check_grid_configuration_inputs('3', length_of_grid=9, height_of_grid=9, mine=True) == 3

    def test_check_grid_configuration_input_9(self):
        assert check_grid_configuration_inputs('3') == 3

    def test_check_grid_configuration_input_10(self):
        assert check_grid_configuration_inputs('-1') == None

    def test_check_grid_configuration_input_11(self):
        assert check_grid_configuration_inputs('-1', length_of_grid=9, height_of_grid=9, mine=True) == None

    def test_check_grid_configuration_input_12(self):
        assert check_grid_configuration_inputs('-1', length_of_grid=None, height_of_grid=None, mine=True) == None

    def test_check_grid_configuration_input_13(self):
        assert check_grid_configuration_inputs('4', length_of_grid=None, height_of_grid=None, mine=True) == 4

    def test_check_grid_configuration_input_14(self):
        with pytest.raises(InstructionError) as excinfo:
            check_grid_configuration_inputs('-4', length_of_grid=3, height_of_grid=None, mine=True)

    def test_check_grid_configuration_input_14(self):
        with pytest.raises(InstructionError) as excinfo:
            check_grid_configuration_inputs('0')
