# Program gamelife.py
# Description: 
#   simulates game of life generations
# Author: Rebecca Mckeever
# Date: 10/18/2019
# Last Revised: 
#   08/05/2020

# list libraries used
import lib_neighbor
import lib_draw
import lib_csv
import os
from tkinter import ttk
from tkinter import messagebox
from tkinter import colorchooser
from tkinter import *

# Declare global constants (name in ALL_CAPS)
PAT_FOLDER = 'patterns/'
DATA_FOLDER = 'data_files/'
START_FILE = 'blank'
USER_FILES = DATA_FOLDER + 'patterns.txt'
MOVES_LOG = DATA_FOLDER + 'moves.txt'
DEFAULT_FILENAME = 'mypattern'
EXTENSION = '.csv'
CELL_SIZE = 20
CELL_TAG = 'cell'
DEF_DELAY = 800
DEF_SPEED = 1000/DEF_DELAY
SLOW_SPEED = 0.5
FAST_SPEED = 10
SPINER_MIN = 1
SPINER_MAX = 30
ON_COLOR = 'black'
OFF_COLOR = 'white'
SPACER = 5
LIST_WIDTH = 12
ENTRY_WIDTH = LIST_WIDTH
INTRO_WRAP = 300

class Game(Tk):
    def __init__(self):
        Tk.__init__(self)

        # Declare and INITIALZE Variables (EVERY variable used in this main program)
        self.grid_coords = {'x': 2, 'y': 2}
        self.intro =    {
                            'row': 0,
                            'col': 0,
                            'rowspan': 4,
                            'colspan': 4
                        }
        self.label =    {
                            'col': self.intro['col'] + self.intro['colspan'],
                            'colspan': 2
                        }
        self.inputs =   {
                            'row': list( range(0, 4) ),
                            'col': self.label['col'] + self.label['colspan'],
                            'rowspan': 1,
                            'colspan': 1
                        }
        self.buttons =  {
                            'row': self.inputs['row'][3] + 1,
                            'col': list( range(0, 4) )
                        }
        self.scale =    {
                            'row': self.buttons['row'],
                            'col': self.buttons['col'][3] + 2,
                            'rowspan': 1,
                            'colspan': 3
                        }
        self.canvas =   {
                            'row': 1,
                            'col': 0,
                            'rowspan': 1,
                            'colspan': 1
                        }
        self.keep_going = False
        self.file_names = []
        self.cell_arr = [
            [0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0]
        ]
        self.width = 0
        self.height = 0
        self.num_rows = IntVar()
        self.num_cols = IntVar()
        self.list_selection = StringVar()
        self.save_name = StringVar()
        self.options_list = ''
        self.cell_canvas = ''
        self.row_spin = ''
        self.col_spin = ''
        self.scale_value = DoubleVar()
        self.container = Frame(self)
        self.controls = Frame(self.container)
        self.current_move = 0

        try:
            # set up initial cell state array
            self.cell_arr = lib_csv.get_csv(PAT_FOLDER + START_FILE)
            self.width = self.canvas_width()
            self.height = self.canvas_height()

            # set up entry variables
            self.num_rows.set( self.number_rows() )
            self.num_cols.set( self.number_cols() )
            self.save_name.set(DEFAULT_FILENAME)
            self.scale_value.set(DEF_SPEED)
            self.file_names = self.get_file_names()

            # set up window components
            self.show_list()
            self.buttons_bar()
            self.display_scale()
            self.show_intro()
            self.display_canvas(self.cell_arr)
            self.display_spiners()
            self.display_save()
            self.controls.grid(row=0)
            self.container.grid(
                row=0,
                column=0,
                padx=2*SPACER,
                pady=2*SPACER)

            # set up blank moves log file
            self.init_moves_log(MOVES_LOG)

        except Exception as err:
            print( err )
        # End Try

    # End __init__

    def calc_delay(self, speed):
        delay = 1000/speed
        return int(delay)
    # End calc_delay()

    def buttons_bar(self):
        go_button = Button(self.controls,
            text='Go',
            command=self.go,
            bg='#28a745', activebackground='#218838',
            fg='white', activeforeground='white')
        go_button.grid(
            row=self.buttons['row'],
            column=self.buttons['col'][0],
            pady=SPACER,
            sticky=E+W)

        stop_button = Button(self.controls,
            text='Stop',
            command=self.stop,
            bg='#dc3545', activebackground='#c82333',
            fg='white', activeforeground='white')
        stop_button.grid(
            row=self.buttons['row'],
            column=self.buttons['col'][1],
            pady=SPACER,
            sticky=E+W)

        forward_button = Button(self.controls,
            text='Forward',
            command=self.forward,
            bg='#ffc107', activebackground='#e0a800')
        forward_button.grid(
            row=self.buttons['row'],
            column=self.buttons['col'][2],
            pady=SPACER,
            sticky=E+W)

        clear_button = Button(self.controls,
            text='Clear',
            command=self.clear_grid,
            bg='#007bff', activebackground='#0069d9',
            foreground='white', activeforeground='white')
        clear_button.grid(
            row=self.buttons['row'],
            column=self.buttons['col'][3],
            pady=SPACER,
            sticky=E+W)
    # End function buttons_bar()

    def display_scale(self):
        scale_label = Label(self.controls, text='speed:')
        scale_label.grid(
            row=self.scale['row'],
            column=self.scale['col'] - 1,
            rowspan=self.scale['rowspan'],
            padx=SPACER,
            sticky=E)

        speed_scale = Scale(self.controls,
            from_=SLOW_SPEED,
            to=FAST_SPEED,
            orient=HORIZONTAL,
            resolution=0.05,
            variable=self.scale_value,
            sliderlength=5,
            tickinterval=9.5,
            length=300)
        speed_scale.grid(
            row=self.scale['row'],
            column=self.scale['col'],
            rowspan=self.scale['rowspan'],
            columnspan=self.scale['colspan'],
            sticky=W)
    # End function display_scale()

    def show_list(self):
        list_label = Label(self.controls, text='initial state:')
        list_label.grid(
            row=self.inputs['row'][0],
            column=self.label['col'],
            columnspan=self.label['colspan'],
            padx=SPACER,
            sticky=E)
        self.list_selection.set(START_FILE)

        self.options_list = ttk.Combobox(self.controls,
            values=self.file_names,
            textvariable=self.list_selection,
            width=LIST_WIDTH)
        self.options_list.bind('<<ComboboxSelected>>', self.list_callback)
        self.options_list.bind('<Return>', self.list_callback)
        self.options_list.grid(
            row=self.inputs['row'][0],
            column=self.inputs['col'],
            columnspan=self.inputs['colspan'],
            padx=SPACER,
            sticky=E+N+W+S)
    # End function show_list()

    def show_intro(self):
        intro_text = "Draw a custom pattern by clicking cells to toggle their states, or select a pattern from the list. Or, you can type the file name into the initial state field and then press the Enter key. Use the Go, Stop, and Forward buttons to see the cells evolve according to the rules of the Game of Life. For more info, see the READ_ME file. "

        intro_label = Label(self.controls,
            text=intro_text,
            justify=LEFT,
            wraplength=INTRO_WRAP)
        intro_label.grid(
            row=self.intro['row'],
            column=self.intro['col'],
            rowspan=self.intro['rowspan'],
            columnspan=self.intro['colspan'],
            sticky=N+E+W)
    # End function show_intro()

    def display_canvas(self, cell_arr):
        self.cell_canvas = Canvas(self.container,
            width=self.width,
            height=self.width)
        self.cell_canvas.tag_bind(CELL_TAG,
            '<Button-1>',
            self.click_cells)
        self.cell_canvas.grid(
            row=self.canvas['row'],
            column=self.canvas['col'],
            columnspan=self.canvas['colspan'],
            padx=0,
            pady=SPACER)
        lib_draw.draw_filled_grid(self.cell_canvas,
            self.grid_coords['x'],
            self.grid_coords['y'],
            CELL_SIZE,
            cell_arr,
            CELL_TAG)
    # End function display_canvas()

    def display_spiners(self):
        row_label = Label(self.controls, text='rows:')
        row_label.grid(
            row=self.inputs['row'][1],
            column=self.label['col'],
            columnspan=self.label['colspan'],
            padx=SPACER,
            sticky=E)
        self.row_spin = Spinbox(self.controls,
            from_=SPINER_MIN,
            to=SPINER_MAX,
            textvariable=self.num_rows,
            command=self.adjust_dimensions,
            width=LIST_WIDTH)
        self.row_spin.grid(
            row=self.inputs['row'][1],
            column=self.inputs['col'],
            columnspan=self.inputs['colspan'],
            padx=SPACER,
            sticky=N+E+W+S)

        col_label = Label(self.controls, text='columns:')
        col_label.grid(
            row=self.inputs['row'][2],
            column=self.label['col'],
            columnspan=self.label['colspan'],
            padx=SPACER,
            sticky=E)
        self.col_spin = Spinbox(self.controls,
            from_=SPINER_MIN,
            to=SPINER_MAX,
            textvariable=self.num_cols,
            command=self.adjust_dimensions,
            width=LIST_WIDTH)
        self.col_spin.grid(
            row=self.inputs['row'][2],
            column=self.inputs['col'],
            columnspan=self.inputs['colspan'],
            padx=SPACER,
            sticky=N+E+W+S)
    # End display_spiners()

    def display_save(self):
        name_label = Label(self.controls,
            text="save current pattern as:",
            wraplength=100)
        name_label.grid(
            row=self.inputs['row'][3],
            column=self.label['col'],
            columnspan=self.label['colspan'],
            padx=SPACER,
            sticky=E)
        name_entry = Entry(self.controls,
            width=ENTRY_WIDTH,
            textvariable=self.save_name)
        name_entry.grid(
            row=self.inputs['row'][3],
            column=self.inputs['col'],
            columnspan=self.inputs['colspan'],
            padx=SPACER,
            sticky=N+E+W+S)

        save_button = Button(self.controls,
            text='Save',
            command=self.save_pattern)
        save_button.grid(
            row=self.inputs['row'][3],
            column=self.inputs['col']+self.inputs['colspan'],
            sticky=N+W+S)
    # End display_save()

    def error_dialog(self, title, message):
        messagebox.showerror(title, message)
    # End error_dialog()

    def confirm_dialog(self, title, message):
        response = messagebox.askokcancel(title, message)
        return response
    # End confirm_dialog()

    def message_dialog(self, title, message):
        messagebox.showinfo(title, message)
    # End message_dialog()

    def get_file_names(self):
        patterns_file = ''
        file_names = []
        index = 0
        sys_msg = ''

        try:
            file_names = os.listdir(path=PAT_FOLDER)
            file_names.sort()

        except Exception as sys_msg:
            print ( sys_msg )

            try:
                patterns_file = open(USER_FILES, 'r')
                file_names = patterns_file.readlines()
                patterns_file.close()

            except Exception as sys_msg:
                print ( sys_msg )

            # End Try

        # update patterns file with current directory contents
        else:
            patterns_file = open(USER_FILES, 'w')

            for index in range( len( file_names ) ):
                file_names[index] = lib_csv.ext_remove(file_names[index])
                patterns_file.write(file_names[index] + '\n')
            # End For

            patterns_file.close()

        # End Try

        for index in range( len( file_names ) ):
            file_names[index] = file_names[index].rstrip('\n')
        # End For

        return file_names
    # End get_file_names

    def adjust_dimensions(self):
        row_val = int( self.row_spin.get() )
        col_val = int( self.col_spin.get() )

        in_range =  (row_val >= SPINER_MIN) \
                and (row_val <= SPINER_MAX) \
                and (col_val >= SPINER_MIN) \
                and (col_val <= SPINER_MAX)

        self.cell_arr = self.get_cell_states()

        if (in_range):
            lib_draw.extend_grid(self.cell_canvas,
                self.grid_coords['x'],
                self.grid_coords['y'],
                CELL_SIZE,
                self.cell_arr,
                CELL_TAG,
                int(self.row_spin.get() ),
                int(self.col_spin.get() ) )
            self.resize_canvas()
        else:
            self.error_dialog("Invalid", "invalid grid dimensions")
        # End if
    # End function adjust_dimensions()

    def number_cols(self):
        row = self.cell_arr[0]
        numb_cols = len(row)
        return numb_cols
    # End function

    def number_rows(self):
        numb_rows = len(self.cell_arr)
        return numb_rows
    # End function

    def canvas_width(self):
        numb_cells = self.number_cols()
        c_width = numb_cells*CELL_SIZE + 1*(numb_cells + 1)
        return c_width
    # End function

    def canvas_height(self):
        numb_cells = self.number_rows()
        c_height = numb_cells*CELL_SIZE + 1*(numb_cells + 1)
        return c_height
    # End function

    def go(self):
        self.keep_going = True
        self.cont_gen()
    # End function

    def stop(self):
        self.keep_going = False
    # End function

    def resize_canvas(self):
        self.width = self.canvas_width()
        self.height = self.canvas_height()
        self.cell_canvas.configure(
            width=self.width,
            height=self.height)
        self.num_cols.set( self.number_cols() )
        self.num_rows.set( self.number_rows() )
    # End function

    def forward(self):
        self.cell_arr = self.draw_generation(
                            CELL_TAG,
                            self.get_cell_states() )
    # End function forward()

    def cont_gen(self):
        if (self.keep_going):
            self.forward()
            self.after(
                self.calc_delay( self.scale_value.get() ),
                self.cont_gen)
        # End if
    # End function

    def list_callback(self, event):
        file_name = event.widget.get()
        full_file_name = lib_csv.ext_append(file_name)
        error = True
        sys_msg = ''
        error_msg = "Pattern file " + full_file_name + " is not valid or does not exist."

        try:
            if ( file_name in self.get_file_names() ):
                self.cell_arr = lib_csv.get_csv(PAT_FOLDER + file_name)
            # End If

        except Exception as sys_msg:
            print ( sys_msg )

        else:
            error = False
            self.resize_canvas()
            lib_draw.redraw_grid(self.cell_canvas,
                self.grid_coords['x'],
                self.grid_coords['y'],
                CELL_SIZE,
                self.cell_arr,
                CELL_TAG)

        # End Try

        if ( error ):
            self.error_dialog("Error", error_msg)
        # End If

    # End function list_callback()

    def click_cells(self, event):
        cur_id = self.cell_canvas.find_withtag("current")
        self.unclick_cell(cur_id)
    # End function click_cells()

    def unclick_cell(self, cell_id):
        cur_fill = self.cell_canvas.itemcget(cell_id, "fill")
        if (cur_fill == ON_COLOR):
            self.cell_canvas.itemconfig(cell_id, fill=OFF_COLOR)
        elif (cur_fill == OFF_COLOR):
            self.cell_canvas.itemconfig(cell_id, fill=ON_COLOR)
        # End if
    # End function unclick_cell()

    def clear_grid(self):
        arr = self.cell_canvas.find_withtag(CELL_TAG)
        for i in range( len(arr) ):
            self.cell_canvas.itemconfig(arr[i], fill=OFF_COLOR)
        # End For
    # End function

    def save_pattern(self):
        # Declare and INITIALZE Variables (EVERY variable used in this main program)
        arr = []
        file_name = self.save_name.get()
        full_file_name = lib_csv.ext_append(file_name)
        save_file = False
        patterns_file = ''
        overwrite_msg = "The folder already contains the file " + full_file_name \
            + ". Do you want to overwrite that file with the current pattern?"
        confirm_msg = "Really save current pattern as " + full_file_name + "?"
        saved_msg = "The current pattern was saved as " + full_file_name + "."

        if (file_name in self.file_names):
            if ( self.confirm_dialog("Save As", overwrite_msg) ):
                save_file = True
            # End If
        elif ( self.confirm_dialog("Save As", confirm_msg) ):
            save_file = True
        else:
            save_file = False
        # End If

        if (save_file):
            arr = self.get_cell_states()
            lib_csv.set_csv(PAT_FOLDER + file_name, arr)

            if not ( file_name in self.get_file_names() ):
                try:
                    patterns_file = open(USER_FILES, 'a')
                    patterns_file.write(file_name + '\n')
                    patterns_file.close()

                except Exception as sys_msg:
                    print ( sys_msg )

                # End Try

            # End If

            self.file_names = self.get_file_names()
            self.options_list.configure(values=self.file_names)
            self.message_dialog("Saved", saved_msg)

        # End If
    # End function save_pattern()

    def get_cell_states(self):
        cell_list = self.cell_canvas.find_withtag(CELL_TAG)
        arr_row = []
        states = []
        coord_list = self.cell_canvas.coords( cell_list[0] )
        y = coord_list[1]
        cell_id = 0
        fill_color = ''
        state = 0

        for i in range( len(cell_list) ):
            cell_id = cell_list[i]
            fill_color = self.cell_canvas.itemcget(cell_id, "fill")
            state = self.get_cell_state(fill_color)
            coord_list = self.cell_canvas.coords(cell_id)

            if (y == coord_list[1] ):
                arr_row.append(state)
            else:
                states.append(arr_row)
                arr_row = [state]
            # End If

            y = coord_list[1]
        # End For
        states.append(arr_row)
        return states
    # End function get_cell_states()

    def get_cell_state(self, fill_color):
        state = 0
        if (fill_color == ON_COLOR):
            state = 1
        # End If
        return state
    # End function get_cell_state()

    def draw_generation(self, tag, cell_arr):
        # Declare and INITIALZE Local Variables (NOT parameters)
        row = 0
        col = 0
        neighbor_arr = lib_neighbor.grid_neighbors(cell_arr)

        for row in range( len(cell_arr) ):
            for col in range( len( cell_arr[row] ) ):
                cell_arr[row][col] = int( self.generation ( cell_arr[row][col],
                        neighbor_arr[row][col] ) )

            # End For
        # End For

        self.resize_canvas()
        lib_draw.redraw_grid(self.cell_canvas,
            self.grid_coords['x'],
            self.grid_coords['y'],
            CELL_SIZE,
            cell_arr,
            tag)
        return cell_arr
    # End function draw_generation()

    # Function generation (cell, neighbors)
    # Description:
    #   determines if cell will be dead or alive in next generation
    #   based on current state and number of neighbors, based on the Game of Life rules:
    #   1.  Any live cell with two or three neighbors survives.
    #   2.  Any dead cell with three live neighbors becomes a live cell.
    #   3.  All other live cells die in the next generation.
    #       Similarly, all other dead cells stay dead.
    # Calls:
    #   none
    # Parameters:
    #       cell            Integer
    #       neighbors       Integer
    # Returns:
    #       cell
    def generation (self, state, neighbors):

        # Declare and INITIALZE Local Variables (NOT parameters)

        if ( neighbors == 3 ):
            state = 1
        elif ( ( neighbors == 2 ) and ( state == 1 ) ):
            state = 1
        else:
            state = 0
        # End If

        # Return the return variable, if any
        return state
    # End Function generation()

    # Function init_moves_log (moves_log)
    # Description:
    #   initializes a blank moves log file named moves_log, sets current move to 0
    # Calls:
    #   none
    # Parameters:
    #       moves_log       String
    # Returns:
    #       moves_log       String
    def init_moves_log (self, moves_log):
        try:
            moves_log_file = open(moves_log, 'w')
            moves_log_file.write('')
            moves_log_file.close()

        except Exception as sys_msg:
            print ( sys_msg )

        # End Try

        self.current_move = 0

        return moves_log

    # End function init_moves_log()

if __name__ == "__main__":
    root = Game()
    root.mainloop()

