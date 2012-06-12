import boolfunction as bf
import copy

#------- file read ---------------------------------------------

f = open('absp.pla','r')
#f = open('blif_src/spla.pla','r')
#f = open('blif_src/apex2.pla','r')
#f = open('blif_src/seq.pla','r')
#f = open('blif_src/ex1010.pla','r')
#f = open('blif_src/pdc.pla','r')
#f = open('blif_src/apex4.pla','r')
#f = open('blif_src/misex3.pla','r')
#f = open('blif_src/ex5.pla','r')


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

print "BLIF input On set:"
maxterm = bf.Maxterm(0)		# 0 is index, increment for every output 
for line in equations:

	for x in range(outputs):

		if line[1][x] == '1':
			print line[0]
			maxterm.addMinterm(bf.buildMinterm(line[0]))

# Example for shannon expansion
print "Maxterm: "
print maxterm
print "First expansion with x1: "
maxterm1 = bf.Maxterm(1)
maxterm2 = bf.Maxterm(2)
maxterm1 = copy.deepcopy(maxterm)
maxterm2 = copy.deepcopy(maxterm)
maxterm1.setLiteralTrue('x1')
maxterm2.setLiteralFalse('x1')
print "x1=1:", maxterm1
print "x1=0:", maxterm2

