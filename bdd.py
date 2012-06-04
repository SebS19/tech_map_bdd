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
	def getTrueNode(self):
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



def createTree(n):
	
	subTree = Node('x1', Node.F, Node.F)
	k=2

	while n > 1:
		tree 	= Node('x%i' %k, subTree, subTree)
		subTree = tree
		k+=1
		n-=1

	return tree

