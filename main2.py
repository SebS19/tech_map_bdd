import boolfunction as bf
import bdd
import math
from operator import itemgetter		# to sort dictionary of weight values

import cProfile

#------- file read ---------------------------------------------

f = open('absp2.pla','r')
#f = open('absp_i28.pla','r')			#i28
#f = open('blif_src/spla.pla','r')		#i16
#f = open('blif_src/apex2.pla','r')		#i39
#f = open('blif_src/seq.pla','r')		#i41
#f = open('blif_src/ex1010.pla','r')		#i10
#f = open('blif_src/pdc.pla','r')		#i16
#f = open('blif_src/apex4.pla','r')		#i9
f = open('blif_src/misex3.pla','r')		#i14
#f = open('blif_src/ex5.pla','r')		#i8

# define your k here
k = 7 

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
	
	if line[0][0] != '.' and len(line) >= 2:
		equations.append([ line[0] , line[1][:-1]])


#------- create minterms from blif equations  ---------------------

outputs = 1	# delete if all outputs shall computed !!!!!
maxtermArray = []

for i in range(outputs):
	maxtermArray.append(bf.Maxterm(i))						# i is index, increment for every output 

for output in range(outputs):									# for every output
	equations_ONset = []								# only ON set equations
	equations_NumberOfCares = []							# gives a number for each line, which indicates how many 0s or 1s are included

	for line in equations:
	
	
			if line[1][output] == '1':			# select the line with an 1 at the end to create the minterm
				#print line[0]
				equations_ONset.append(line[0])
				tempCareCounter = 0	
				for position in range(inputs):
					if (line[0][position] == '0' or line[0][position] == '1'):
						tempCareCounter += 1
				equations_NumberOfCares.append(float(tempCareCounter))

	#------- sort inputs depending on variable weights ----------------
	weight_dic = {}						# dictionary in the form of {'x1': 0.7337, 'x2': 0.1234, ... }
	numberOfLines = float(len(equations_ONset))
	
	# all values to zero
	for i in range(inputs):
		weight_dic['x' + str(i+1)]=0
	# update weigth for each variable
	for i in range(inputs):
		for index, line in enumerate(equations_ONset):
			if(line[i] == '0' or line[i] == '1'):
				weight_dic['x' + str(i+1)] += 1.0/equations_NumberOfCares[index] * 1.0/numberOfLines
	
	# sort weight_dic
	weight_dic = sorted(weight_dic.items(), key=itemgetter(1))	# notice that dictionary becomes a list of tuples now

	# weight list becomes a list of variable indeces in sorted order [9, 3, ...]
	weight_dic_int = []
	for var in weight_dic:
		weight_dic_int.append(int(var[0][1:]))
	# lowest value at the beginning -> must be reversed
	weight_dic_int.reverse()

	# finally build the maxterm
	for line in equations_ONset:
		maxtermArray[output].addMinterm(bf.buildMinterm(line))
	

#-------- building tree -----------------------------------------

print "\n... creating tree",
resultTree = bdd.doShannon(maxtermArray[0],1, inputs, weight_dic_int)		# must be done for every output !!!!

#cProfile.run("bdd.doShannon(maxtermArray[0],1, inputs)")

#print resultTree

print "\n\n... creating QRBDD"
resultTree.makeQRBDD()

#--------create LUT structure ------------------------------------
# create ld(my) for every level (actually it is not ld(my), because every ld(my)=0 becomes ld(my)=1)
setOfLdMy = []
for levels in range(1,inputs):
	ldmy = int(math.ceil(math.log(bdd.getMy(resultTree,levels+1),2)))
	# ldmy gets modify if ldmy=0 -> necessary for doNaiveDecomp function
	if(ldmy == 0):
		ldmy = 1
	setOfLdMy.append(ldmy)

resultTree.dotPrint2()
print "\n... creating LUT structure" 

lutstruc = resultTree.doNaiveDecomp(k, weight_dic_int, setOfLdMy)
print "\nChosen %s-LUT structure:" %k
print lutstruc




# my for each level
print "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
print "'My' for each height:"
for levels in range(1,inputs):
	my = bdd.getMy(resultTree,levels+1)
	print "Level",levels,":", my
	gain = levels - int(math.ceil(math.log(my,2)))
 	print "Gain:", gain

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
