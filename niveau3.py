import tkinter as tk
from Minesweeper import Minesweeper
from functools import partial

# TODO:
# METTRE L'APP DANS UNE CLASSE. ca va faciliter une couple d'affaires comme quand il faut créer une nouvelle grid
# SHOULD I CHANGE THE DESIGN SO THAT THE FIRST TILE SELECTED IS AN EMPTY TILE # HOW
# MAYBE ADD THE MIDDLE BUTTON MECHANIC/COMMAND FROM THE REAL MINESWEEPER GAME
# ADD SMILEY BUTTON??
# ADD TIMER
# ADD FLAG COUNTER
# ADD BORDERS --- jpas capable d'ajouter de border sur la grid. ca a l'air un peu off
# SOMETHING TO CHOOSE SIZE AND NUMBER OF MINES # MENU
# ON THE GAME LOST WINDOW -> ASK TO EXIT OR PLAY AGAIN
# ON THE GAME WON WINDOW -> ASK TO EXIT OR PLAY AGAIN

def smiley_button_press():
    pass

def open_settings_window():
    settings_window = tk.Toplevel()
    settings_window.wm_title('Settings')

    settings_window_frame = tk.Frame(settings_window)
    settings_window_frame.grid()

    height = tk.StringVar()
    height_label = tk.Label(master=settings_window_frame, text='Height').grid(row=0, column=0)
    height_entry = tk.Entry(master=settings_window_frame, textvariable=height).grid(row=0, column=1)
    height.set('9')

    length = tk.StringVar()
    length_label = tk.Label(master=settings_window_frame, text='Length').grid(row=1, column=0)
    length_entry = tk.Entry(master=settings_window_frame, textvariable=length).grid(row=1, column=1)
    length.set('9')

    mines = tk.StringVar()
    mines_label = tk.Label(master=settings_window_frame, text='Number of Mines').grid(row=2, column=0)
    mines_entry = tk.Entry(master=settings_window_frame, textvariable=mines).grid(row=2, column=1)
    mines.set('12')

    create_board_button = tk.Button(master=settings_window_frame,
                                    text='Create Board',
                                    command=partial(get_settings, height, length, mines))
    create_board_button.grid(row=3)

def get_settings(height, length, mines):
    height=height.get()
    length=length.get()
    mines=mines.get()
    print((height, length, mines))

    # Check if the entries were numbers
    if height.isdigit():
        height = int(height)
    else:
        height = 9

    if length.isdigit():
        length = int(length)
    else:
        length = 9

    if mines.isdigit():
        if int(mines) < height*length:
            mines = int(mines)
        else:
            mines = int(0.12345*length*height)
    else:
        mines = int(0.12345*length*height)

    print((height, length, mines))

    new_grid_window(height, length, mines)

def new_grid_window(height, length, mines):
    # Implement Reset Timer
    # Implement Reset Flag Count

    #frame_grid.forget()
    #frame_grid.destroy()  <- METTRE EN CLASSE POUR POUVOIR IMPLEMENTER CA LOL. sinon ca empile les grids

    game.create_board(length, height, mines)
    game.board.create_random_grid()
    game.board.change_0s_to_blank_spaces()

    global list_buttons # GLOBAL :( -> to reset the list of buttons
    list_buttons = []

    # FRAME GRID
    frame_grid=tk.Frame(frame_whole_window)
    frame_grid.grid(row=1, column=0, padx=5, pady=10)
    frame_grid.config(background='#C0C0C0')

    # Create board seen by the user
    for i, tile in enumerate(game.board.tiles):
        column = i%game.board.grid_size[1]
        row = i//game.board.grid_size[1]
        photo = image_full_tile
        btn = SpecialButton(frame_grid,
                            tile=tile,
                            text=str(tile.appearance),
                            rrow=row,
                            ccolumn=column,
                            #height=int(30/game.board.grid_size[0]), # Might not change anything since the size is based on image size
                            #width=int(90/game.board.grid_size[1]), # Might not change anything since the size is based on image size
                            image=photo,
                            )
        btn.grid(row=row, column=column)
        list_buttons.append(btn)



def smiley_face_switch(won=None, lost=None): # Ca fait flasher l'écran
    if smiley_button['image'] == 'pyimage14': # HARDCODED IMAGE
        smiley_button['image'] = image_smiley_surprised

    elif smiley_button['image'] == 'pyimage15': # HARDCODED IMAGE
        smiley_button['image'] = image_smiley

    if won is True:
        smiley_button['image'] = image_smiley_won

    if lost is True:
        smiley_button['image'] = image_smiley_lost




class SpecialButton(tk.Button):
    def __init__(self, master=None, tile=None, rrow=None, ccolumn=None, **kw):
        tk.Button.__init__(self,master,**kw)
        self.board = game.board
        self.tile = tile
        self.position = (rrow, ccolumn)

        # Choose which image the tile represents
        if self.tile.val == ' ':
            self.real_image = image_discovered_tile
        elif self.tile.val == 1:
            self.real_image = image_tile_1
        elif self.tile.val == 2:
            self.real_image = image_tile_2
        elif self.tile.val == 3:
            self.real_image = image_tile_3
        elif self.tile.val == 4:
            self.real_image = image_tile_4
        elif self.tile.val == 5:
            self.real_image = image_tile_5
        elif self.tile.val == 6:
            self.real_image = image_tile_6
        elif self.tile.val == 7:
            self.real_image = image_tile_7
        elif self.tile.val == 8:
            self.real_image = image_tile_8
        elif self.tile.val == '*':
            self.real_image = image_mine


        self.bind("<Button-1>", self.reveal)
        self.bind("<Button-2>", self.flag)

    def flag(self, event):
        smiley_face_switch()
        if self['text'] == 'F':
            self['text'] = self.tile.appearance
            self['image'] = image_full_tile # un peu weird de permettre de flagger des tiles révélées

        else:
            self['text'] = 'F'
            self['image'] = image_flag

    def reveal(self, event):
        x, y = self.tile.position
        if self.board.board_as_grid_hidden[x][y] == '*':
            smiley_face_switch(lost=True)
            end_game_window = tk.Toplevel()
            message = tk.Message(end_game_window, text='You lost.')
            message.pack()

            # Reveal board
            for btn in list_buttons:
                btn['text'] = btn.tile.val
                btn['image'] = btn.real_image
            self['image'] = image_red_mine

        elif self.board.board_as_grid_hidden[x][y] == ' ':
            smiley_face_switch()
            surrounding_tiles = self.board.blank_space_BFS(self.position)
            for tile in surrounding_tiles:
                tile_row, tile_col = tile
                for button in list_buttons:
                    if button.tile.position == tile:
                        btn = button
                btn['text'] = btn.tile.val
                btn.tile.appearance = btn.tile.val
                btn['image'] = btn.real_image

        else:
            self['text'] = self.tile.val
            self['image'] = self.real_image
            self.tile.appearance = self.tile.val
            smiley_face_switch()

        self.board.check_win_condition()
        if self.board.game_won:
            smiley_face_switch(won=True)
            end_game_window = tk.Toplevel()
            message = tk.Message(end_game_window, text='You won!')
            message.pack()

            # Reveal board
            for btn in list_buttons:
                btn['text'] = btn.tile.val
                btn['image'] = btn.real_image

        # MAYBE ADD THE MIDDLE BUTTON MECHANIC/COMMAND FROM THE REAL MINESWEEPER GAME



list_buttons = []

# Create behind the scenes board
game = Minesweeper()
game.create_board(9, 9, 3)
#game.create_board(3, 3, 1)
game.board.create_random_grid()
game.board.change_0s_to_blank_spaces()



# Create window
root = tk.Tk()
root.wm_title("Minesweeper")
root.iconbitmap("images/Minesweeper_Game_icon.ico")

# Load images
image_tile_1 = tk.PhotoImage(file='images/tile_1.png')
image_tile_2 = tk.PhotoImage(file='images/tile_2.png')
image_tile_3 = tk.PhotoImage(file='images/tile_3.png')
image_tile_4 = tk.PhotoImage(file='images/tile_4.png')
image_tile_5 = tk.PhotoImage(file='images/tile_5.png')
image_tile_6 = tk.PhotoImage(file='images/tile_6.png')
image_tile_7 = tk.PhotoImage(file='images/tile_7.png')
image_tile_8 = tk.PhotoImage(file='images/tile_8.png')
image_flag = tk.PhotoImage(file='images/flag.png')
image_mine = tk.PhotoImage(file='images/mine.png')
image_full_tile = tk.PhotoImage(file='images/full_tile.png')
image_discovered_tile = tk.PhotoImage(file='images/empty_tile.png')
image_red_mine = tk.PhotoImage(file='images/red_mine.png')
image_smiley = tk.PhotoImage(file='images/smiley.png')
image_smiley_surprised = tk.PhotoImage(file='images/smiley_surprised.png')
image_smiley_won = tk.PhotoImage(file='images/smiley_won.png')
image_smiley_lost = tk.PhotoImage(file='images/smiley_lost.png')

# Add menu
menubar = tk.Menu(root)
gamemenu = tk.Menu(menubar, tearoff=0)
gamemenu.add_command(label='Settings', command=open_settings_window)
menubar.add_cascade(label='Game', menu=gamemenu)

helpmenu = tk.Menu(menubar, tearoff=0)
helpmenu.add_command(label="You don't need help lol.", command=lambda: None)
menubar.add_cascade(label='Help', menu=helpmenu)

# Display Menu
root.config(menu=menubar)



# FRAME WHOLE WINDOW
frame_whole_window = tk.Frame(root)
frame_whole_window.grid()
frame_whole_window.config(background='#C0C0C0')

# FRAME OVER GRID
frame_over_grid = tk.Frame(frame_whole_window)
frame_over_grid.grid(row=0, column=0, padx=5, pady=5)
frame_over_grid.config(background='#C0C0C0') # highlightbackground change rien sur les frames


# FRAME FLAG COUNT
frame_flag_count = tk.Frame(frame_over_grid)
frame_flag_count.grid(row = 0, column = 0, sticky=tk.W, padx=5, pady=5)
frame_flag_count.config(background='#C0C0C0') # MAYBE
flag_count_placeholder = tk.Label(frame_flag_count,
                                    text='flag_count',
                                    relief=tk.SUNKEN
                                    ).grid()

# FRAME SMILEY
frame_smiley = tk.Frame(frame_over_grid)
frame_smiley.grid(row=0, column= 1, padx=5, pady=5)
frame_smiley.config(background='#C0C0C0') # MAYBE
smiley_button = tk.Button(frame_smiley,
                                    text='smiley',
                                    image=image_smiley,
                                    )
smiley_button.grid(row=0)

# FRAME TIME COUNTER
frame_time_counter = tk.Frame(frame_over_grid)
frame_time_counter.grid(row = 0, column = 2, sticky=tk.E, padx=5, pady=5)
frame_time_counter.config(background='#C0C0C0') # MAYBE
counter_placeholder = tk.Label(frame_time_counter,
                                    text='timer',
                                    relief=tk.SUNKEN
                                    ).grid()


# FRAME GRID
frame_grid=tk.Frame(frame_whole_window)
frame_grid.grid(row=1, column=0, padx=5, pady=10)
frame_grid.config(background='#C0C0C0')

# Create board seen by the user
for i, tile in enumerate(game.board.tiles):
    column = i%game.board.grid_size[1]
    row = i//game.board.grid_size[1]
    photo = image_full_tile
    btn = SpecialButton(frame_grid,
                        tile=tile,
                        text=str(tile.appearance),
                        rrow=row,
                        ccolumn=column,
                        #height=int(30/game.board.grid_size[0]), # Might not change anything since the size is based on image size
                        #width=int(90/game.board.grid_size[1]), # Might not change anything since the size is based on image size
                        image=photo,
                        )
    btn.grid(row=row, column=column)
    list_buttons.append(btn)

root.mainloop()
