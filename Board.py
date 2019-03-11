import copy
import random
import queue
from Tile import Tile

class Board:
    def __init__(self, grid_length, grid_height, number_of_mines):
        if number_of_mines is None:
            self.number_of_mines = int(0.15*grid_length*grid_height)
        else:
            self.number_of_mines = number_of_mines

        self.grid_size = [grid_height, grid_length]
        self.flags_count = number_of_mines
        self.position_of_mines = []

        # Create the tiles
        self.tiles = []
        for i in range(grid_height):
            for j in range(grid_length):
                tile = Tile(self, 0, i, j, False)
                self.tiles.append(tile)


    def create_random_grid(self):
        self.position_of_mines = random.sample(range(self.grid_size[0]*self.grid_size[1]), self.number_of_mines)
        for tile in self.position_of_mines:
            self.tiles[tile].bomb = True
            self.tiles[tile].val = '*' # probablement moins efficace vue que pour certaines tiles .val est un int mais bon.

        for tile in self.tiles:
            tile.find_adjacent_positions()
            #tile.find_child()

        # Create grid
        self.board_as_grid_hidden = []
        self.board_as_grid_user = []
        for i in range(self.grid_size[0]):
            row_hidden = []
            row_user = []
            for j in range(self.grid_size[1]):
                row_hidden.append(str(self.tiles[i*self.grid_size[0] + j].val))
                row_user.append(str(self.tiles[i*self.grid_size[0] + j].appearance))
            self.board_as_grid_hidden.append(row_hidden)
            self.board_as_grid_user.append(row_user)

    def blank_space_BFS(self, position):
        x, y = position
        open_set = queue.Queue()
        visited = set()

        for tile in self.tiles:
            if tile.position == (x, y):
                root = node
        open_set.put(root)

        while not open_set.empty():
            subtree_root = open_set.get()

            for child in subtree_root.child:
                if child.position in visited:
                    continue
                if child.position not in visited:
                    if child.val != 0:
                        visited.add(child.position)
                    elif child.val == 0:
                        open_set.put(child)
            visited.add(subtree_root.position)
        return visited

    def print_board_seen_by_user(self):
        for i in self.board_as_grid_hidden:
            print(' '.join(i))

    def print_board_hidden_from_user(self):
        for i in self.board_as_grid_user:
            print(' '.join(i))
