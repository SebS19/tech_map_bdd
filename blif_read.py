#import pycudd as pc
#from eqn import *

import bdd
'''
m = pc.DdManager()
m.SetDefault()

#----------------CLASS DEF -------------------

class eqn:
	def __init__(self,m):
		self.logic=m.IthVar(0) & ~m.IthVar(0)

	def addLogic(self, newString, m):
		sub=m.IthVar(0) | ~ m.IthVar(0)
		
		i=0
		for literal in newString:
			
			if 	literal == '1':
				sub &= m.IthVar(i)

			elif literal == '0':
				sub &= ~m.IthVar(i)

			elif literal == '-':
				sub &= (m.IthVar(i) | ~m.IthVar(i))

			else:
				print "you shouldnt see me"
			
			i+=1
		
		self.logic |= sub

	def printMinterm(self):
		self.logic.PrintMinterm()

''' 

#------- file read ---------------------------------------------

f = open('absp.pla','r')

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


#------- create output objects ---------------------

output_eqn = []
for i in range(outputs):
	output_eqn.append(bdd.createTree(inputs))



#------- extract on-set to output functions ----------

lineCounter=0
for line in equations:

	for x in range(outputs):

		if line[1][x] == '1':
			print line[0]
			bdd.adjust(line[0], output_eqn[x])



#------- done! -------------

print "inputs: %i" %inputs
print "outputs: %i" %outputs

#for x in range(len(output_eqn)):
#	output_eqn[x].dotPrint2()
output_eqn[0].dotPrint2()





