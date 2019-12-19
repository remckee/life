# Library neighbor
# Functions Included in Library: 
# 	grid_neighbors
# 	cell_neighbors
# 	increment_bounds
# Author: Rebecca Mckeever
# Date: 10/18/2019
# Revised: 
# 	11/18/2019

# list libraries used

# Declare global constants (name in ALL_CAPS)

# Function grid_neighbors()
# Description:
#	determine the number of neighbors for each element of array
# Calls:
#	cell_neighbors()
# Parameters:
#       arr     Array
# Returns:
#	neighbors	Array

def grid_neighbors (arr):

	# Declare and INITIALZE Local Variables (NOT parameters)
	i = 0
	j = 0
	row = []
	neighbors = []

	for i in range( len(arr) ):
		row = []
		for j in range( len(arr[i]) ):
			row.append( cell_neighbors(arr, i, j) )
		# End For

		neighbors.append(row)
	# End For

	# Return the return variable, if any
	return neighbors

# End Function grid_neighbors()

# Function cell_neighbors()
# Description:
#	determine the number of neighbors for an individual cell within an array
# Calls:
#	increment_bounds()
# Parameters:
#       arr     		Array
#		cell_row		Integer
#		cell_col		Integer
# Returns:
#	neighbors	Integer

def cell_neighbors (arr, cell_row, cell_col):

	# Declare and INITIALZE Local Variables (NOT parameters)
	i = 0
	j = 0
	neighbors = 0
	rmin = cell_row
	rmax = cell_row
	cmin = cell_col
	cmax = cell_col
	rmin = increment_bounds(rmin,   (cell_row > 0),                     -1)
	rmax = increment_bounds(rmax,   (cell_row < len(arr)-1),             1)
	cmin = increment_bounds(cmin,   (cell_col > 0),                     -1)
	cmax = increment_bounds(cmax,   (cell_col < len(arr[cell_row])-1),   1)
	neighbors = 0

	for i in range(rmin, rmax+1):
		for j in range(cmin, cmax+1):
			if (arr[i][j] == 1):
				if ( (i != cell_row) or (j != cell_col) ):
					neighbors += 1
				# End If
			# End If
		# End For
	# End For

	# Return the return variable, if any
	return neighbors

# End Function cell_neighbors()

# Function increment_bounds()
# Description:
#	increments bounds up or down depending on boolean test
# Calls:
#	none
# Parameters:
#       value     		Integer
#		test			Boolean expression
#		increment		Integer
# Returns:
#		value			Integer

def increment_bounds (value, test, increment):

	# Declare and INITIALZE Local Variables (NOT parameters)

	if (test):
		value += increment
	# End If

	# Return the return variable, if any
	return value

# End Function increment_bounds()

