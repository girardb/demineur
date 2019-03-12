class Tile:
    def __init__(self, board, val, x, y, bomb, appear_as='-'):
        self.board = board
        self.val = val
        self.position = (x, y)
        self.bomb = bomb
        self.appearance = appear_as

        self.adjacent_positions = []
        self.child = []

    def __str__(self):
        return self.appearance

    def find_adjacent_positions(self):
        x, y = self.position

        for i in range(-1, 2):
            for j in range(-1, 2):
                if (x+i) >= 0 and (x+i)<self.board.grid_size[0] and (y+j) >= 0 and (y+j)<self.board.grid_size[1]:
                    if (x+i, y+j) != (x,y):
                        self.adjacent_positions.append((x+i, y+j))

        for adjacent_tile in self.adjacent_positions:
            x, y = adjacent_tile
            tile_index = x*self.board.grid_size[0] + y
            if tile_index in self.board.position_of_mines:
                self.val += 1

    def find_child(self):
        for tile in self.board.tiles:
            if tile.position in self.adjacent_positions:
                self.child.append(tile)
