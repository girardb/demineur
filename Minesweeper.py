from Board import Board

class Minesweeper:
    def __init__(self):
        self.board = None

    def create_board(self, grid_length, grid_height, number_of_mines):
        self.board = Board(grid_length, grid_height, number_of_mines)


    def update_revealed_grid(self, move, position):
        x, y = position

        if move == 'R' or move == 'r': # reveal
            if self.grids[0][x][y] == '*':
                print('You lost.')
                self.print_the_grids()
                self.bomb_hit = True
            elif self.grids[0][x][y] == ' ':
                surrounding_tiles = self.blank_space_BFS((x,y))
                for tile in surrounding_tiles:
                    tile_x, tile_y = tile
                    self.revealed_grid[tile_x][tile_y] = self.grids[0][tile_x][tile_y]
            else:
                self.revealed_grid[x][y] = self.grids[0][x][y]
        elif move == 'F' or move == 'f':
            if self.revealed_grid[x][y] == 'F':
                self.revealed_grid[x][y] = '-'
                self.flags_count += 1
            else:
                self.revealed_grid[x][y] = 'F'
                self.flags_count -= 1

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
        self.flags_count = 0
        self.game_won = False
        self.bomb_hit = False
        self.create_random_grid(grid_length, grid_height, number_of_mines)
        self.create_graph_of_grid()
        print(f'\nFlags left = {self.flags_count}')
        self.print_revealed_grid()
        print('')

        while self.game_won is False and self.bomb_hit is False:
            move = input()
            move = move.split()
            position = move[1].strip('()').split(',')
            position[0] = int(position[0])
            position[1] = int(position[1])
            position.reverse()
            action = move[0]
            self.update_revealed_grid(action, position)
            if self.bomb_hit is True:
                break
            if self.game_won is True:
                print('You won.')
                self.print_the_grids()
                break
            print(f'\nFlags left = {self.flags_count}')
            self.print_revealed_grid()
            print('')
