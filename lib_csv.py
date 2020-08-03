# Library csv
# Functions Included in Library: 
# 	get_csv
# 	set_csv
# Author: Rebecca Mckeever
# Date: 11/18/2019
# Last Revised: 
# 	08/03/2020

# list libraries used

# Declare global constants (name in ALL_CAPS)
EXTENSION = '.csv'
COL_SEP = ','

# Function get_csv (file_name)
# Description:
#	reads data from csv file into a 2-dimensional array
# Calls:
#		ext_append()
# Parameters:
#		file_name		String
# Returns:
#		cell_arr		Array
def get_csv(file_name):

	# Declare and INITIALZE Local Variables (NOT parameters)
	row = []
	i = 0
	j = 0
	cell_arr = []
	infile = ''
	lines = []

	file_name = ext_append(file_name)

	infile = open(file_name, 'r')
	lines = infile.readlines()
	infile.close()

	for i in range( len(lines) ):
		row = lines[i].rstrip('\n')
		row = row.split( COL_SEP )

		for j in range( len(row) ):
			row[j] = int( row[j] )
		# End for

		cell_arr.append(row)
	# End for

	return cell_arr

# End function get_csv()

# Function set_csv (file_name, cell_arr)
# Description:
#	writes array data to csv file
# Calls:
#		ext_append()
# Parameters:
#		file_name		String
#		cell_arr		Array
# Returns:
#		none
def set_csv(file_name, cell_arr):

	# Declare and INITIALZE Local Variables (NOT parameters)
	i = 0
	j = 0
	outfile = ''
	line = ''

	file_name = ext_append(file_name)
	outfile = open(file_name, 'w')

	for i in range( len(cell_arr) ):
		line = ''
		for j in range( len( cell_arr[i] ) ):
			if ( j > 0 ):
				line += COL_SEP
			# End If

			line += str( cell_arr[i][j] )
		
		# End For
		line += '\n'
		outfile.write(line)

	# End For

	outfile.close()

# End function set_csv()

# Function ext_append (file_name)
# Description:
#	appends .csv extension to file name if not already present
# Calls:
#	none
# Parameters:
#		file_name		String
# Returns:
#		file_name		String
def ext_append (file_name):
	if ( not file_name.endswith(EXTENSION) ):
		file_name += EXTENSION
	# End If

	return file_name

# End function ext_append()
