import tkinter as tk
from Minesweeper import Minesweeper

class SpecialButton(tk.Button):
    def __init__(self, master=None, tile=None, rrow=None, ccolumn=None, **kw):
        tk.Button.__init__(self,master,**kw)
        self.board = game.board
        self.tile = tile
        self.position = (rrow, ccolumn)
        self.bind("<Button-1>", self.reveal)
        self.bind("<Button-2>", self.flag)

    def flag(self, event):
        if self['text'] == 'F':
            self['text'] = self.tile.appearance
        else:
            self['text'] = 'F'

    def reveal(self, event):
        x, y = self.tile.position
        if self.board.board_as_grid_hidden[x][y] == '*':
            end_game_window = tk.Toplevel()
            message = tk.Message(end_game_window, text='You lost.')
            message.pack()

            # Reveal board
            for btn in list_buttons:
                btn['text'] = btn.tile.val

        elif self.board.board_as_grid_hidden[x][y] == ' ':
            surrounding_tiles = self.board.blank_space_BFS(self.position)
            for tile in surrounding_tiles:
                tile_row, tile_col = tile
                for button in list_buttons:
                    if button.tile.position == tile:
                        btn = button
                btn['text'] = btn.tile.val
                btn.tile.appearance = btn.tile.val

        else:
            self['text'] = self.tile.val
            self.tile.appearance = self.tile.val

        self.board.check_win_condition()
        if self.board.game_won:
            end_game_window = tk.Toplevel()
            message = tk.Message(end_game_window, text='You won!')
            message.pack()

            # Reveal board
            for btn in list_buttons:
                btn['text'] = btn.tile.val



list_buttons = []
game = Minesweeper()
game.create_board(9, 9, 10)
#game.create_board(3, 3, 1)
game.board.create_random_grid()
game.board.change_0s_to_blank_spaces()

root = tk.Tk()
frame=tk.Frame(root)
frame.grid(sticky=tk.N+tk.E+tk.S+tk.W) # Ca change tu vraiment quelque chose le sticky

for i, tile in enumerate(game.board.tiles):
    column = i%game.board.grid_size[1]
    row = i//game.board.grid_size[1]
    btn = SpecialButton(frame,
                        tile=tile,
                        text=str(tile.appearance),
                        rrow=row,
                        ccolumn=column,
                        height=int(30/game.board.grid_size[0]),
                        width=int(90/game.board.grid_size[1]),
                        )
    btn.grid(row=row, column=column)
    list_buttons.append(btn)


root.mainloop()
