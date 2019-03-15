import tkinter as tk

class SpecialButton(tk.Button):
    def __init__(self, master=None, tile=None, rrow=None, ccolumn=None, app=None, **kw):
        tk.Button.__init__(self,master,**kw)
        self.app = app
        self.board = self.app.game.board
        self.tile = tile
        self.position = (rrow, ccolumn)

        # Choose which image the tile represents
        if self.tile.val == ' ':
            self.real_image = self.app.image_discovered_tile
        elif self.tile.val == 1:
            self.real_image = self.app.image_tile_1
        elif self.tile.val == 2:
            self.real_image = self.app.image_tile_2
        elif self.tile.val == 3:
            self.real_image = self.app.image_tile_3
        elif self.tile.val == 4:
            self.real_image = self.app.image_tile_4
        elif self.tile.val == 5:
            self.real_image = self.app.image_tile_5
        elif self.tile.val == 6:
            self.real_image = self.app.image_tile_6
        elif self.tile.val == 7:
            self.real_image = self.app.image_tile_7
        elif self.tile.val == 8:
            self.real_image = self.app.image_tile_8
        elif self.tile.val == '*':
            self.real_image = self.app.image_mine


        self.bind("<Button-1>", self.reveal)
        self.bind("<Button-2>", self.flag)

    def flag(self, event): # rajouter le point d'interrogation là-dedans
        self.app.smiley_face_switch()
        if self['text'] == 'F':
            self['text'] = self.tile.appearance
            self['image'] = self.app.image_full_tile # un peu weird de permettre de flagger des tiles révélées

            # update flags
            self.app.game.board.flags_count += 1
            flags_count = self.app.game.board.flags_count
            self.app.counterDigit.reveal_segments(flags_count%10)
            self.app.counter10s.reveal_segments(flags_count//10)
            self.app.counter100s.reveal_segments(flags_count//100)

        else:
            self['text'] = 'F'
            self['image'] = self.app.image_flag
            self.app.game.board.flags_count -= 1

            # update flags
            flags_count = self.app.game.board.flags_count
            self.app.counterDigit.reveal_segments(flags_count%10)
            self.app.counter10s.reveal_segments(flags_count//10)
            self.app.counter100s.reveal_segments(flags_count//100)

    def reveal(self, event):
        #if self.app.timer_status is not True:
        self.app.timer_status = True

        x, y = self.tile.position
        if self.board.board_as_grid_hidden[x][y] == '*':
            self.app.smiley_face_switch(lost=True)
            self.app.spawn_end_game_window(lost=True)
            self.app.timer_status = False

            # Reveal board
            for btn in self.app.list_buttons:
                btn['text'] = btn.tile.val
                btn['image'] = btn.real_image
            self['image'] = self.app.image_red_mine

        elif self.board.board_as_grid_hidden[x][y] == ' ':
            self.app.smiley_face_switch()
            surrounding_tiles = self.board.blank_space_BFS(self.position)
            for tile in surrounding_tiles:
                tile_row, tile_col = tile
                for button in self.app.list_buttons:
                    if button.tile.position == tile:
                        btn = button
                btn['text'] = btn.tile.val
                btn.tile.appearance = btn.tile.val
                btn['image'] = btn.real_image

        else:
            self['text'] = self.tile.val
            self['image'] = self.real_image
            self.tile.appearance = self.tile.val
            self.app.smiley_face_switch()

        self.board.check_win_condition()
        if self.board.game_won:
            self.app.smiley_face_switch(won=True)
            self.app.spawn_end_game_window(won=True)
            self.app.timer_status = False

            # Reveal board
            for btn in self.app.list_buttons:
                btn['text'] = btn.tile.val
                btn['image'] = btn.real_image

        # MAYBE ADD THE MIDDLE BUTTON MECHANIC/COMMAND FROM THE REAL MINESWEEPER GAME
