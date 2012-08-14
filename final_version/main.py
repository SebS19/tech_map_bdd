#!/usr/bin/python

import boolfunction as bf
import getopt
import bdd
import math
import basicfunctions as bas
import copy
from operator import itemgetter		# to sort dictionary of weight values

from sys import exit
import sys

def mainProcedure(inputfile, k, actSifting, plotGraph):
	f = open(inputfile,'r')
	content = f.readlines()
	f.close()
	print inputfile

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

	outputs = 1 	# comment if all outputs shall computed !!!!!
	maxtermArray = []
	variableOrderArray = []

	for i in range(outputs):
		maxtermArray.append(bf.Maxterm(i))						# i is index, increment for each output 

	for output in range(outputs):									# for each output
		equations_ONset = []								# only ON set equations
		equations_NumberOfCares = []							# gives a number for each line, which indicates how many 0s or 1s are included

		for line in equations:
		
		
				if line[1][output] == '1':			# select the line with an 1 at the end to create the minterm

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

		# add the initial order to an array
		variableOrderArray.append(weight_dic_int)

		# finally build	 the maxterm
		for line in equations_ONset:
			maxtermArray[output].addMinterm(bf.buildMinterm(line))
		

	#-------- building tree -----------------------------------------

	print "\n... creating tree",
	resultTree = bdd.doShannon(maxtermArray[0],1, inputs, weight_dic_int)		# must be done for every output !!!!
	
	print "\n\n... creating QRBDD"
	resultTree.makeQRBDD()

	print "\n... updating level"
	bdd.updateLevel(resultTree)
	if(actSifting == 1):
		print "\n\n... sifting tree"
		bdd.doSifting(resultTree)

	# update the variable order after sifting:
	weight_dic_int=bdd.getVariableOrder(resultTree,[])

	print "\nNumber of Nodes:",bdd.countNodes(resultTree)


	#--------create LUT structure ------------------------------------

	# create ld(my) for every level (actually it is not ld(my), because every ld(my)=0 becomes ld(my)=1)
	print "\n... calculating 'my' for each level"
	setOfLdMy = []
	for levels in range(1,inputs):
		ldmy = int(math.ceil(math.log(bdd.getMy(resultTree,levels+1),2)))
		# ldmy get modify if ldmy=0 -> necessary for doNaiveDecomp function
		if(ldmy == 0):
			ldmy = 1
		setOfLdMy.append(ldmy)

	# naive or smart decomposition?
	print "\n... creating LUT structure" 

	# here comes the actual decomposition algorithm which returns just an array of arrays/integers and a array of integers with the cut position within the tree
	lutstruc, cutHeights = resultTree.doNaiveDecomp(k, weight_dic_int, setOfLdMy)

	print "\nCut positions:"
	print cutHeights


	ultimativeArray = bdd.encodeCutNodes(resultTree,cutHeights)
	outputCore = bdd.getBLIF(ultimativeArray, resultTree)



	#------write BLIF file ------------------------------------------
	print "\n... creating BLIF file"

	outputName = f.name.split('/')[-1].split('.')[0]+ '_%s_feasible' %k

	outputContent = ".model " + outputName + "\n.inputs" 
	for inVar in range(1,inputs+1):
		outputContent += " x%s" %inVar
	outputContent += "\n.outputs y\n\n" + outputCore

	print "\n########## BLIF #########\n\n" + outputContent
	print "#########################"

	outputFile = open(outputName + ".blif", 'w')
	outputFile.write(outputContent)
	outputFile.close()



	# ------- PLOT --------------------------------------------------
	if(plotGraph == 1):
		print "\n... plotting tree"
		resultTree.dotPrint2()

	print "\nDone. Result saved in " + outputName +".\n"

	exit(1)



def main(argv):
   inputfile = ''
   try:
      opts, args = getopt.getopt(argv,"hi:k:s:p:")
   except getopt.GetoptError:
      print 'Error: ./main.py -i <inputfile> -k <LUT size> [-s <sifting activation> -p <plot graph>]'
      exit(2)
   actSifting = '0'
   plotGraph = '0'
   for opt, arg in opts:
      if opt == '-h':
         print './main.py -i <inputfile> -k <LUT size> [-s <sifting activation> -p <plot graph>]'
         sys.exit()
      elif opt in ("-i"):
         inputfile = arg
      elif opt in ("-k"):
         k = arg
      elif opt in ("-s"):
	 actSifting = arg
      elif opt in ("-p"):
	 plotGraph = arg
	
   k = int(k)
   if not(k > 0):
	print "Error: k must be positive"
	sys.exit()

   if not(plotGraph == '0' or plotGraph == '1'):
	print "Error: p must be 0 or 1"
	sys.exit()
   else:
	plotGraph = int(plotGraph)

   if not(actSifting == '0' or actSifting == '1'):
	print "Error: s must be 0 or 1"
	sys.exit()
   else:
	actSifting = int(actSifting)

   mainProcedure(inputfile, k, actSifting, plotGraph)

if __name__ == "__main__":
   main(sys.argv[1:])
