#! /usr/bin/python -i

import pycudd as pyc
m = pyc.DdManager()
m.SetDefault()

x1 = m.IthVar(0)
x2 = m.IthVar(1)
x3 = m.IthVar(2)
x4 = m.IthVar(3)
x5 = m.IthVar(4)

f = (x1 & x2 & ~x3 & ~x4 & ~x5) + (~x3 & ~x4 & x5) + (~x1 & ~x2 & ~x3 & x4 & ~x5) + (~x1 & x2 & ~x3 & x4 & ~x5) + (x1 & ~x2 & ~x3 & x4 & ~x5) + (x1 & x2 & ~x3 & x4 & x5) + (~x1 & ~x2 & x3 & ~x4 & ~x5) + (x1 & ~x2 & x3 & ~x4 & ~x5) + (x3 & ~x4 & x5) + (~x1 & x2 & x3 & x4 & ~x5) + (x1 & x2 & x3 & x4 & ~x5) + (~x1 & ~x2 & x3 & x4 & x5) + (x1 & ~x2 & x3 & x4 & x5)

print "Funktion:"
f.PrintMinterm()
print " "
fc = ~f
print "Funktion negiert:"
fc.PrintMinterm()
print " "

# Over nodes     
print "Over nodes ..."
pyc.set_iter_meth(1)
for node in f:
    print "***"
    node.PrintMinterm()
