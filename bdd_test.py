import bdd

#bdd.Node(variable, TrueNode, FalseNode)

n1=bdd.Node('x1', bdd.Node.T, bdd.Node.F)
n2=bdd.Node('x1', bdd.Node.T, bdd.Node.F)

n3=bdd.Node('x1', bdd.Node.T, bdd.Node.F)
n4=bdd.Node('x1', bdd.Node.F, bdd.Node.F)


n5 = bdd.Node('x2', n1,n2)
n6 = bdd.Node('x2', n3,n4)

n7 = bdd.Node('x3', n5, n6)



#print n1
#print n2
#print n4

n7.makeQRBDD()
n7.makeQRBDD()
n7.dotPrint2()


#gen=bdd.createTree(4)

#gen.dotPrint2()