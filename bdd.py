import commands
import basicfunctions 	as bas
import boolfunction		as bf
import math
from copy import copy
from copy import deepcopy
from operator import itemgetter

class DecompositionError(Exception):
	def __init__(self, value):
		self.__value__ = value
	
	def __str__(self):
		return self.__value__

class Node(object):

	# true / false classes for the end of the tree
	counter = 0

	class __TrueNode:
		def __repr__(self):
			return "True"

	class __FalseNode:
		def __repr__(self):
			return "False"

	T = __TrueNode()
	F = __FalseNode()

	
	###############
	# constructor #
	###############
	
	def __init__(self, variable, trueNode, falseNode):
		self.__variable 	= variable
		self.__trueNode 	= trueNode
		self.__falseNode 	= falseNode
		
		# attribute needed for sifting
		self.__level		= 0
		self.__note			= ""

	

	##########
	# getter #
	##########

	@property
	def trueNode(self):
		return self.__trueNode

	@property		
	def falseNode(self):
		return self.__falseNode

	@property
	def variable(self):
		return self.__variable

	@property 
	def level(self):
		return self.__level

	@property
	def note(self):
		return self.__note


	##########
	# setter #
	##########

	
	def setTrueNode(self,newNode):
		self.__trueNode = newNode

	def setFalseNode(self,newNode):
		self.__falseNode = newNode

	def setLevel(self,newLevel):
		self.__level 	= newLevel

	def setVariable(self,variable):
		self.__variable = variable

	def setNote(self,newNote):
		self.__note = newNote

	#####################
	# function overload #
	#####################


	# defining the textual representation of a node (keep in mind that this is a recursion)
	def __repr__(self):
		return  'Node('+ repr(self.__variable) + ':' + repr(self.__trueNode) + '|' + repr(self.__falseNode) + ')'


	def __eq__(self, otherNode):
		if self.__variable == otherNode.variable:
			if ( self.__trueNode is self.__falseNode and not(otherNode.trueNode is otherNode.falseNode)):
				return False
			elif ( not(self.__trueNode is self.__falseNode) and otherNode.trueNode is otherNode.falseNode):
				return False
			elif type(self.__trueNode) == Node:
				return self.__trueNode == otherNode.trueNode and self.__falseNode == otherNode.falseNode
			else:
				return repr(self.__trueNode) == repr(otherNode.trueNode) and repr(self.__falseNode) == repr(otherNode.falseNode)
		else:
			return False

	
	##########################################
	# some very cool implicit tree functions #
	##########################################

	def makeQRBDD(self):

		compareSet  = [self]
		compareNode = self

		while type(compareNode.trueNode) == Node:

			rootNodes = compareSet[:]

			while len(compareSet)>0:
				
				#print len(compareSet)
				#print compareSet

				compareNode = compareSet[0]
				compareSet.remove(compareNode)

				if (compareNode.trueNode == compareNode.falseNode) and not (compareNode.trueNode is compareNode.falseNode):
					compareNode.setFalseNode(compareNode.trueNode)
					#print "selbst umbiegen II"

				for knoten in compareSet:
					
					if compareNode.trueNode == knoten.trueNode and not (compareNode.trueNode is knoten.trueNode):
						knoten.setTrueNode(compareNode.trueNode)
						#print "umbiegen 1"

					if compareNode.trueNode == knoten.falseNode and not (compareNode.trueNode is knoten.falseNode):
						knoten.setFalseNode(compareNode.trueNode)
						#print "umbiegen 2"

					if compareNode.falseNode == knoten.trueNode and not (compareNode.falseNode is knoten.trueNode):
						knoten.setTrueNode(compareNode.falseNode)
						#print "umbiegen 3"

					if compareNode.falseNode == knoten.falseNode and not (compareNode.falseNode is knoten.falseNode):
						knoten.setFalseNode(compareNode.falseNode)
						#print "umbiegen 4" 

			#creating compare set
			compareSet=[]
			for knoten in rootNodes:
				
				if not knoten.falseNode in compareSet:
					compareSet.append(knoten.falseNode)
				
				if not knoten.trueNode in compareSet:
					compareSet.append(knoten.trueNode)
				

	def dotPrint(self):
		
		nodeList= [self]
		outputString = ""

		while len(nodeList) > 0:
			
			nextNodeList = []

			for knoten in nodeList:
				
				outputString += str(id(knoten))  + ' [label="%s (%s) [%s]"]' %(knoten.variable,knoten.level,knoten.note) + "\n"
				outputString += str(id(knoten))  + "->" + str(id(knoten.falseNode)) + "[style=dotted] \n"
				outputString += str(id(knoten))  + "->" + str(id(knoten.trueNode))  + "\n"

				if type(knoten.falseNode) == Node:
					nextNodeList.append(knoten.falseNode)
					nextNodeList.append(knoten.trueNode)

			nodeList = set(nextNodeList[:])


		outputString += str(id(Node.T)) + ' [label="True"] \n'
		outputString += str(id(Node.F)) + ' [label="False"] \n'

		return outputString

	
	def dotPrint2(self, name="graph"):
		datei = open(name+".dot","w")
		datei.write("digraph G { \n" + "graph [fontsize=24];\n" + "edge  [fontsize=24];\n" + "node  [fontsize=24];\n" + "ranksep = 1.5;\n" + "nodesep = .25;\n" + 'edge [style="setlinewidth(3)"];\n' +  'size="2,4";\n' + "rotate=90;\n" "center=1;\n" + self.dotPrint() + "\n}")
		#	datei.write("digraph G { \n" + "graph [fontsize=24];\n" + self.dotPrint() + "\n}")
		datei.close()
		commands.getstatusoutput('dot -Tps ' + name + '.dot -o '+ name + '.ps')
		commands.getstatusoutput('ps2pdf ' + name + '.ps')
		return #"digraph G { \n" + self.dotPrint() + "\n}"


	def doNaiveDecomp(self, k, variableOrder, setOfLdMy, listOfCuts=[]):
		# returns a nested array which symbolizes the structure of the LUT chain, for example for k=3: [3,2, [1,[4,5,6],[4,5,6]] ] -> x2 and x3 are in the free set, remaining variables are in the bound set
		
		# variableOrder is an array with the form of [9, 3, 12, ...] as example (cardinality is number of inputs)
		# setOfLdMy is an arary with the form of [1, 1, 2, 8, ..., 4, 2] as example (cardinality is number of inputs-1), elements with the form of 2**i
		# listOfCuts returns a list of integers which symbolize the cut heights of the tree
		if(0 in setOfLdMy):
			print "\nExit status: setOfLdMy must not contain 0 as element!"
			exit(1)
		if(k > 8):
			print "\nExit Status: k > 8 not implemented"
			exit(1)

		nestedLUTstruct=[]
		treeHeight = len(variableOrder)
		cutPosition = len(setOfLdMy)
		
		# exit condition
		if(cutPosition < k):
			variableOrder.reverse()		# just to keep the order of the LUT structure consistently
			nestedLUTstruct=variableOrder
			return nestedLUTstruct,listOfCuts
	
		# add variables to free set until all ports are assigned
		whileLoopEntered = False						# boolean variable to check if it is actually possible to assign further ports
		while   ( k >= treeHeight - cutPosition + setOfLdMy[cutPosition-1])  :
			nestedLUTstruct.append(variableOrder[cutPosition])	
			cutPosition -= 1
			whileLoopEntered = True

		# Check if tree is too wide for the given k
		if(not(whileLoopEntered)):
			if(k < 8):
				print "\nExit status: Value of k=%s is to low for the given PLA. Please increase!" %k
			else:
				print "\nYour problem is not feasible for k<=8."
		        exit(1)


		# restore cutPosition
		cutPosition += 1
		
		listOfCuts.append(cutPosition-1)

		# recursive cutting depending on ld(my)
		currentLdMy = setOfLdMy[cutPosition-1]

		if(currentLdMy == 1):
			recursiveLUTstruct, cutHeigths = self.doNaiveDecomp(k, variableOrder[:cutPosition], setOfLdMy[:cutPosition-1], listOfCuts) 
			nestedLUTstruct.append(recursiveLUTstruct)
			return nestedLUTstruct, cutHeigths
		elif(currentLdMy == 2):
			recursiveLUTstruct, cutHeigths = self.doNaiveDecomp(k, variableOrder[:cutPosition], setOfLdMy[:cutPosition-1], listOfCuts)
			nestedLUTstruct.extend([recursiveLUTstruct, recursiveLUTstruct])
			return nestedLUTstruct, cutHeigths
		elif(currentLdMy == 3):
			recursiveLUTstruct, cutHeigths = self.doNaiveDecomp(k, variableOrder[:cutPosition], setOfLdMy[:cutPosition-1], listOfCuts)
			nestedLUTstruct.extend([recursiveLUTstruct, recursiveLUTstruct, recursiveLUTstruct])
			return nestedLUTstruct, cutHeigths
		elif(currentLdMy == 4):
			recursiveLUTstruct, cutHeigths = self.doNaiveDecomp(k, variableOrder[:cutPosition], setOfLdMy[:cutPosition-1], listOfCuts)
			nestedLUTstruct.extend([recursiveLUTstruct, recursiveLUTstruct, recursiveLUTstruct, recursiveLUTstruct])
			return nestedLUTstruct, cutHeigths
		elif(currentLdMy == 5):
			recursiveLUTstruct, cutHeigths = self.doNaiveDecomp(k, variableOrder[:cutPosition], setOfLdMy[:cutPosition-1], listOfCuts)
			nestedLUTstruct.extend([recursiveLUTstruct, recursiveLUTstruct, recursiveLUTstruct, recursiveLUTstruct, recursiveLUTstruct])
			return nestedLUTstruct, cutHeigths
		elif(currentLdMy == 6):
			recursiveLUTstruct, cutHeigths = self.doNaiveDecomp(k, variableOrder[:cutPosition], setOfLdMy[:cutPosition-1], listOfCuts)
			nestedLUTstruct.extend([recursiveLUTstruct, recursiveLUTstruct, recursiveLUTstruct, recursiveLUTstruct, recursiveLUTstruct, recursiveLUTstruct])
			return nestedLUTstruct, cutHeigths
		elif(currentLdMy == 7):
			recursiveLUTstruct, cutHeigths = self.doNaiveDecomp(k, variableOrder[:cutPosition], setOfLdMy[:cutPosition-1], listOfCuts)
			nestedLUTstruct.extend([recursiveLUTstruct, recursiveLUTstruct, recursiveLUTstruct, recursiveLUTstruct, recursiveLUTstruct, recursiveLUTstruct, recursiveLUTstruct])
			return nestedLUTstruct, cutHeigths
		elif(currentLdMy == 8):
			recursiveLUTstruct, cutHeigths = self.doNaiveDecomp(k, variableOrder[:cutPosition], setOfLdMy[:cutPosition-1], listOfCuts)
			nestedLUTstruct.extend([recursiveLUTstruct, recursiveLUTstruct, recursiveLUTstruct, recursiveLUTstruct, recursiveLUTstruct, recursiveLUTstruct, recursiveLUTstruct, recursiveLUTstruct])
			return nestedLUTstruct, cutHeigths
		else:
			print "k has to be 0<k<9."
			exit(1)

def encodeCutNodes(rootNode, cutPositions):
	ultimativeArray = []
	
	for cutPos in cutPositions:
		cutHeightArray = []
		
		allCutNodes = getArrayOfLvlNodes(rootNode,cutPos+2)
		#update attribute 'note' with binary annotation
	
		numOfBits = int( math.ceil(math.log(len(allCutNodes),2)) )
		counter   = int('100000000',2); 				# small hack for a binary counter ;)

		for knoten in allCutNodes:
			binEncoding = bin(counter)[-numOfBits:]
			knoten.setNote(binEncoding)
			cutHeightArray.append([binEncoding,knoten])
			counter += 1

		ultimativeArray.append(cutHeightArray)
	
	return ultimativeArray

def getBLIF(ultArr):

	############# INITIAL STEP ###############
	currCutLvl = ultArr[0]
	numSuppFuncs = len(currCutLvl[0][0])
	usedSuppFuncs = numSuppFuncs
	variablesBelow = getVariableOrder(currCutLvl[0][1], [])

	bout = ".names"
	for i in range(usedSuppFuncs):
		bout += " h" + str(i+1)
	for j in variablesBelow:
		bout += " x" + str(j)
	bout += " y"
	
	for eachCutNode in currCutLvl:
		allOnPaths = getOnPaths(eachCutNode[1])
		for eachWay in allOnPaths:
			bout += "\n" + eachCutNode[0] + eachWay + ' 1'

	return bout
	#for currCut in range(len(ultArr)):
		

def cutTreeAtHeight(rootNode, cutHeight):

	print "--------CUTTING AT LVL %s----------" %cutHeight
	print rootNode

	# find all nodes on the level before and after cutHeight

	checkNode     = rootNode
	afterCutNodes = [rootNode]
	level 		  = 0

	while level < cutHeight+1:

		newRootNodes = []

		for knoten in afterCutNodes:

			newRootNodes.append(knoten.trueNode)
			newRootNodes.append(knoten.falseNode)

		checkNode     = newRootNodes[0]

		beforeCutNodes = afterCutNodes
		afterCutNodes  = set(newRootNodes[:])
		
		level 	  += 1

		try:
			t = checkNode.trueNode
		except Exception, e:
			print "unzulaessiger Knotenzugriff, Cut Height (%s) konnte nicht erreicht werden." %(cutHeight) ,e



	#update attribute 'note' with binary annotation

	numOfBits = int( math.ceil(math.log(len(afterCutNodes),2)) )
	counter   = int('100000000',2); # small hack for a binary counter ;)

	for knoten in afterCutNodes:
		knoten.setNote( bin(counter)[-numOfBits:])
		counter += 1
		#print str(knoten) + "ANNOT " + knoten.note




	# debug

	rootNode.dotPrint2("debug")

	# creating return trees

	returnTrees = []

	for idx in range(numOfBits):
		print idx
		returnTrees.append(deepcopy(rootNode))



	# go to cut level in each return tree and set the correct leaves

	for idx in range(numOfBits):
		#print "---------------------"
		#print tree
		#print "---------------------"
		level = 0
		beforeCutNodes = [returnTrees[idx]]

		while level != cutHeight:

			newRootNodes = []

			for knoten in beforeCutNodes:

				newRootNodes.append(knoten.trueNode)
				newRootNodes.append(knoten.falseNode)

			beforeCutNodes = set(newRootNodes[:])
			level += 1


		for knoten in beforeCutNodes:

			if knoten.falseNode.note[idx] == '0':
				knoten.setFalseNode(Node.F)
			elif knoten.falseNode.note[idx] == '1':
				knoten.setFalseNode(Node.T)
			else:
				print "error while setting the leaves"
				exit(1)

			if knoten.trueNode.note[idx] == '0':
				knoten.setTrueNode(Node.F)
			elif knoten.trueNode.note[idx] == '1':
				knoten.setTrueNode(Node.T)
			else:
				print "error while setting the leaves"
				exit(1)

	print "--------- CUT DONE ----------------"
	return returnTrees,afterCutNodes

def getOnPaths(rootNode):
	# returns an array of all ways for the rootNode which met a True-leave. e.g. ['111','010'] or [], if treeHeight=0 or no on-path is available
	arrayOnSetAll = getAllOnPaths(getHeight(rootNode), rootNode)

	# catch some exceptions here
	if (arrayOnSetAll == '' or arrayOnSetAll == None):
		return []
	elif (type(arrayOnSetAll) == str):
		arrayOnSetAll = [arrayOnSetAll]
	else:
		arrayOnSetAll = bas.flatten_tuple(arrayOnSetAll)			# flatten the tuple structure
	arrayOnSetAll = filter (lambda x: x!=None, arrayOnSetAll)			# remove all None entries	

	return arrayOnSetAll

# function can be deleted later on, overwritten by getOnPaths
'''
def bddToBlif(rootNode, base):
	#base gives the my, which symbolizes the number of ones at the beginning of each line
	stringOutput = ''
	arrayOnSetAll = getAllOnPaths(getHeight(rootNode), rootNode)

	# catch some exceptions here
	if (type(arrayOnSetAll) == str):
		arrayOnSetAll = [arrayOnSetAll]
	elif (arrayOnSetAll == None):
		if(base == 2):
			return '1 1'
		else:
			return ' 1'
	else:
		arrayOnSetAll = bas.flatten_tuple(arrayOnSetAll)
	arrayOnSetAll = filter (lambda x: x!=None, arrayOnSetAll)			# remove all None entries	

	# converting array to blif string format
	for minterm in arrayOnSetAll[:-1]:
		if (base == 2):
			stringOutput += "1" + minterm + " 1" + '\n'
		else:
			stringOutput += minterm + " 1" + '\n'
	if (base == 2):
		stringOutput += "1" + arrayOnSetAll[-1] + " 1"					# last line without newline at the end
	else:
		stringOutput += arrayOnSetAll[-1] + " 1"					# last line without newline at the end
	return stringOutput 
'''
# auxiliary function to descend recursive through the tree and save all ways of the on set, necessary for function getOnPaths
def getAllOnPaths(treeheight, rootNode, way=''):
	# termination condition:
	if treeheight == 0 and repr(rootNode)=='True':
		return way
	elif treeheight == 0:
		return
	# recursive descent:
	if (rootNode.trueNode is rootNode.falseNode):
		return getAllOnPaths(treeheight-1, rootNode.trueNode, way+'-')
	else:
		return getAllOnPaths(treeheight-1, rootNode.trueNode, way+'1'), getAllOnPaths(treeheight-1, rootNode.falseNode, way+'0')

# auxiliary function to get height of a tree, height of a leave is defined as 0
def getHeight(rootNode):
	if type(rootNode) != Node:		# just in case you call the function with a leave
		return 0
	elif type(rootNode.trueNode) != Node:
		return 1
	else:
		return getHeight(rootNode.trueNode) + 1

# returns the compatibilty My depending on the chosen tree level or with other words the number of the nodes x_i for a chosen i
def getMy(rootNode, level):
	global arrayOfNodes
	my = len(getArrayOfLvlNodes(rootNode, level))
	arrayOfNodes = []
	return my 

arrayOfNodes = []
def getArrayOfLvlNodes(rootNode, level):
	global arrayOfNodes
	tempArray = getArrayOfLvlNodesAUX(rootNode, level)
	arrayOfNodes = []
	return tempArray

# NEVER use this function, just defined for the usage in getArrayOfLvlNodes 
def getArrayOfLvlNodesAUX(rootNode, level):
	global arrayOfNodes
	if(level == 1 and not(rootNode in arrayOfNodes)):
		arrayOfNodes.append(rootNode)	
	else:
		if(type(rootNode.trueNode) == Node):
			getArrayOfLvlNodesAUX(rootNode.trueNode, level-1)
		if(type(rootNode.falseNode) == Node):
			getArrayOfLvlNodesAUX(rootNode.falseNode, level-1)

	return arrayOfNodes

def getVariableOrder(rootNode, orderArray):
	# returns an array of integers, which symbolize the order of the variables of the tree from the top to the bottom
	orderArray.append( int(rootNode.variable[1:]) )
	if(type(rootNode.trueNode) == Node):
		return getVariableOrder(rootNode.trueNode, orderArray)
	else:
		return orderArray

def doShannon(maxterm, level, height, expansionOrder):
	# expansionOrder is a list of integers which symbolize the variable indeces sorted by weight

	# maxTermT = copy.deepcopy(maxterm)
	maxTermT = maxterm
	# maxTermF = copy.deepcopy(maxterm)
	
	### auxiliary function to avoid deepcopy (bottleneck)
	# if maxterm is just [0] or [1] do not call for-loop
	if(maxterm == [0]):
		maxTermF = bf.Maxterm()
		maxTermF.setTrue()
	elif(maxterm == [1]):
		maxTermF = bf.Maxterm()
		maxTermF.setFalse()
	else:
		maxTermF = bf.Maxterm()
		for terms in maxterm:
			minterm_temp = bf.Minterm()
			minterm_content_temp = terms.content()[:]
			minterm_temp.setContent(minterm_content_temp)
			maxTermF.addMinterm(minterm_temp)

	# shannon expansion
	maxTermT.setLiteralTrue( 'x' + str(expansionOrder[level-1]))
	maxTermF.setLiteralFalse('x' + str(expansionOrder[level-1]))

	#print "--- aktueller maxTerm ---- \n"
	#print maxterm

	#print "\n maxtermT \n"
	#print maxTermT


	#print "\n maxtermF \n"
	#print maxTermF

	#print "\n ----------------------"

	if level==height:
		
		if maxTermT == [0] and maxTermF == [0]:
			return Node('x'+str(expansionOrder[level-1]), Node.F, Node.F)
		elif maxTermT == [0] and maxTermF == [1]:
			return Node('x'+str(expansionOrder[level-1]), Node.F, Node.T)
		elif maxTermT == [1] and maxTermF == [0]:
			return Node('x'+str(expansionOrder[level-1]), Node.T, Node.F)
		elif maxTermT == [1] and maxTermF == [1]:
			return Node('x'+str(expansionOrder[level-1]), Node.T, Node.T)
		else:
			raise SyntaxError("irgendwas stimmt nicht")
	
	else:
		
		if maxTermF == maxTermT:
			temp = doShannon(maxTermF,level+1, height, expansionOrder)
			return Node('x' + str(expansionOrder[level-1]), temp, temp)
		else:
			return Node('x' + str(expansionOrder[level-1]), doShannon(maxTermT,level+1,height,expansionOrder), doShannon(maxTermF, level+1,height,expansionOrder) )

def countNodes(rootNode):

	counter   = 0

	countSet  = [rootNode]
	checkNode = rootNode

	while type(checkNode.trueNode) == Node:

		counter 	+= len(set(countSet)) 
		checkNode 	= countSet[0]
		rootNodes	= countSet[:]

		countSet	= []

		for knoten in rootNodes:
			
			countSet.append(knoten.falseNode)
			countSet.append(knoten.trueNode)
	return counter

def updateLevel(rootNode):

	level 		 = 0
	checkNode    = rootNode
	rootNodes    = [rootNode]


	while type(checkNode) == Node:

		newRootNodes = []

		for knoten in rootNodes:
			
			knoten.setLevel(level)
			newRootNodes.append(knoten.trueNode)
			newRootNodes.append(knoten.falseNode)

		checkNode  = newRootNodes[0]
		rootNodes  = set(newRootNodes[:])
		level 	  += 1

def moveDown(variable, rootNode):

	updateLevel(rootNode)

	# searching for the variable in tree and collect all nodes of this variable
	checkNode = rootNode
	nodeSet   = [rootNode]

	while (checkNode.variable != variable):

		newNodes = []

		for knoten in nodeSet:

			newNodes.append(knoten.falseNode)
			newNodes.append(knoten.trueNode)

		checkNode = newNodes[0]
		nodeSet   = set(newNodes[:])

		try:
			t = checkNode.trueNode
		except Exception, e:
			print "unzulaessiger Knotenzugriff, Variable %s konnte nicht gefunden werden." %(variable) ,e 


	# check if move is possible and move
	if type(checkNode.trueNode) != Node:
		
		print "couldnt move down, variable at bottom!"
		return False

	else:
		
		print "moving down %s" %variable

		# bend the pointer :)
		for knoten in nodeSet:

			# shallow copy to prevent interference when node has more than one predecessor
			knoten.setTrueNode(copy(knoten.trueNode))
			knoten.setFalseNode(copy(knoten.falseNode))

			trueFalse = knoten.trueNode.falseNode
			falseTrue = knoten.falseNode.trueNode

			knoten.trueNode.setFalseNode(falseTrue)
			knoten.falseNode.setTrueNode(trueFalse)

			var1 = knoten.variable
			var2 = knoten.trueNode.variable

			knoten.setVariable(var2)
			knoten.trueNode.setVariable(var1)
			knoten.falseNode.setVariable(var1)

		return True

def moveUp(variable, rootNode):

	# searching for the variable above the variable to move up
	checkNode = rootNode

	if checkNode.variable == variable:
	
		print "couldnt move up - variable on top"
		return False
	
	else:


		try:
			t = checkNode.trueNode
		except Exception, e:
			print "unzulaessiger Knotenzugriff, Variable %s konnte nicht gefunden werden." %(variable) ,e 

		while(checkNode.variable != variable):

			prevNode  = checkNode
			checkNode = checkNode.trueNode


		print "moving up %s by moving down %s" %(variable, prevNode.variable)
		
		return moveDown(prevNode.variable,rootNode)

def doSifting(rootNode):
	
	updateLevel(rootNode)
	movedVariables = set([])

	while len(movedVariables) < getHeight(rootNode):

		rootNode.makeQRBDD()
		

		# selecting highest variable that is not moved yet
		var 	  = rootNode.variable
		tempNode  = rootNode

		while var in movedVariables:
			tempNode = tempNode.trueNode
			var 	 = tempNode.variable



		# shift down to end / bottom of the tree and notice the number of nodes at every position
		book = dict({})
		book[tempNode.level] = countNodes(rootNode)

		while(moveDown(var,rootNode)):

			tempNode = tempNode.trueNode
			updateLevel(rootNode)
			rootNode.makeQRBDD()		# big performance issue
			
			book[tempNode.level] = countNodes(rootNode)
			print tempNode.level

		# shift up to level with smallest number of nodes
		print book
		mini  = min(book.iteritems(), key=itemgetter(1))[0]
		level = getHeight(rootNode)-1

		print "starting level: %s" %level
		print "minimum at level %i" %mini

		while(level != mini):
			level -= 1
			moveUp(var,rootNode)

		movedVariables.add(var)

def transformToLUT(cutList, rootNode):

	print "---------TRANSFORM TO LUT----------------"
	#datei = open(output +".blif","w")
	outString = ""

	treesToCut = [rootNode]
	cutResults = []

	helpFuncCounter = 1
	helpSet = ['out']


	for idx_tree in range(len(cutList)):
		print "-----> CUT: %s" %idx_tree

		
		for tree in treesToCut:
			print "---------TREE to CUT at HEIGHT %s -------------------- \n \n" %(cutList[idx_tree])
			print tree
			tree.dotPrint2("treeToCut")
			cutResults.append( cutTreeAtHeight(tree, cutList[idx_tree]) )



		treesToCut = []


		resultCnt = 0
		for result in cutResults:
			#print "------> nodesToBlif: %s" %result[1]

			outString += "\n.names "

			for tree in result[0]:
				outString 		+= "h" + str(helpFuncCounter) + " "
				helpSet.append("h" + str(helpFuncCounter));
				helpFuncCounter += 1

				treesToCut.append(tree)
				lastTree = tree;



			ele = result[1].pop()
			result[1].add(ele)

			for var in getVariableOrder(ele,[]):
				outString += "x" + str(var) + " " + helpSet.pop(0)

			outString = outString + "\n" + nodesToBlif(result[1]);

		cutResults = []


	print "output: \n"
	
	for funcs in helpSet:

		outString += "\n.names "
		for var in getVariableOrder(lastTree,[]):
			outString +=  "x" + str(var) + " "

		outString += str(funcs) + "\n" + nodesToBlif([lastTree])






	print outString



def nodesToBlif(listOfNodes):
	
	outputString = ""

	for knoten in listOfNodes:
		#print "\n knoten to blif \n"
		#print knoten
		onPaths = getOnPaths(knoten)
		
		for way in onPaths:
			outputString += knoten.note + way + " 1" + "\n"


	#print outputString
	return outputString

