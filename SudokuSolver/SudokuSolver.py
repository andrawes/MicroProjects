import numpy as np 
import math
import copy
import sys

####################### Sudoku Class ############################## 
class Sudoku():
	def __init__(self, puzzle):
		self.puzzle = puzzle
		print("Initial Grid")
		self.sudoku_print()
		self.allowed = self.__initialize_allowed()
		self.update_allowed()
		self.update_sudoku()
		return None

	# Initialize datastructure of 9x9 items where each item contains
	# a list of allowed numbers
	def __initialize_allowed(self):
		allowed = [[None]*9 for i in range(9)]
		row_count = 0
		col_count = 0
		for row in self.puzzle: 
			col_count = 0
			for val in row: 
				# If the location is empty, then all numbers are allowed
				if val == 0:
					allowed[row_count][col_count] = [i for i in range(1,10)] 
				# If the location is not empty, then only one number is allowed
				else: 
					allowed[row_count][col_count] = [val]
				col_count += 1
			row_count += 1	
		return allowed

	# Returns true if the game is complete correctly
	def is_solved(self):
		if self.is_false(): 
			print("Puzzle contains error")
			return False
		else: 
			# Check if there are any empty positions
			if 0 in self.puzzle: 
				return False
			else: 
				return True

	# Check if there are any faults
	def is_false(self):
		contains_fault = False
		# First check row-wise and column-wise
		for x in range(0,9):
			dada = [0]*9
			dada2 = [0]*9

			# See if there is redundant number at row x
			for i in self.puzzle[x]:
				if i != 0:
					dada[i-1]=dada[i-1]+1
					if dada[i-1]>1:
						#print("problem at row: "+str(x))
						contains_fault = True

			# See if there is redundant number at column x
			for i in self.puzzle[:,x]:
				if i != 0:
					dada2[i-1]=dada2[i-1]+1
					if dada2[i-1]>1:
						#print("Problem at column "+str(x))
						contains_fault = True

		return contains_fault

	# This method prints the sudoku puzzle in a readable fashion
	def sudoku_print(self):
		table = self.puzzle
		row_counter = 0
		for row in table:
			if (row_counter % 3 == 0): 
				print("-----------------------------------")
			print("|| "+ str(row[0:3])),
			print(' | '+ str(row[3:6])+' | '),
			print(str(row[6:9]) + " ||")
			row_counter += 1
			if (row_counter == 9):
				print("-----------------------------------")

	# This method writes a value to the given grid position
	def sudoku_write(self, r, c, val):
		self.puzzle[r][c]= val
		#print("writing to r: "+str(r)+" c: "+str(c))
		#self.sudoku_print()

	# This method looks in a 3x3 square to see if any of the values
	# specified in the list values_to_test belongs to the 3x3 square
	def in_square(self, r, c, values_to_test):
		# Initialize empty set
		found_items = set()
		# Iterate over all the values whose presence we want to test
		for i in values_to_test:
			# Find the coordinates/indices of the square to which the
			# the position specified by r and c belongs
			r_start_index = int(3*math.floor(r/3))
			c_start_index = int(3*math.floor(c/3))

			if i in (self.puzzle[r_start_index:r_start_index+3,c_start_index:c_start_index+3]):
				found_items.add(i)
		return found_items

	# This method looks in a 1x9 row vector to see if any of the 
	# values specified in the list values_to_test belongs to the row
	def in_row(self, r, values_to_test):
		# Initialize empty set
		found_items = set()
		# Iterate over all the values whose presence we want to test
		for i in values_to_test:
			if i in self.puzzle[r]:
				found_items.add(i)
		return found_items

	# This method looks in a 9x1 column vector to see if any of the 
	# values specified in the list values_to_test belongs to the column
	def in_column(self, c, values_to_test):
		# Initialize empty set
		found_items = set()
		# Iterate over all the values whose presence we want to test
		for i in values_to_test:
			if i in self.puzzle[:,c]:
				found_items.add(i)
		return found_items

	# Scan through the datastructure of allowed numbers in each position
	# and evaluate if that should still be the case by checking if the 
	# value exists in the line, column, or square
	def update_allowed(self):
		for r in range (0,9):
			for c in range(0,9):
				# If only one number is allowed, then there is no need to 
				# update
				if len(self.allowed[r][c]) == 1: 
					pass
				else: 
					# If the grid position is not empty, then this could be 
					# a new value that has been written and thus the list of 
					# allowed numbers here should be reduced to just 1
					if (self.puzzle[r][c] != 0):
						self.allowed[r][c]= [self.puzzle[r][c]]
					else:
						# Chose from the set of allowed numbers those which cannot
						# be allowed anymore due to their presence in the row, column,
						# or square.
						is_in_row = self.in_row(r,self.allowed[r][c])
						is_in_column = self.in_column(c,self.allowed[r][c])
						is_in_square = self.in_square(r,c,self.allowed[r][c])
						
						# Create the union set of all disallowed numbers for a particular
						# position
						prohibited_numbers = is_in_row.union(is_in_column, is_in_square)
						# Create the set of allowed numbers which have not been prohibited
						current_allowed = set(self.allowed[r][c]) 
						remaining_items = current_allowed.difference(prohibited_numbers)
						# Update the datastructure of allowed items
						self.allowed[r][c] = list(remaining_items)
		
		#self.update_sudoku()

	# For a position given by R and C, this method checks all the positions
	# of the same row
	def allowed_in_other_positions_row(self, R, C):
		 # Initialize the set of allowed numbers in other positions of the same
		 # row
		allowed = set()
		row_range = set([x for x in range(0,9)])
		row_range.remove(C)

		# Create a union of all allowed values in row positions
		for c in row_range:
			allowed = allowed.union(set(self.allowed[R][c]))

		return allowed

	# For a position given by R and C, this method checks all the positions
	# of the same column 
	def allowed_in_other_positions_col(self, R, C):
		 # Initialize the set of allowed numbers in other positions of the same
		 # column
		allowed = set()
		row_range = set([x for x in range(0,9)])
		row_range.remove(R)

		# Create a union of all allowed values in row positions
		for r in row_range:
			allowed = allowed.union(set(self.allowed[r][C]))

		return allowed

	# For a position given by R and C, this method checks all the positions
	# of the same 3x3 square
	def allowed_in_other_positions_square(self, R, C):
		# Initialize the set of allowed numbers in other positions of the same
		# column
		allowed = set()
		r_start_index = int(3*math.floor(R/3))
		c_start_index = int(3*math.floor(C/3))

		for r in range(r_start_index,r_start_index+3):
			for c in range(c_start_index,c_start_index+3):
				if (r==R) and (c==C): 
					# Do not include the position in question
					pass
				else:
					# Add the numbers allowed in the other positions of the 
					# same square 
					allowed = allowed.union(set(self.allowed[r][c]))

		return allowed

	# This method does a simple autocomplete of the sudoku grid
	def update_sudoku(self):
		update = False
		for r in range(0,9):
			for c in range(0,9):
				if (len(self.allowed[r][c])==1) and (self.puzzle[r][c]==0):
					# the empty positions where there is only one allowed item
					self.sudoku_write(r, c, self.allowed[r][c][0])
					update = True
				if len(self.allowed[r][c])!=1:
					# Set of allowed numbers in the current position
					current_allowed = set(self.allowed[r][c])
					
					# Sets of numbers allowed in other positions of the same column 
					allowed_in_column = self.allowed_in_other_positions_col(r,c)
					# Sets of numbers allowed in other positions of the same row
					allowed_in_row = self.allowed_in_other_positions_row(r,c)
					# Sets of numbers allowed in other positions of the same row
					allowed_in_square = self.allowed_in_other_positions_square(r,c)

					# TODO: change the locations for unique outside the loop such that it 
					# runs more efficienty
					# Find the numbers uniquely allowed by a single position in a 3x3 square
					unique_square = current_allowed.difference(allowed_in_square)
					# Find the numbers uniquely allowed by a single position in a row 
					unique_row = current_allowed.difference(allowed_in_row)
					# Find the numbers uniquely allowed by a single position in a column
					unique_col = current_allowed.difference(allowed_in_column)
			
					# This is guaranteed to be the empty set or a set containing 1 item
					unique = unique_row.union(unique_col, unique_square)

					# If there is only one element, then we have found the the uniquely
					# allowed number in the position (r,c). We thus write it
					if len(unique)==1:
						(unique_allowed_number,) = unique
						self.sudoku_write(r,c, unique_allowed_number)
						update = True
		if update==True:
			self.update_allowed()
			self.update_sudoku()

	# In case the problem cannot be solved still, we suggest a number 
	# of values which can be tried at certain positions. 
	def get_suggestions(self):
		min_length = 1000
		possibilities = None
		c_number = 1000
		r_number = 1000

		for r in range(0,9):
			for c in range(0,9):
				if len(self.allowed[r][c])==1: 
					pass
				else: 
					if (len(self.allowed[r][c])<min_length):
						min_length = len(self.allowed[r][c])
						possibilities = self.allowed[r][c]
						c_number = c
						r_number = r
				# This is an early stopping condition 
				if min_length ==2: 
					break
			# This is an early stopping condition
			if min_length == 2:
				break

		return r_number, c_number, possibilities

#################### End of Sudoku Class ###########################


############## Helper functions ###################################
# This method recursively calls itself to explore a tree of 
# possibilities in a depth first manner
def recursive_solver(sudoku_obj,r,c,possib): 
	# Iterate over all possible values at position (r,c)
	for p in possib: 
		# Copy the grid, preserving the original, to test if the 
		# current possibiity works
		sudoku = copy.deepcopy(sudoku_obj)
		# Write to the sudoku grid the solution we want to test
		sudoku.sudoku_write(r,c,p)
		# Update the grid so that easy autofills can be made
		sudoku.update_allowed()
		sudoku.update_sudoku()

		# Now check if the sudoku does not contain faults so far
		if sudoku.is_false() :
			# Backtrack
			# print("Backtrack")
			pass
		# If no faults are found yet
		else: 
			# In case the entire sudoku is solved
			if sudoku.is_solved():
				print("Success !")
				sudoku.sudoku_print()
				sys.exit()
			# In case the sudoku is not yet fully solved
			else: 
				# Obtain the set of new possibilities to test on the 
				# child node of the current one
				R, C, possibilities = sudoku.get_suggestions()
				# Recursively call this function to carry out the same
				# task on the child node
				recursive_solver(sudoku,R, C, possibilities)
				
############## End Helper functions ###############################

################## Input Conditioning ############################## 

# This string represents the sudoku puzzle. 0 means empty
init_grid = '040600005902005400080200900000060090300000007010030000009002030005800201100006050'
# Convert from single string to an array of strings
init_grid = list(init_grid)
# Convert from array of strings into array of ints 
init_grid = map(lambda x: int(x), init_grid)
# Transform into np array object
init_grid = np.array(init_grid)
# Split into rows of 9 ints
init_grid = np.split(init_grid, 9)
# Convert the whole into 2D np array
init_grid = np.array([i for i in init_grid])

################# End Input Conditioning ##########################

################ Main Execution ###################################
# Initialize sudoku puzzle
sudo = Sudoku(init_grid)
# Check if the initial entry contains obvious errors or not
if sudo.is_false():
	print("The entry is incorrect")
	sys.exit()

if sudo.is_solved():
	print("Success !")
	sudo.sudoku_print()
else: 
	# If the puzzle is not solved, call the recursive solver
	R, C, possibilities = sudo.get_suggestions()
	recursive_solver(sudo, R, C, possibilities)

# If the code reaches this point, then no solution exists 
print("No solution could be found")

############## End main execution #################################
