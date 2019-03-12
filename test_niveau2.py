import pytest
from Minesweeper import Minesweeper

class TestPlayerInput(object):
    def test_player_input_1(self):
        assert Minesweeper.player_input('0,0') == [0,0, None]

    def test_player_input_2(self):
        pass

    def test_player_input_3(self):
        pass
