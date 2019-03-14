import tkinter as tk
from Minesweeper import Minesweeper
from functools import partial

# TODO:
# PAS OUBLIER DE FIX LES DEUX TESTS QUI FAIL POUR LE NIVEAU 2
# Clean le code -> jviens de le copy paste dans une class donc c'est messy un peu beaucoup
# ^ il y a genre un million de variables rattaché à un object MinesweeperApp. Jdevrais tu le breakdown encore plus? (breakdown en plus de classes)
# SHOULD I CHANGE THE DESIGN SO THAT THE FIRST TILE SELECTED IS AN EMPTY TILE # HOW
# MAYBE ADD THE MIDDLE BUTTON MECHANIC/COMMAND FROM THE REAL MINESWEEPER GAME
# ADD TIMER
# ADD FLAG COUNTER
# ^ utiliser le code du 7 segment display pis en mettre 3 collés  pis mettre les segments off à une couleure plus pale
# ^ capoter si le user fait spawner plus de 999 mines
# ADD BORDERS --- jpas capable d'ajouter de border sur la grid. ca a l'air un peu off
# Make menu friendlier
# ON THE GAME LOST WINDOW -> ASK TO EXIT OR PLAY AGAIN
# ON THE GAME WON WINDOW -> ASK TO EXIT OR PLAY AGAIN
# Clicking on help -> lol you don't need help -> should spawn a window with something funny
# niveau2 ->est-ce que je devrais print la grille avec les index quand la personne a gagner/perdu?
# le smiley et le surprised smiley sont centrés un peu différemment. eyesore
# Rajouter beginner, medium, hard level ?
# le smiley est supposé reset le jeu quand tu cliques dessus ou juste changer de smiley à surprised ?? lol

class MinesweeperApp:
    def __init__(self):
        self.list_buttons = []

        # Create behind the scenes board
        self.height=9
        self.length = 9
        self.mines = 10

        self.game = Minesweeper()
        self.game.create_board(self.length, self.height, self.mines)
        self.game.board.create_random_grid()
        self.game.board.change_0s_to_blank_spaces()

        # Create window
        self.root = tk.Tk()
        self.root.wm_title("Minesweeper")
        self.root.iconbitmap("images/Minesweeper_Game_icon.ico")

        self.load_images()

        # Add menu
        self.menubar = tk.Menu(self.root)
        gamemenu = tk.Menu(self.menubar, tearoff=0)
        gamemenu.add_command(label='Settings', command=self.open_settings_window)
        self.menubar.add_cascade(label='Game', menu=gamemenu)

        helpmenu = tk.Menu(self.menubar, tearoff=0)
        helpmenu.add_command(label="You don't need help lol.", command=lambda: None)
        self.menubar.add_cascade(label='Help', menu=helpmenu)

        # Display Menu
        self.root.config(menu=self.menubar)



        # FRAME WHOLE WINDOW
        self.frame_whole_window = tk.Frame(self.root)
        self.frame_whole_window.grid()
        self.frame_whole_window.config(background='#C0C0C0')

        # FRAME OVER GRID
        self.frame_over_grid = tk.Frame(self.frame_whole_window)
        self.frame_over_grid.grid(row=0, column=0, padx=5, pady=5)
        self.frame_over_grid.config(background='#C0C0C0') # highlightbackground change rien sur les frames


        # FRAME FLAG COUNT
        self.frame_flag_count = tk.Frame(self.frame_over_grid)
        self.frame_flag_count.grid(row = 0, column = 0, sticky=tk.W, padx=5, pady=5)
        self.frame_flag_count.config(background='#C0C0C0') # MAYBE
        self.flag_count_placeholder = tk.Label(self.frame_flag_count,
                                            text='flag_count',
                                            relief=tk.SUNKEN
                                            ).grid()

        # FRAME SMILEY
        self.frame_smiley = tk.Frame(self.frame_over_grid)
        self.frame_smiley.grid(row=0, column= 1, padx=5, pady=5)
        self.frame_smiley.config(background='#C0C0C0') # MAYBE
        self.smiley_button = tk.Button(self.frame_smiley,
                                            text='smiley',
                                            image=self.image_smiley,
                                            command=self.smiley_face_switch,
                                            )
        self.smiley_button.grid(row=0)

        # FRAME TIME COUNTER
        self.frame_time_counter = tk.Frame(self.frame_over_grid)
        self.frame_time_counter.grid(row = 0, column = 2, sticky=tk.E, padx=5, pady=5)
        self.frame_time_counter.config(background='#C0C0C0') # MAYBE
        self.counter_placeholder = tk.Label(self.frame_time_counter,
                                            text='timer',
                                            relief=tk.SUNKEN
                                            ).grid()


        # FRAME GRID
        self.frame_grid=tk.Frame(self.frame_whole_window)
        self.frame_grid.grid(row=1, column=0, padx=5, pady=10)
        self.frame_grid.config(background='#C0C0C0')

        # Create board seen by the user
        for i, tile in enumerate(self.game.board.tiles):
            column = i%self.game.board.grid_size[1]
            row = i//self.game.board.grid_size[1]
            photo = self.image_full_tile
            btn = SpecialButton(self.frame_grid,
                                tile=tile,
                                text=str(tile.appearance),
                                rrow=row,
                                ccolumn=column,
                                image=photo,
                                app=self,
                                )
            btn.grid(row=row, column=column)
            self.list_buttons.append(btn)

        self.root.mainloop()

    def smiley_face_switch(self, won=None, lost=None): # Ca fait flasher l'écran
        if self.smiley_button['image'] == 'pyimage14': # HARDCODED IMAGE
            self.smiley_button['image'] = self.image_smiley_surprised

        elif self.smiley_button['image'] == 'pyimage15': # HARDCODED IMAGE
            self.smiley_button['image'] = self.image_smiley

        if won is True:
            self.smiley_button['image'] = self.image_smiley_won

        if lost is True:
            self.smiley_button['image'] = self.image_smiley_lost

    def load_images(self):
        # Load images
        self.image_tile_1 = tk.PhotoImage(file='images/tile_1.png')
        self.image_tile_2 = tk.PhotoImage(file='images/tile_2.png')
        self.image_tile_3 = tk.PhotoImage(file='images/tile_3.png')
        self.image_tile_4 = tk.PhotoImage(file='images/tile_4.png')
        self.image_tile_5 = tk.PhotoImage(file='images/tile_5.png')
        self.image_tile_6 = tk.PhotoImage(file='images/tile_6.png')
        self.image_tile_7 = tk.PhotoImage(file='images/tile_7.png')
        self.image_tile_8 = tk.PhotoImage(file='images/tile_8.png')
        self.image_flag = tk.PhotoImage(file='images/flag.png')
        self.image_mine = tk.PhotoImage(file='images/mine.png')
        self.image_full_tile = tk.PhotoImage(file='images/full_tile.png')
        self.image_discovered_tile = tk.PhotoImage(file='images/empty_tile.png')
        self.image_red_mine = tk.PhotoImage(file='images/red_mine.png')
        self.image_smiley = tk.PhotoImage(file='images/smiley.png')
        self.image_smiley_surprised = tk.PhotoImage(file='images/smiley_surprised.png')
        self.image_smiley_won = tk.PhotoImage(file='images/smiley_won.png')
        self.image_smiley_lost = tk.PhotoImage(file='images/smiley_lost.png')

    def new_grid_window(self, height, length, mines):
        # Implement Reset Timer
        # Implement Reset Flag Count

        self.height = height
        self.length = length
        self.mines = mines

        self.frame_grid.forget()
        self.frame_grid.destroy()

        self.game.create_board(length, height, mines)
        self.game.board.create_random_grid()
        self.game.board.change_0s_to_blank_spaces()

        self.list_buttons = []

        # FRAME GRID
        self.frame_grid=tk.Frame(self.frame_whole_window)
        self.frame_grid.grid(row=1, column=0, padx=5, pady=10)
        self.frame_grid.config(background='#C0C0C0')

        # Create board seen by the user
        for i, tile in enumerate(self.game.board.tiles):
            column = i%self.game.board.grid_size[1]
            row = i//self.game.board.grid_size[1]
            photo = self.image_full_tile
            btn = SpecialButton(self.frame_grid,
                                tile=tile,
                                text=str(tile.appearance),
                                rrow=row,
                                ccolumn=column,
                                #height=int(30/game.board.grid_size[0]), # Might not change anything since the size is based on image size
                                #width=int(90/game.board.grid_size[1]), # Might not change anything since the size is based on image size
                                image=photo,
                                app=self,
                                )
            btn.grid(row=row, column=column)
            self.list_buttons.append(btn)

    def get_settings(self, height, length, mines):
        height=height.get()
        length=length.get()
        mines=mines.get()
        # HERE I CAN PROBABLY USE minesweeper.check_grid_configuration_inputs()
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

        self.new_grid_window(height, length, mines)

    def open_settings_window(self):
        # add label to say that if you leave a field blank it will either be a 9 long axis or an appropriate number of mines generated
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
                                        command=partial(self.get_settings, height, length, mines))
        create_board_button.grid(row=3)

    def spawn_end_game_window(self, won=None, lost=None):
        # The buttons spawn on top of the label
        end_game_window = tk.Toplevel()
        end_game_frame = tk.Frame(end_game_window)
        end_game_frame.grid()

        if won is True:
            text='You won!'

        if lost is True:
            text='You lost.'

        message = tk.Label(end_game_window, text=text).grid(row=0)
        play_again_button = tk.Button(master=end_game_frame,
                                    text='Play Again.',
                                    command=partial(self.new_grid_window, self.height, self.length, self.mines))

        play_again_button.grid(row=1, column=0)
        exit_button = tk.Button(master=end_game_frame,
                                text='Exit.',
                                command=self.root.destroy)

        exit_button.grid(row=1, column=1)




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

        else:
            self['text'] = 'F'
            self['image'] = self.app.image_flag

    def reveal(self, event):
        x, y = self.tile.position
        if self.board.board_as_grid_hidden[x][y] == '*':
            self.app.smiley_face_switch(lost=True)
            self.app.spawn_end_game_window(lost=True)

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

            # Reveal board
            for btn in self.app.list_buttons:
                btn['text'] = btn.tile.val
                btn['image'] = btn.real_image

        # MAYBE ADD THE MIDDLE BUTTON MECHANIC/COMMAND FROM THE REAL MINESWEEPER GAME

if __name__ == '__main__':
    # Startup time est un peu long. Faudrait que je check ca prend combien de RAM aussi, d'un coup que j'exagère.
    app = MinesweeperApp()
