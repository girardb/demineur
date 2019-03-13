"""Program that reads strings from a file and prints the according Minesweeper grids."""
class MinesweeperFromStrings:
    """Creates a Minesweeper board from a string.

    Creates the necessary methods to read, interpret and print a Minesweeper
    grid from a string.
    """
    def __init__(self):
        """Initializes the grids."""
        self.grids = []
        self.mine_positions_per_grid = []
        self.grid_sizes = []
        self.grids_as_string = []

    def determine_adjacent_mines(self, blank_space_character=0):
        """Determine how many mines are close for each tile on the grid."""
        for grid_number, grid in enumerate(self.grids):
            for pos_r, row in enumerate(grid):
                for pos_c in range(len(row)):
                    adjacent_mines = 0
                    adjacent_positions = []
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            if (pos_r+i) >= 0 and (pos_r+i) < self.grid_sizes[grid_number][0] and (pos_c+j) >= 0 and (pos_c+j) < self.grid_sizes[grid_number][1]:
                                if (pos_r+i, pos_c+j) != (pos_r, pos_c):
                                    adjacent_positions.append((pos_r+i, pos_c+j))
                    for tile in adjacent_positions:
                        if tile in self.mine_positions_per_grid[grid_number]:
                            adjacent_mines += 1

                    if self.grids[grid_number][pos_r][pos_c] != '*':
                        if adjacent_mines == 0:
                            self.grids[grid_number][pos_r][pos_c] = str(blank_space_character)
                        else:
                            self.grids[grid_number][pos_r][pos_c] = str(adjacent_mines)

    def print_the_grids(self):
        """Prints the interpreted grids."""
        for grid_number, grid in enumerate(self.grids):
            for row in grid:
                print(' '.join(row))
            if grid_number != len(self.grids)-1:
                print('')

    def read_grids_from_file_and_get_their_respective_size(self, text_file_with_grids_as_string):
        """Reads strings from a file and gets the size and mine locations of the grids."""
        with open(text_file_with_grids_as_string, 'r') as file:
            self.grids_as_string = file.read().split('\n')

        grid_sizes_as_string = [grid.strip('.*x') for grid in self.grids_as_string]

        for grid in grid_sizes_as_string:
            y_visited = False
            x_as_string = ''
            y_as_string = ''
            for character in grid:
                if character == 'y':
                    y_visited = True
                elif y_visited is False:
                    x_as_string += character
                else:
                    y_as_string += character
            self.grid_sizes.append((int(x_as_string), int(y_as_string)))

    def recreate_grids_in_array(self):
        """Interprets the strings and recreates the grids in a 2D-array."""
        grids_one_dimension = [list(grid.strip('0123456789xy')) for grid in self.grids_as_string]

        # Assuming that the number of mines/empty positions sent correspond to height*length
        # AKA assuming that the input is valid (#Might need to implement something to check that.)

        for grid_number, grid in enumerate(grids_one_dimension):
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
        """This method uses the other methods to pipeline actions in the right order."""
        # Step 1. Determine Height and Length of each grid
        self.read_grids_from_file_and_get_their_respective_size(text_file_with_grids_as_string)

        # Step 2. Place each mine into their respective position in the 2D-array
        self.recreate_grids_in_array()

        # Step 3. Determine the number of mines adjacent to each position on the grid
        self.determine_adjacent_mines()

        # Step 4. Print the grids
        self.print_the_grids()

if __name__ == '__main__':
    GAME = MinesweeperFromStrings()
    GAME.niveau_1_print_from_file('grids.txt')
