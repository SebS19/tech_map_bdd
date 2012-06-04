import bdd

#bdd.Node(variable, TrueNode, FalseNode)

n1=bdd.Node('x1', bdd.Node.T, bdd.Node.T)
n2=bdd.Node('x1', bdd.Node.F, bdd.Node.F)

n2.setTrueNode(bdd.Node.T)
n2.setFalseNode(bdd.Node.T)

print n2
n3=bdd.Node('x2', n1, n2)

n4=bdd.Node('x3', n3, n3)

n5= bdd.Node('x4', n4, n4)

#print n1
#print n2
#print n4


#print n2.dotPrint2()


gen=bdd.createTree(4)

gen.dotPrint2()