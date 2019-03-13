"""Creates the Board class for a Minesweeper game.

Creates the Board class for a Minesweeper Class to use in order to play
a game of Minesweeper.
"""
import copy
import queue
import random
from Tile import Tile

class Board:
    """Used to create a board/grid for a Minesweeper game."""
    def __init__(self, grid_length, grid_height, number_of_mines):
        """Initializes the board.

        Initializes the size of the board as well as the Tile objects that it
        uses to represent the Minesweeper's board's game state.
        """
        if grid_length is None:
            grid_length = 9

        if grid_height is None:
            grid_height = 9

        if number_of_mines is None:
            self.number_of_mines = int(0.15*grid_length*grid_height)
        else:
            self.number_of_mines = number_of_mines

        self.grid_size = [grid_height, grid_length]
        self.flags_count = self.number_of_mines
        self.position_of_mines = []
        self.game_won = False
        self.bomb_hit = False
        self.board_as_grid_hidden = []
        self.board_as_grid_user = []

        # Create the tiles
        self.tiles = []
        for i in range(grid_height):
            for j in range(grid_length):
                tile = Tile(self, 0, i, j, False)
                self.tiles.append(tile)


    def create_random_grid(self):
        """Creates a grid with random mine placements.

        Creates a grid with random mine placements and represents it in a
        2D-array.
        """
        self.position_of_mines = random.sample(range(self.grid_size[0]*self.grid_size[1]), self.number_of_mines)

        for tile in self.tiles:
            tile.find_adjacent_positions()
            tile.find_child()

        for tile in self.position_of_mines:
            self.tiles[tile].bomb = True
            self.tiles[tile].val = '*'

        # Create grid
        for i in range(self.grid_size[0]):
            row_hidden = []
            row_user = []
            for j in range(self.grid_size[1]):
                row_hidden.append(str(self.tiles[i*self.grid_size[1] + j].val)) ###
                row_user.append(str(self.tiles[i*self.grid_size[1] + j].appearance)) ###
            self.board_as_grid_hidden.append(row_hidden)
            self.board_as_grid_user.append(row_user)

    def blank_space_BFS(self, position):
        """Uses Breadth-first search to find all the adjacent blank tiles."""
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
                    if child.val != ' ':
                        visited.add(child.position)
                    elif child.val == ' ':
                        open_set.put(child)
            visited.add(subtree_root.position)
        return visited

    def print_board_seen_by_user(self): # suuuuuper long pour rien. Il faut changer ca.
        """Prints the board state as seen by the user."""
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
        """Prints the real board state."""
        for i in self.board_as_grid_hidden:
            print(' '.join(i))

    def update_board(self, position, move):
        """Updates the board state seen by the user.

        Using the user inputs, this method will either see if the user hit a
        mine, and then uncover or flag a tile. It will also verify if the user
        won.
        """
        pos_r, pos_c = position

        if move == 'r' or move == 'R' or move is None:
            if self.board_as_grid_hidden[pos_r][pos_c] == '*':
                print('You lost.')
                self.print_board_hidden_from_user()
                self.bomb_hit = True

            elif self.board_as_grid_hidden[pos_r][pos_c] == ' ': # Changed here for blank spaces
                surrounding_tiles = self.blank_space_BFS(position)
                for tile in surrounding_tiles:
                    tile_x, tile_y = tile
                    self.board_as_grid_user[tile_x][tile_y] = self.board_as_grid_hidden[tile_x][tile_y]
                    self.tiles[tile_x*self.grid_size[1] + tile_y].appearance = self.tiles[tile_x*self.grid_size[1] + tile_y].val
            else:
                self.board_as_grid_user[pos_r][pos_c] = self.board_as_grid_hidden[pos_r][pos_c]
                self.tiles[pos_r*self.grid_size[1] + pos_c].appearance = self.tiles[pos_r*self.grid_size[1] + pos_c].val

        elif move == 'f' or move == 'F':
            if self.board_as_grid_user[pos_r][pos_c] == 'F':
                self.board_as_grid_user[pos_r][pos_c] = '-'
                self.flags_count += 1
            else:
                self.board_as_grid_user[pos_r][pos_c] = 'F'
                self.flags_count -= 1

        self.check_win_condition()

    def check_win_condition(self):
        """Verifies that the user has uncovered all non-mine tiles."""
        if all(tile.val == tile.appearance for tile in self.tiles if tile.val != '*'):
            self.game_won = True
        return self.game_won

    def change_0s_to_blank_spaces(self):
        """Changes the 0s in the grid seen by the user by blank spaces."""
        # C'est clair qu'il y a une manière plus efficace de faire ca
        for tile in self.tiles:
            if tile.val == 0:
                tile.val = ' '

        for pos_r, row in enumerate(self.board_as_grid_user):
            for pos_c in range(len(row)):
                if self.board_as_grid_user[pos_r][pos_c] == '0':
                    self.board_as_grid_user[pos_r][pos_c] = ' '

        for pos_r, row in enumerate(self.board_as_grid_hidden): # Même code que lui en haut. jpeux les merge
            for pos_c in range(len(row)):
                if self.board_as_grid_hidden[pos_r][pos_c] == '0':
                    self.board_as_grid_hidden[pos_r][pos_c] = ' '
