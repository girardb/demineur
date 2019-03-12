import pytest
from Minesweeper import Minesweeper, InstructionError, OutOfBoundsError

class TestPlayerInput(object):
    def test_player_input_1(self):
        assert Minesweeper.player_input('0,0') == [0, 0, None]

    def test_player_input_2(self):
        with pytest.raises(InstructionError) as excinfo:
            Minesweeper.player_input('0000aaaa aaaa')

    def test_player_input_3(self):
        with pytest.raises(InstructionError) as excinfo:
            Minesweeper.player_input('a000aaa')

    def test_player_input_4(self):
        with pytest.raises(InstructionError) as excinfo:
            Minesweeper.player_input('0,0 k')

    def test_player_input_5(self):
        with pytest.raises(InstructionError) as excinfo:
            Minesweeper.player_input('00 f')

    def test_player_input_6(self):
        assert Minesweeper.player_input('0,0 f') == [0, 0, 'f']

    def test_player_input_7(self):
        assert Minesweeper.player_input('0,0 F') == [0, 0, 'F']

    def test_player_input_8(self):
        assert Minesweeper.player_input('0,0 r') == [0, 0, 'r']

    def test_player_input_9(self):
        assert Minesweeper.player_input('0,0 R') == [0, 0, 'R']

    def test_player_input_10(self):
        game = Minesweeper()
        game.create_board()
        game.create_random_grid(3, 3, 1)
        game.change_0s_to_blank_spaces() # Au cas où que ca change de quoi lol

        with pytest.raises(OutOfBoundsError) as excinfo:
            Minesweeper.player_input('9,9')
        # Mettre le contexte d'un board 3,3 et accéder à un index plus grand.
        # Test si on essaie d'input des coordonnées plus grandes que les grandeurs de la grid. -> OutOfBounds Error
