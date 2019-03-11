class Minesweeper_1:
    def determine_adjacent_mines(self, blank_space_character=0):
        for grid_number, grid in enumerate(self.grids):
            for x, row in enumerate(grid):
                for y, position in enumerate(row):
                    adjacent_mines = 0
                    adjacent_positions = []
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            if (x+i) >= 0 and (x+i)<self.grid_sizes[grid_number][0] and (y+j) >= 0 and (y+j)<self.grid_sizes[grid_number][1]:
                                if (x+i, y+j) != (x,y):
                                    adjacent_positions.append((x+i, y+j))
                    for tile in adjacent_positions:
                        if tile in self.mine_positions_per_grid[grid_number]:
                            adjacent_mines += 1

                    if self.grids[grid_number][x][y] != '*':
                        if adjacent_mines == 0:
                            self.grids[grid_number][x][y] = str(blank_space_character)
                        else:
                            self.grids[grid_number][x][y] = str(adjacent_mines)

    def print_the_grids(self):
        for grid_number, grid in enumerate(self.grids):
            for row in grid:
                print(' '.join(row))
            if grid_number != len(self.grids)-1:
                print('')

    def read_grids_from_file_and_get_their_respective_size(self, text_file_with_grids_as_string):
        with open(text_file_with_grids_as_string, 'r') as f:
            self.grids_as_string = f.read().split('\n')

        grid_sizes_as_string = [grid.strip('.*x') for grid in self.grids_as_string]
        self.grid_sizes = []

        for grid in grid_sizes_as_string:
            y_visited = False
            x = ''
            y = ''
            for character in grid:
                if character == 'y':
                    y_visited = True
                elif y_visited is False:
                    x += character
                else:
                    y += character
            self.grid_sizes.append((int(x), int(y)))

    def recreate_grids_in_array(self):
        grids_1D = [list(grid.strip('0123456789xy')) for grid in self.grids_as_string]

        # Assuming that the number of mines/empty positions sent correspond to height*length
        # AKA assuming that the input is valid (#Might need to implement something to check that.)
        self.grids = []
        self.mine_positions_per_grid = []

        for grid_number, grid in enumerate(grids_1D):
            grid_to_append = []
            row_to_append = []
            mines = []
            for character_index, character in enumerate(grid):
                if character_index % self.grid_sizes[grid_number][1] == 0 and character_index != 0:
                    grid_to_append.append(row_to_append)
                    row_to_append = []
                row_to_append.append(character)

                # Remember the position of the mines
                if character == '*':
                    mines.append((character_index // self.grid_sizes[grid_number][1], character_index % self.grid_sizes[grid_number][1]))

            grid_to_append.append(row_to_append) # Ugly
            self.grids.append(grid_to_append)
            self.mine_positions_per_grid.append(mines)

    def niveau_1_print_from_file(self, text_file_with_grids_as_string):
        # Step 1. Determine Height and Length of each grid
        self.read_grids_from_file_and_get_their_respective_size(text_file_with_grids_as_string)

        # Step 2. Place each mine into their respective position in the 2D-array
        self.recreate_grids_in_array()

        # Step 3. Determine the number of mines adjacent to each position on the grid
        self.determine_adjacent_mines()

        # Step 4. Print the grids
        self.print_the_grids()

if __name__ == '__main__':
    game = Minesweeper_1()
    game.niveau_1_print_from_file('grids.txt')
