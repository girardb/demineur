import tkinter as tk
from Minesweeper import Minesweeper
from Counter import Counter
from SpecialButton import SpecialButton
from functools import partial


class MinesweeperApp:
    def __init__(self):
        # Create the behind the scenes board
        self.height= 9
        self.length = 9
        self.mines = 10

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
        self.frame_over_grid.rowconfigure(0, weight=1)

        # FRAME FLAG COUNT
        self.frame_flag_count = tk.Canvas(self.frame_over_grid, width=45, height=25)
        self.frame_flag_count.grid(row = 0, column = 0, sticky=tk.W, padx=5, pady=5)
        self.frame_flag_count.config(background='black') # MAYBE

        self.counterDigit = Counter(self.frame_flag_count, 35, 5, 10, 3)
        self.counter10s = Counter(self.frame_flag_count, 20, 5, 10, 3)
        self.counter100s = Counter(self.frame_flag_count, 5, 5, 10, 3)

        # FRAME SMILEY
        self.frame_smiley = tk.Frame(self.frame_over_grid)
        self.frame_smiley.grid(row=0, column= 1, padx=5, pady=5)
        self.frame_smiley.config(background='#C0C0C0') # MAYBE
        self.smiley_button = tk.Button(self.frame_smiley,
                                            text='smiley',
                                            image=self.image_smiley,
                                            command=self.call_new_grid_window,
                                            )
        self.smiley_button.grid(row=0)

        # FRAME TIME COUNTER
        self.time = 0
        self.timer_status = False
        self.frame_time_counter = tk.Canvas(self.frame_over_grid, width=45, height=25)
        self.frame_time_counter.grid(row = 0, column = 2, sticky=tk.E, padx=5, pady=5)
        self.frame_time_counter.config(background='black') # MAYBE

        self.timeDigit = Counter(self.frame_time_counter, 35, 5, 10, 3)
        self.time10s = Counter(self.frame_time_counter, 20, 5, 10, 3)
        self.time100s = Counter(self.frame_time_counter, 5, 5, 10, 3)

        self.timeDigit.reveal_segments(0)
        self.time10s.reveal_segments(0)
        self.time100s.reveal_segments(0)

        self.create_hidden_and_button_board(self.length, self.height, self.mines)
        self.reset_flag_count()

        # Update clock
        self.root.after(1000, self.update_clock)

        self.root.mainloop()

    def smiley_face_switch(self, won=None, lost=None):
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

    def call_new_grid_window(self):
        self.new_grid_window(self.height, self.length, self.mines)

    def new_grid_window(self, height, length, mines):
        self.height = height
        self.length = length
        self.mines = mines

        # Kill grid frame
        self.frame_grid.forget()
        self.frame_grid.destroy()

        # Create new board
        self.create_hidden_and_button_board(length, height, mines)

        # Reset Flag Count
        self.reset_flag_count()

    def get_settings(self, height, length, mines, window):
        height=height.get()
        length=length.get()
        mines=mines.get()
        # HERE I CAN PROBABLY USE minesweeper.check_grid_configuration_inputs()
        # Check if the entries are numbers
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

        # Kill pop-up window
        self.create_board_and_destroy_window(height, length, mines, window)

    def open_settings_window(self):
        # add label to say that if you leave a field blank it will either be a 9 long axis or an appropriate number of mines generated
        settings_window = tk.Toplevel()
        settings_window.wm_title('Settings')

        settings_window_frame = tk.Frame(settings_window)
        settings_window_frame.grid()

        height = tk.StringVar()
        height_label = tk.Label(master=settings_window_frame, text='Height').grid(row=1, column=0)
        height_entry = tk.Entry(master=settings_window_frame, textvariable=height).grid(row=1, column=1)
        height.set('9')

        length = tk.StringVar()
        length_label = tk.Label(master=settings_window_frame, text='Length').grid(row=2, column=0)
        length_entry = tk.Entry(master=settings_window_frame, textvariable=length).grid(row=2, column=1)
        length.set('9')

        mines = tk.StringVar()
        mines_label = tk.Label(master=settings_window_frame, text='Number of Mines').grid(row=3, column=0)
        mines_entry = tk.Entry(master=settings_window_frame, textvariable=mines).grid(row=3, column=1)
        mines.set('10')

        beginner_button = tk.Button(master=settings_window_frame,
                                        text='Beginner',
                                        command=partial(self.set_difficulty, height, length, mines, settings_window, 0))
        beginner_button.grid(row=0, column=0)
        medium_button = tk.Button(master=settings_window_frame,
                                        text='Medium',
                                        command=partial(self.set_difficulty, height, length, mines, settings_window, 1))
        medium_button.grid(row=0, column=1)
        hard_button = tk.Button(master=settings_window_frame,
                                        text='Hard',
                                        command=partial(self.set_difficulty, height, length, mines, settings_window, 2))
        hard_button.grid(row=0, column=2)


        create_board_button = tk.Button(master=settings_window_frame,
                                        text='Create Board',
                                        command=partial(self.get_settings, height, length, mines, settings_window))
        create_board_button.grid(row=4, columnspan=3)

    def spawn_end_game_window(self, won=None, lost=None):
        # The buttons spawn on top of the label
        end_game_window = tk.Toplevel()
        end_game_frame = tk.Frame(end_game_window)
        end_game_frame.grid()

        if won is True:
            text='You won!'

        if lost is True:
            text='You lost.'

        message = tk.Label(end_game_frame, text=text).grid(row=0)
        play_again_button = tk.Button(master=end_game_frame,
                                    text='Play Again',
                                    command=partial(self.create_board_and_destroy_window, self.height, self.length, self.mines, end_game_window))

        play_again_button.grid(row=1, column=0)
        exit_button = tk.Button(master=end_game_frame,
                                text='Exit',
                                command=self.root.destroy)

        exit_button.grid(row=1, column=1)

    def update_clock(self):
        if self.timer_status is True:
            self.time += 1
            self.timeDigit.reveal_segments(self.time%10)
            self.time10s.reveal_segments((self.time//10)%10)
            self.time100s.reveal_segments((self.time//100)%10)

        self.root.after(1000, self.update_clock)

    def set_difficulty(self, height, length, mines, settings_window, difficulty):
        if difficulty == 0:
            height.set(9)
            length.set(9)
            mines.set(10)

        elif difficulty == 1:
            height.set(16)
            length.set(16)
            mines.set(40)

        elif difficulty == 2:
            height.set(16)
            length.set(30)
            mines.set(99)

    def create_hidden_and_button_board(self, length, height, mines):
        self.list_buttons = []
        self.game = Minesweeper()
        self.game.create_board(length, height, mines)
        self.game.board.create_random_grid()
        self.game.board.change_0s_to_blank_spaces()

        # CREATE GRID FRAME
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

        # Reset Smiley
        self.smiley_button['image'] = self.image_smiley

        # Reset Timer
        self.time = 0
        self.timer_status = False

    def reset_flag_count(self):
        flags_count = self.game.board.flags_count
        self.counterDigit.reveal_segments(flags_count%10)
        self.counter10s.reveal_segments((flags_count//10)%10)
        self.counter100s.reveal_segments((flags_count//100)%10)

    def create_board_and_destroy_window(self, height, length, mines, window):
        window.destroy()
        self.new_grid_window(height, length, mines)
