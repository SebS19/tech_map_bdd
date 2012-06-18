import commands
import copy
from basicfunctions import flatten_tuple

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
		datei.write("digraph G { \n" + "rotate=90\n" "center=1\n" + self.dotPrint() + "\n}")
		datei.close()
		commands.getstatusoutput('dot -Tps graph.dot -o graph.ps')
		commands.getstatusoutput('ps2pdf graph.ps')
		return #"digraph G { \n" + self.dotPrint() + "\n}"




def adjust(stringInput, rootNode):
	currentNode 	= rootNode
	currentDepth 	= 0
	# getting the last variable node
	for literal in stringInput[:-1]:
		currentDepth += 1	
		if literal == '1':
			currentNode = currentNode.trueNode
		elif literal == '0':
			currentNode = currentNode.falseNode
		elif literal == '-':
			adjust(stringInput[currentDepth:], currentNode.trueNode)
			adjust(stringInput[currentDepth:], currentNode.falseNode)
			return

	# setting the leaves
	if stringInput[-1] == '1' or stringInput[-1] == '-':	
		currentNode.setTrueNode(Node.T)
	if stringInput[-1] == '0' or stringInput[-1] == '-':	
		currentNode.setFalseNode(Node.T)

def createTree(n):
	
	subTree = Node('x1', Node.F, Node.F)
	k=2

	while n > 1:
		a = copy.deepcopy(subTree)
		b = copy.deepcopy(subTree)
		tree 	= Node('x%i' %k, a, b)
		subTree = tree
		k+=1
		n-=1

	return tree

def bddToBlif(rootNode):
	stringOutput = ''
	arrayOnSetAll = flatten_tuple(getAllOnPaths(getHeight(rootNode), rootNode, ''))
	arrayOnSetAll = filter (lambda x: x!=None, arrayOnSetAll)			# remove all None entries	

	# converting array to blif string format
	for minterm in arrayOnSetAll[:-1]:
		stringOutput += minterm + " 1" + '\n'
	stringOutput += arrayOnSetAll[-1] + " 1"					# last line without newline at the end
	return stringOutput 
	
# auxiliary function to descend recursive through the tree and save all ways of the on set
def getAllOnPaths(treeheight, rootNode, way):
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


def doShannon(maxterm, level, height):


	maxTermT = copy.deepcopy(maxterm)
	maxTermF = copy.deepcopy(maxterm)

	# shannon expansion
	maxTermT.setLiteralTrue( 'x' + str(level))
	maxTermF.setLiteralFalse('x' + str(level))

	#print "--- aktueller maxTerm ---- \n"
	#print maxterm

	#print "\n maxtermT \n"
	#print maxTermT


	#print "\n maxtermF \n"
	#print maxTermF

	#print "\n ----------------------"

	if level==height:
		
		if maxTermT == [0] and maxTermF == [0]:
			return Node('x'+str(level), Node.F, Node.F)
		elif maxTermT == [0] and maxTermF == [1]:
			return Node('x'+str(level), Node.F, Node.T)
		elif maxTermT == [1] and maxTermF == [0]:
			return Node('x'+str(level), Node.T, Node.F)
		elif maxTermT == [1] and maxTermF == [1]:
			return Node('x'+str(level), Node.T, Node.T)
		else:
			raise SyntaxError("irgendwas stimmt nicht")
	
	else:
		
		if maxTermF == maxTermT:
			temp = doShannon(maxTermF,level+1, height)
			return Node('x' + str(level), temp, temp)
		else:
			return Node('x' + str(level), doShannon(maxTermT,level+1,height), doShannon(maxTermF, level+1,height) )




'''
	if level == 0:
		if maxterm == [1]:
			return Node.T
		if maxterm == [0]:
			return Node.F
		elif:
			raise SyntaxError("wrong level specified, looser")

	if maxterm == [1] or maxterm == [0]:
		self.__trueNode  = makeChildNode(maxterm, level-1)
		self.__falseNode = self.__trueNode

	else:



		self.__trueNode  = Node(	'x' + str(level),\
									makeChildNode( maxTermT, level-1),\
									makeChildNode( maxTermF, level-1) )
		self.__falseNode =  
'''