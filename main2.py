import boolfunction as bf
import copy
import bdd

import cProfile

#------- file read ---------------------------------------------

#f = open('absp2.pla','r')
#f = open('absp_i28.pla','r')			#i28
#f = open('blif_src/spla.pla','r')		#i16
f = open('blif_src/apex2.pla','r')		#i39
#f = open('blif_src/seq.pla','r')		#i41
#f = open('blif_src/ex1010.pla','r')		#i10
#f = open('blif_src/pdc.pla','r')		#i6
#f = open('blif_src/apex4.pla','r')		#i9
#f = open('blif_src/misex3.pla','r')		#i14
#f = open('blif_src/ex5.pla','r')		#i8


content = f.readlines()
f.close()



#------- splitting header / boundset / freeset  ---------------------

content2 	= []
equations	= []


for line in content:
	content2.append(line.split(' '))

for line in content2:

	if line[0] == '.i':
		inputs = int(line[1][:-1])
	
	if line[0] == '.o':
		outputs = int(line[1][:-1])
	
	if line[0][0] != '.' and len(line) == 2:
		equations.append([ line[0] , line[1][:-1]])


#------- create minterms from blif equations  ---------------------

print "BLIF input On set:"

maxtermArray = []
for i in range(outputs):
	maxtermArray.append(bf.Maxterm(i))					# 0 is index, increment for every output 

for line in equations:

	for output in range(1):			# for every output

		if line[1][output] == '1':			# select the line with an 1 at the end to create the minterm
			print line[0]
			maxtermArray[output].addMinterm(bf.buildMinterm(line[0]))




print maxtermArray[0]



#resultTree = bdd.doShannon(maxtermArray[0],1, inputs)

cProfile.run("bdd.doShannon(maxtermArray[0],1, inputs)")

#print type(resultTree)
#print resultTree

#resultTree.makeQRBDD()
#resultTree.dotPrint2()


'''
# Example for shannon expansion
print "Maxterm: "
print maxtermArray[0]
print "First expansion with x1: "

# allocation
maxterm1 = copy.deepcopy(maxtermArray[0])
maxterm2 = copy.deepcopy(maxtermArray[0])

maxterm1.setLiteralTrue('x1')
maxterm2.setLiteralFalse('x1')
print "x1=1:", maxterm1
print "x1=0:", maxterm2

print maxterm2 == maxterm1

maxterm1.setLiteralTrue('x2')
print "x1=1:", maxterm1
maxterm1.setLiteralTrue('x3')
print "x1=1:", maxterm1
maxterm1.setLiteralTrue('x4')
print "x1=1:", maxterm1

print maxterm1 ==  1
print maxterm1 == [1]
print maxterm1 == 1

'''
