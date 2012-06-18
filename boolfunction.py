# Minterm is a array of strings which hold the literals. Negated literals have to with '~'. If a minterm gets true it will be [1], if it gets false it will be [0]
class Minterm(object):

	def __init__(self, index=-1):
		self.__index = index # index is optional, maybe not needed
		self.__content = []

	def __repr__(self):
		return repr(self.__content)

	def __eq__(self, minterm):
		if (repr(self.__content) == repr(minterm)):
			return True
		else:
			return False

	def index(self):
		return self.__index

	def content(self):
		return self.__content

	# expects 0 or 1 to create [0] or [1]
	def createBoolTerm(self, boolv):
		self.__content = [boolv]
		return
		
	def addLiteral(self, literal):
		# avoid to add more instances of the same literal
		if(literal[0] == '~'):
			notliteral = literal[1:] 
		else:
			notliteral = '~' + literal
		if(not(literal in self.__content or notliteral in self.__content)):
			self.__content.append(literal)
		else:
			print "Literal " + literal + " is already part of the minterm."
		return

	# expects a not negated literal
	def setLiteralFalse(self, literal):
		notliteral = '~' + literal
		if(literal in self.__content):
			self.__content = [0]
		elif((notliteral in self.__content) and (len(self.__content) > 1)):
			self.__content.remove(notliteral)
		elif((notliteral in self.__content) and (len(self.__content) == 1)):
			self.__content = [1]
		return	

	# expects a not negated literal
	def setLiteralTrue(self, literal):
		notliteral = '~' + literal
		if((literal in self.__content) and (len(self.__content) > 1)):
			self.__content.remove(literal)
		elif((literal in self.__content) and (len(self.__content) == 1)):
			self.__content = [1]
		elif(notliteral in self.__content):
			self.__content = [0]
		return

	
# Maxterm is a array of minterms
class Maxterm(object):

	def __init__(self, index=-1):
		self.__index 	= index # index is optional, maybe not needed
		self.__content 	= []
		self.__iterindex= 0 

	def __repr__(self):
		return repr(self.__content)

	def __len__(self):
		return len(self.__content)
	
	# make Maxterm iterable
	def __iter__(self):
		return self
	
	def next(self):
		if self.__iterindex == len(self):
			self.__iterindex = 0
			raise StopIteration
		self.__iterindex += 1
		return self.__content[self.__iterindex-1]

	def index(self):
		return self.__index

	def removeAll(self, minterm):
		newMaxterm = [] 
		for x in self:
			if(repr(x) != repr(minterm)):
				newMaxterm.append(x)
		self.__content = newMaxterm	
		return
	
	def isEmpty(self):
		if(repr(self) == '[]'):
			return True
		else:
			return False

	def addMinterm(self, minterm):
		if(not(minterm in self.__content)):
			self.__content.append(minterm)
		return

	# expects a not negated literal
	def setLiteralFalse(self, literal):
		if(not(self.__content == [0] or self.__content == [1])): 	#  do not set literal if maxterm=0 or =1
			for minterm in self.__content:
				minterm.setLiteralFalse(literal)

		## UPDATE
		# if maxterm contains a minterm=[1] it will be also [1]
		if([1] in self.__content):
			self.__content = [1]
			return
		# remove all occurences of minterms=[0] 
		self.removeAll([0])
		if (self.isEmpty()):
			self.__content = [0]
		return

	# expects a not negated literal
	def setLiteralTrue(self, literal):
		if(not(self.__content == [0] or self.__content == [1])):	 # do not set literal if maxterm=0 or =1
			for minterm in self.__content:
				minterm.setLiteralTrue(literal)

		## UPDATE
		# if maxterm contains a minterm=[1] it will be also [1]
		if([1] in self.__content):
			self.__content = [1]
			return
		# remove all occurences of minterms=[0] 
		self.removeAll([0])
		if (self.isEmpty()):
			self.__content = [0]
		return 

def buildMinterm(stringInput):
	newMinterm 		= Minterm()
	variableCounter = 1
	
	for literal in stringInput:
		if literal == '1':
			newMinterm.addLiteral('x' + str(variableCounter))
		elif literal == '0':
			newMinterm.addLiteral('~x' + str(variableCounter))
		# elif literal == '-': do nothing
		variableCounter += 1

	return newMinterm
			
		
