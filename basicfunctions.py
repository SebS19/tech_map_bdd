# function to flatten an irregular tuple
def flatten_tuple(utuple):
	result = []
	for x in utuple:
		if isinstance(x, tuple):
			result += flatten_tuple(x)
		else:
			result.append(x)		
	return result
    
