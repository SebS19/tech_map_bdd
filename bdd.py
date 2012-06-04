import commands

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
		return  "Node("+ repr(self.variable) + ":" + repr(self.trueNode) + "|" + repr(self.falseNode) + ")"

	def dotPrint(self):
		
		temp = Node.counter
		Node.counter +=1

		if type(self.__trueNode) == Node:

			return	repr(self.variable)[1:-1] + "_%i" %temp + "->" + repr(self.__trueNode.variable)[1:-1] 	+ "_" 	+ str(Node.counter)  	+ ";\n" 					+ \
					str(self.__trueNode.dotPrint()) + \
					repr(self.variable)[1:-1] + "_%i" %temp + "->" + repr(self.__falseNode.variable)[1:-1] 	+ "_" 	+ str(Node.counter) 	+ "[style=dotted];\n"  	+ \
					str(self.__falseNode.dotPrint())

		else:

			return 	repr(self.variable)[1:-1] + "_%i" %temp +";\n" + \
					repr(self.variable)[1:-1] + "_%i" %temp + "->" + repr(self.__trueNode) + ";\n" + \
					repr(self.variable)[1:-1] + "_%i" %temp + "->" + repr(self.__falseNode) + "[style=dotted];\n" 


	def dotPrint2(self):
		datei = open("graph.dot","w")
		datei.write("digraph G { \n" + self.dotPrint() + "\n}")
		datei.close()
		commands.getstatusoutput('dot -Tps graph.dot -o graph.ps')
		commands.getstatusoutput('ps2pdf graph.ps')
		return "digraph G { \n" + self.dotPrint() + "\n}"


def bddAdjust(stringInput, rootNode):
	currentNode = rootNode
	currentDepth = 0
	# getting the last variable node
	for literal in stringInput[:-1]:
		currentDepth += 1	
		if literal == '1':
			currentNode = currentNode.trueNode
		elif literal == '0':
			currentNode = currentNode.falseNode
		elif literal == '-':
			bddAdjust(currentNode.trueNode, stringInput[currentDepth+1:])
			bddAdjust(currentNode.falseNode, stringInput[currentDepth+1:])
			return
	# setting the leaves
	if stringInput[-1] == '1' or stringInput[-1] == '-':	
		currentNode.setTrueNode(Node.T)
	if stringInput[-1] == '0' or stringInput[-1] == '-':	
		currentNode.setFalseNode(Node.T)
