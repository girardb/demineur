"""Creates the Tile class to be used by the Board class for a Minesweeper game."""
class Tile:
    """Creates the tile for a Minesweeper board/grid."""
    def __init__(self, board, val, x, y, bomb, appear_as='-'):
        """Initializes the tile."""
        self.board = board
        self.val = val
        self.position = (x, y)
        self.bomb = bomb
        self.appearance = appear_as
        self.adjacent_positions = []
        self.child = []

    def __str__(self):
        """Returns the tile as it should be seen by the user."""
        return self.appearance

    def find_adjacent_positions(self):
        """Finds the adjacent tiles to a tile."""
        pos_r, pos_c = self.position

        for i in range(-1, 2):
            for j in range(-1, 2):
                if (pos_r+i) >= 0 and (pos_r+i) < self.board.grid_size[0] and (pos_c+j) >= 0 and (pos_c+j) < self.board.grid_size[1]:
                    if (pos_r+i, pos_c+j) != (pos_r, pos_c):
                        self.adjacent_positions.append((pos_r+i, pos_c+j))

        for adjacent_tile in self.adjacent_positions:
            pos_r, pos_c = adjacent_tile
            tile_index = pos_r*self.board.grid_size[0] + pos_c
            if tile_index in self.board.position_of_mines:
                self.val += 1

    def find_child(self):
        """Finds the children of a tile.

        It will be useful when the board is seen as a graph and Breadth-first
        search will be used to find all the connected blank spaces to reveal.
        """
        for tile in self.board.tiles:
            if tile.position in self.adjacent_positions:
                self.child.append(tile)
