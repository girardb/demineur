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

        if grid_length is None:
            grid_length = 9

        if grid_height is None:
            grid_height = 9

        self.grid_size = [grid_height, grid_length]
        self.flags_count = self.number_of_mines
        self.position_of_mines = []
        self.game_won = False # Probably need to put this on the game class
        self.bomb_hit = False # Probably need to put this on the game class

        # Create the tiles
        self.tiles = []
        for i in range(grid_height):
            for j in range(grid_length):
                tile = Tile(self, 0, i, j, False)
                self.tiles.append(tile)


    def create_random_grid(self):
        self.position_of_mines = random.sample(range(self.grid_size[0]*self.grid_size[1]), self.number_of_mines)

        for tile in self.tiles:
            tile.find_adjacent_positions()
            tile.find_child()

        for tile in self.position_of_mines:
            self.tiles[tile].bomb = True
            self.tiles[tile].val = '*' # probablement moins efficace vue que pour certaines tiles .val est un int mais bon.

        # Create grid
        self.board_as_grid_hidden = []
        self.board_as_grid_user = []
        for i in range(self.grid_size[0]):
            row_hidden = []
            row_user = []
            for j in range(self.grid_size[1]):
                row_hidden.append(str(self.tiles[i*self.grid_size[0] + j].val)) # Change somewhere around here for blank spaces?
                row_user.append(str(self.tiles[i*self.grid_size[0] + j].appearance))
            self.board_as_grid_hidden.append(row_hidden)
            self.board_as_grid_user.append(row_user)

    def blank_space_BFS(self, position):
        open_set = queue.Queue()
        visited = set()

        for tile in self.tiles:
            if tile.position == position:
                root = tile
        open_set.put(root)

        while not open_set.empty():
            subtree_root = open_set.get()

            for child in subtree_root.child:
                if child.position in visited:
                    continue
                if child.position not in visited:
                    if child.val != ' ':                # Changed here for blank spaces
                        visited.add(child.position)
                    elif child.val == ' ':                # Changed here for blank spaces
                        open_set.put(child)
            visited.add(subtree_root.position)
        return visited

    def print_board_seen_by_user(self): # suuuuuper long pour rien. Il faut changer ca.
        grid_to_print = copy.deepcopy(self.board_as_grid_user)
        first_row = [' ', ' '] + [str(i) for i in range(self.grid_size[1])]
        second_row = [' ', ' '] + ['x' for i in range(self.grid_size[1])]
        for i, row in enumerate(grid_to_print):
            row.insert(0, str(i))
            row.insert(1, 'x')

        grid_to_print.insert(0, first_row)
        grid_to_print.insert(1, second_row)

        for i in grid_to_print:
            print(' '.join(i))

    def print_board_hidden_from_user(self):
        for i in self.board_as_grid_hidden:
            print(' '.join(i))

    def update_board(self, position, move):
        x, y = position

        if move == 'r' or move == 'R' or move == None:
            if self.board_as_grid_hidden[x][y] == '*':
                print('You lost.')
                self.print_board_hidden_from_user()
                self.bomb_hit = True

            elif self.board_as_grid_hidden[x][y] == ' ': # Changed here for blank spaces
                surrounding_tiles = self.blank_space_BFS(position)
                for tile in surrounding_tiles:
                    tile_x, tile_y = tile
                    self.board_as_grid_user[tile_x][tile_y] = self.board_as_grid_hidden[tile_x][tile_y]
                    self.tiles[tile_x*self.grid_size[0] + tile_y].appearance = self.tiles[tile_x*self.grid_size[0] + tile_y].val
            else:
                self.board_as_grid_user[x][y] = self.board_as_grid_hidden[x][y]
                self.tiles[x*self.grid_size[0] + y].appearance = self.tiles[x*self.grid_size[0] + y].val

        elif move == 'f' or move == 'F':
            if self.board_as_grid_user[x][y] == 'F':
                self.board_as_grid_user[x][y] = '-'
                self.flags_count += 1
            else:
                self.board_as_grid_user[x][y] = 'F'
                self.flags_count -= 1

        self.check_win_condition()

    def check_win_condition(self):
        if all(tile.val == tile.appearance for tile in self.tiles if tile.val != '*'):
            self.game_won = True
        return self.game_won

    def change_0s_to_blank_spaces(self):
        # C'est clair qu'il y a une manière plus efficace de faire ca
        for tile in self.tiles:
            if tile.val == 0:
                tile.val = ' '

        for x, row in enumerate(self.board_as_grid_user):
            for y, column in enumerate(row):
                if self.board_as_grid_user[x][y] == '0':
                    self.board_as_grid_user[x][y] = ' '

        for x, row in enumerate(self.board_as_grid_hidden):
            for y, column in enumerate(row):
                if self.board_as_grid_hidden[x][y] == '0':
                    self.board_as_grid_hidden[x][y] = ' '
