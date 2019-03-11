import copy
import random
import queue
from niveau1 import Minesweeper, Node

# Generate random grids
def create_random_grid(self, grid_length, grid_height, number_of_mines):
    if number_of_mines is None:
        number_of_mines = int(0.15*grid_length*grid_height)

    self.grid_sizes = [[grid_height, grid_length]]

    grid_array = []
    position_of_mines = random.sample(range(grid_length*grid_height), number_of_mines)

    grid_string = ''
    for i in range(grid_length*grid_height):
        if i in position_of_mines:
            grid_string += '*'
        else:
            grid_string += '.'

    self.grids_as_string = [grid_string]
    self.recreate_grids_in_array()
    self.determine_adjacent_mines(blank_space_character = ' ') # Can make this faster since I already know where the mines are, from the random sampling

    # Hide non-revealed tiles
    self.revealed_grid = copy.deepcopy(self.grids[0])
    for x in range(len(self.revealed_grid)):
        for y in range(len(self.revealed_grid[0])):
            self.revealed_grid[x][y] = '-'

# Find touching blank spaces and adjacent numbered tiles
def blank_space_BFS(self, position):
    x, y = position
    open_set = queue.Queue()
    visited = set()

    for node in self.Nodes:
        if node.position == (x, y):
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


def print_revealed_grid(self):
    # Real Ugly
    reveal_grid = copy.deepcopy(self.revealed_grid) # Inefficient but it works
    reveal_grid.insert(0, list(range(self.grid_sizes[0][1])))
    for i in range(self.grid_sizes[0][1]):
        reveal_grid[0][i] = str(reveal_grid[0][i])
    reveal_grid[0].insert(0, ' ')
    reveal_grid[0].insert(0, ' ')

    k = 0
    for i in range(1, self.grid_sizes[0][0]+1):
        reveal_grid[i].insert(0, str(k))
        reveal_grid[i].insert(1, 'x')
        k += 1

    reveal_grid.insert(1, ['x' for i in range(len(reveal_grid[0])-2)])
    reveal_grid[1].insert(0, ' ')
    reveal_grid[1].insert(0, ' ')
    for row in reveal_grid:
        print(' '.join(row))



def create_graph_of_grid(self):
    self.Nodes = []
    for x, row in enumerate(self.grids[0]):
        for y, column in enumerate(row):
            if self.grids[0][x][y] == ' ':
                node = Node(0, x, y)
            else:
                node = Node(self.grids[0][x][y], x, y)
            self.Nodes.append(node)
    for node in self.Nodes:
        node_x, node_y = node.position
        adjacent_tiles = [(node_x+1, node_y), (node_x-1, node_y), (node_x, node_y+1), (node_x, node_y-1), (node_x-1, node_y-1), (node_x+1, node_y-1), (node_x+1, node_y+1), (node_x-1, node_y+1)]
        for tile in adjacent_tiles:
            if tile[0] < 0 or tile[0]>=self.grid_sizes[0][0] or tile[1]<0 or tile[1]>=self.grid_sizes[0][1]:
                adjacent_tiles.pop(adjacent_tiles.index(tile))

        for other_node in self.Nodes:
            if other_node.position in adjacent_tiles:
                node.child.append(other_node)

def update_revealed_grid(self, move, position):
    x, y = position

    if move == 'R': # reveal
        if self.grids[0][x][y] == '*':
            print('You lost.')
            self.bomb_hit = True
        elif self.grids[0][x][y] == ' ':
            surrounding_tiles = self.blank_space_BFS((x,y))
            for tile in surrounding_tiles:
                tile_x, tile_y = tile
                self.revealed_grid[tile_x][tile_y] = self.grids[0][tile_x][tile_y]
        else:
            self.revealed_grid[x][y] = self.grids[0][x][y]
    elif move == 'F':
        if self.revealed_grid[x][y] == 'F':
            self.revealed_grid[x][y] = '-'
        else:
            self.revealed_grid[x][y] = 'F'

    # Check win condition
    # Real ugly and definitely not efficient since I recreate the whole grid at every turn
    comparison_grid = copy.deepcopy(self.revealed_grid)
    for i in range(len(comparison_grid)):
        for j in range(len(comparison_grid[0])):
            if comparison_grid[i][j] == 'F':
                comparison_grid[i][j] = '*'

    if comparison_grid == self.grids[0]:
        self.game_won = True

def play_a_game(self, grid_length=9, grid_height=9, number_of_mines=None):
    self.game_won = False
    self.bomb_hit = False
    self.create_random_grid(grid_length, grid_height, number_of_mines)
    self.create_graph_of_grid()
    self.print_revealed_grid()
    print('')

    while self.game_won is False and self.bomb_hit is False:
        move = input()
        move = move.split()
        position = move[1].strip('()').split(',')
        position[0] = int(position[0])
        position[1] = int(position[1])
        action = move[0]
        self.update_revealed_grid(action, position)
        if self.bomb_hit is True:
            break
        if self.game_won is True:
            print('You won.')
            break
        self.print_revealed_grid()
        print('')


# Make it playable from command-line with inputs 'move (x, y)' # Use list(str.strip('(),'))

if __name__ == '__main__':
    Minesweeper.create_random_grid = create_random_grid
    Minesweeper.print_revealed_grid = print_revealed_grid
    Minesweeper.blank_space_BFS = blank_space_BFS
    Minesweeper.update_revealed_grid = update_revealed_grid
    Minesweeper.create_graph_of_grid = create_graph_of_grid
    Minesweeper.play_a_game = play_a_game

    print("To reveal a tile. Use : 'R (y,x)'")
    print("To flag a tile. Use : 'F (y,x)'")
    print('Good Luck!\n')
    print('Write the height of the grid.')
    HEIGTH_OF_GRID = int(input())
    print('Write the length of the grid.')
    LENGTH_OF_GRID = int(input())
    print('Write the number of mines that you want in the grid.')
    NUMBER_OF_MINES = int(input())

    if NUMBER_OF_MINES == '-1':
        NUMBER_OF_MINES = None
    elif NUMBER_OF_MINES > LENGTH_OF_GRID*HEIGTH_OF_GRID:
        NUMBER_OF_MINES = None
        print("The number you wrote is too large. We'll put the appropriate number of mines in the grid.")

    game = Minesweeper()
    game.play_a_game(LENGTH_OF_GRID, HEIGTH_OF_GRID, NUMBER_OF_MINES)
