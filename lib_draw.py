# Library draw
# Functions Included in Library: 
# 	get_cell_color
# 	draw_cell
# 	draw_blank_grid
# 	draw_filled_grid
# 	redraw_grid
# 	extend_grid
# Author: Rebecca Mckeever
# Date: 11/18/2019
# Last Revised: 
# 	08/03/2020

# list libraries used
import tkinter

# Declare global constants (name in ALL_CAPS)
ON_COLOR = "black"
OFF_COLOR = "white"

# Function get_cell_color()
# Description:
#	translates state, which should be 0 or 1, to the corresponding fill color
# Calls:
#	none
# Parameters:
#       state		Integer
# Returns:
#		fill_color	String
def get_cell_color(state):
	# Declare and INITIALZE Variables (EVERY variable used in this main program)
	fill_color = OFF_COLOR
	if (state == 1):
		fill_color = ON_COLOR
	# End If
	return fill_color
# End function get_cell_color()

# Function draw_cell()
# Description:
#	draws a square of given width at x, y, with a state of 0 for "off" or 1 for "on"
# Calls:
#   get_cell_color()
# Parameters:
#		canvas		Canvas
#       x			Float
#       y			Float
#       width		Float
#       state		Integer
#		tag_list	Array
# Returns:
#	state			Integer
def draw_cell(canvas, x, y, width, state, tag_list):
	# Declare and INITIALZE Variables (EVERY variable used in this main program)
	fill_color = get_cell_color(state)
	canvas.create_rectangle(
		x,
		y,
		x+width,
		y+width,
		outline="#999",
		fill=fill_color,
		width=1,
		tags=tag_list)

	return state
# End draw_cell()

# Function draw_blank_grid()
# Description:
#	draws a rows x cols grid of cells of given width starting at x, y
# Calls:
#	draw_cell()
# Parameters:
#		canvas		Canvas
#       x			Float
#       y			Float
#       width		Float
#		rows		Integer
#		cols		Integer
#		tag			String
# Returns:
#		cell_grid	Array
def draw_blank_grid(canvas, x, y, width, rows, cols, tag):
	# Declare and INITIALZE Variables (EVERY variable used in this main program)
	i = 0
	j = 0
	pos_x = x
	pos_y = y
	cell_grid = []
	cell_row = []
	cell = ''

	for i in range(rows):
		cell_row = []
		for j in range(cols):
			pos_x = x + j*width
			pos_y = y + i*width
			cell = draw_cell(
				canvas,
				pos_x,
				pos_y,
				width,
				0,
				tag)
			cell_row.append(cell)
		# End For
		cell_grid.append(cell_row)	
	# End For

	return cell_grid
# End draw_blank_grid()

# Function draw_filled_grid()
# Description:
#	draws a grid of cells of given width starting at x, y
#	the states array specifies the dimensions of the grid and state of each cell
# Calls:
#	draw_cell()
# Parameters:
#		canvas		Canvas
#       x			Float
#       y			Float
#       width		Float
#       states		Array
#		tag			String
# Returns:
#		cell_grid	Array
def draw_filled_grid(canvas, x, y, width, states, tag):
	# Declare and INITIALZE Variables (EVERY variable used in this main program)
	i = 0
	j = 0
	pos_x = x
	pos_y = y
	row_col = ''
	tag_list = []
	cell_grid = []
	cell_row = []
	cell = ''

	for i in range( len(states) ):
		cell_row = []
		for j in range( len( states[i] ) ):
			pos_x = x + j*width
			pos_y = y + i*width
			row_col = "r" + str(i) + "c" + str(j)
			tag_list = [tag, row_col]
			cell = draw_cell(
				canvas,
				pos_x,
				pos_y,
				width,
				states[i][j],
				tag_list)
			cell_row.append(cell)
		# End For
		cell_grid.append(cell_row)
	# End For

	return cell_grid
# End draw_filled_grid()

# Function redraw_grid()
# Description:
#	redraws grid specified by tag with states specified by states
# Calls:
#	draw_filled_grid()
# Parameters:
#		canvas		Canvas
#       x			Float
#       y			Float
#       width		Float
#       states		Array
#		tag			String
# Returns:
#		cell_grid	Array
def redraw_grid(canvas, x, y, width, states, tag):
	# Declare and INITIALZE Variables (EVERY variable used in this main program)
	cell_grid = []

	canvas.delete(tag)
	cell_grid = draw_filled_grid(
		canvas,
		x,
		y,
		width,
		states,
		tag)

	return cell_grid

# End function redraw_grid()

# Function extend_grid()
# Description:
#	adds or removes grid cells according to new dimensions,
#	without changing the states of the remaining cells
# Calls:
#	redraw_grid()
# Parameters:
#		canvas		Canvas
#       x			Float
#       y			Float
#       width		Float
#       states		Array
#		tag			String
#		new_rows	Integer
#		new_cols	Integer
# Returns:
#		cell_grid	Array
def extend_grid(canvas, x, y, width, states, tag, new_rows, new_cols):
	# Declare and INITIALZE Variables (EVERY variable used in this main program)
	cur_rows = len(states)
	cur_cols = len( states[0] )
	cell_grid = []
	row_diff = new_rows - cur_rows
	col_diff = new_cols - cur_cols
	row = []
	row_frag = []
	i = 0

	if (row_diff < 0):
		for i in range(row_diff, 0, 1):
			del( states[i] )
		# End For
	elif (row_diff > 0):
		row = [0] * cur_cols
		for i in range(row_diff):
			states.append(row)
		# End For
	# End If

	if (col_diff < 0):
		for i in range( len(states) ):
			row = states[i]
			states[i] = row[0:new_cols]
		# End For
	elif (col_diff > 0):
		row_frag = [0] * col_diff
		for i in range( len(states) ):
			states[i] = states[i] + row_frag
		# End For
	# End If
	cell_grid = redraw_grid(
		canvas,
		x,
		y,
		width,
		states,
		tag)
	return cell_grid

# End extend_grid()

