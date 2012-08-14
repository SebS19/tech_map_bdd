# function to flatten an irregular tuple
def flatten_tuple(utuple):
	result = []
	for x in utuple:
		if isinstance(x, tuple):
			result += flatten_tuple(x)
		else:
			result.append(x)		
	return result
    
# function to count the number of lists in a list
def count_lists(ulist):
	counter = 0
	for x in ulist:
		if isinstance(x, list):
			counter += 1
	return counter
