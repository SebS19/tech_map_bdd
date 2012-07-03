import commands
import basicfunctions as bas
import boolfunction as bf
import math

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

	# constructor 

	def __init__(self, variable, trueNode, falseNode):
		self.__variable 	= variable
		self.__trueNode 	= trueNode
		self.__falseNode 	= falseNode


	# getter (without the need of "()") for private variables

	@property
	def trueNode(self):
		return self.__trueNode

	@property		
	def falseNode(self):
		return self.__falseNode

	@property
	def variable(self):
		return self.__variable

	# defining the textual representation of a node (keep in mind that this is a recursion)
	def __repr__(self):
		return  "Node("+ repr(self.__variable) + ":" + repr(self.__trueNode) + "|" + repr(self.__falseNode) + ")"

	
	def setTrueNode(self,newNode):
		self.__trueNode = newNode

	def setFalseNode(self,newNode):
		self.__falseNode = newNode

	def __eq__(self, otherNode):
		if self.__variable == otherNode.variable:
			if type(self.__trueNode) == Node:
				return self.__trueNode == otherNode.trueNode and self.__falseNode == otherNode.falseNode 
			else:
				return repr(self.__trueNode) == repr(otherNode.trueNode) and repr(self.__falseNode) == repr(otherNode.falseNode)
		else:
			return False



	def makeQRBDD(self):

		compareSet=[self]
		compareNode=self

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
				
				outputString += str(id(knoten))  + ' [label="%s"]' %knoten.variable + "\n"
				outputString += str(id(knoten))  + "->" + str(id(knoten.falseNode)) + "[style=dotted] \n"
				outputString += str(id(knoten))  + "->" + str(id(knoten.trueNode))  + "\n"

				if type(knoten.falseNode) == Node:
					nextNodeList.append(knoten.falseNode)
					nextNodeList.append(knoten.trueNode)

			nodeList = set(nextNodeList[:])


		outputString += str(id(Node.T)) + ' [label="True"] \n'
		outputString += str(id(Node.F)) + ' [label="False"] \n'

		return outputString

	
	def dotPrint2(self):
		datei = open("graph.dot","w")
		datei.write("digraph G { \n" + "graph [fontsize=24];\n" + "edge  [fontsize=24];\n" + "node  [fontsize=24];\n" + "ranksep = 1.5;\n" + "nodesep = .25;\n" + 'edge [style="setlinewidth(3)"];\n' +  'size="5,8";\n' + "rotate=90;\n" "center=1;\n" + self.dotPrint() + "\n}")
	#	datei.write("digraph G { \n" + "graph [fontsize=24];\n" + self.dotPrint() + "\n}")
		datei.close()
		commands.getstatusoutput('dot -Tps graph.dot -o graph.ps')
		commands.getstatusoutput('ps2pdf graph.ps')
		return #"digraph G { \n" + self.dotPrint() + "\n}"



	def doNaiveDecomp(self, k, variableOrder, setOfLdMy):
	# returns a nested array which symbolizes the structure of the LUT chain, for example for k=3: [3,2, [1,[4,5,6],[4,5,6]] ] -> x2 and x3 are in the free set, remaining variables are in the bound set
		
		# variableOrder is an array with the form of [9, 3, 12, ...] as example (cardinality is number of inputs)
		# setOfLdMy is an arary with the form of [1, 1, 2, 8, ..., 4, 2] as example (cardinality is number of inputs-1), elements with the form of 2**i
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
			return nestedLUTstruct
	
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

		# recursive cutting depending on ld(my)
		currentLdMy = setOfLdMy[cutPosition-1]

		if(currentLdMy == 1):
			recursiveLUTstruct = self.doNaiveDecomp(k, variableOrder[:cutPosition], setOfLdMy[:cutPosition-1]) 
			nestedLUTstruct.append(recursiveLUTstruct)
			return nestedLUTstruct
		elif(currentLdMy == 2):
			recursiveLUTstruct = self.doNaiveDecomp(k, variableOrder[:cutPosition], setOfLdMy[:cutPosition-1]) 
			nestedLUTstruct.extend([recursiveLUTstruct, recursiveLUTstruct])
			return nestedLUTstruct
		elif(currentLdMy == 3):
			recursiveLUTstruct = self.doNaiveDecomp(k, variableOrder[:cutPosition], setOfLdMy[:cutPosition-1]) 
			nestedLUTstruct.extend([recursiveLUTstruct, recursiveLUTstruct, recursiveLUTstruct])
			return nestedLUTstruct
		elif(currentLdMy == 4):
			recursiveLUTstruct = self.doNaiveDecomp(k, variableOrder[:cutPosition], setOfLdMy[:cutPosition-1]) 
			nestedLUTstruct.extend([recursiveLUTstruct, recursiveLUTstruct, recursiveLUTstruct, recursiveLUTstruct])
			return nestedLUTstruct
		elif(currentLdMy == 5):
			recursiveLUTstruct = self.doNaiveDecomp(k, variableOrder[:cutPosition], setOfLdMy[:cutPosition-1]) 
			nestedLUTstruct.extend([recursiveLUTstruct, recursiveLUTstruct, recursiveLUTstruct, recursiveLUTstruct, recursiveLUTstruct])
			return nestedLUTstruct
		elif(currentLdMy == 6):
			recursiveLUTstruct = self.doNaiveDecomp(k, variableOrder[:cutPosition], setOfLdMy[:cutPosition-1]) 
			nestedLUTstruct.extend([recursiveLUTstruct, recursiveLUTstruct, recursiveLUTstruct, recursiveLUTstruct, recursiveLUTstruct, recursiveLUTstruct])
			return nestedLUTstruct
		elif(currentLdMy == 7):
			recursiveLUTstruct = self.doNaiveDecomp(k, variableOrder[:cutPosition], setOfLdMy[:cutPosition-1]) 
			nestedLUTstruct.extend([recursiveLUTstruct, recursiveLUTstruct, recursiveLUTstruct, recursiveLUTstruct, recursiveLUTstruct, recursiveLUTstruct, recursiveLUTstruct])
			return nestedLUTstruct
		elif(currentLdMy == 8):
			recursiveLUTstruct = self.doNaiveDecomp(k, variableOrder[:cutPosition], setOfLdMy[:cutPosition-1]) 
			nestedLUTstruct.extend([recursiveLUTstruct, recursiveLUTstruct, recursiveLUTstruct, recursiveLUTstruct, recursiveLUTstruct, recursiveLUTstruct, recursiveLUTstruct, recursiveLUTstruct])
			return nestedLUTstruct
		else:
			print "k has to be 0<k<9."
			exit(1)

		
	def cutTreeAtHeight(self, cutHeight, lvlNodes):
		if(cutHeight < 1):
			print "\nExit Status: wrong cut height for a certain subtree declared"
		if(cutHeight == 1):
				if(lvlNodes.index(self.trueNode) == 0):
					self.setTrueNode(Node.T)
				if(lvlNodes.index(self.trueNode) == 1):
					self.setFalseNode(Node.F)
		else:
			self.trueNode.cutTreeAtHeight(cutHeight-1, lvlNodes)
			self.falseNode.cutTreeAtHeight(cutHeight-1, lvlNodes)
				
				

def bddToBlif(rootNode):
	stringOutput = ''
	arrayOnSetAll = bas.flatten_tuple(getAllOnPaths(getHeight(rootNode), rootNode))
	arrayOnSetAll = filter (lambda x: x!=None, arrayOnSetAll)			# remove all None entries	

	# converting array to blif string format
	for minterm in arrayOnSetAll[:-1]:
		stringOutput += minterm + " 1" + '\n'
	stringOutput += arrayOnSetAll[-1] + " 1"					# last line without newline at the end
	return stringOutput 
	
# auxiliary function to descend recursive through the tree and save all ways of the on set
def getAllOnPaths(treeheight, rootNode, way=''):
	# termination:
	if treeheight == 0 and repr(rootNode)=='True':
		return way
	elif treeheight == 0:
		return
	# recursive descent:
	if (rootNode.trueNode is rootNode.falseNode):
		return getAllOnPaths(treeheight-1, rootNode.trueNode, way+'-')
	else:
		return getAllOnPaths(treeheight-1, rootNode.trueNode, way+'1'), getAllOnPaths(treeheight-1, rootNode.falseNode, way+'0')

# auxiliary function to get height of a tree
def getHeight(rootNode):
	if type(rootNode.trueNode) != Node:
		return 1
	else:
		return getHeight(rootNode.trueNode) + 1

# returns the combatibilty My depending on the chosen tree level or with other words the number of the nodes x_i for a chosen i
def getMy(rootNode, level):
	global arrayOfNodes
	my = len(getArrayOfLvlNodes(rootNode, level))
	arrayOfNodes = []
	return my 


arrayOfNodes = []

def getArrayOfLvlNodes(rootNode, level):
	global arrayOfNodes

	if(level == 1 and not(rootNode in arrayOfNodes)):
		arrayOfNodes.append(rootNode)	
	else:
		if(type(rootNode.trueNode) == Node):
			getArrayOfLvlNodes(rootNode.trueNode, level-1)
		if(type(rootNode.falseNode) == Node):
			getArrayOfLvlNodes(rootNode.falseNode, level-1)

	return arrayOfNodes


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
