import boolfunction as bf
import copy
a = bf.Minterm(0)
a.addLiteral('x1')
a.addLiteral('x2')
a.addLiteral('~x3')
a.addLiteral('~x4')
a.addLiteral('x5')

b = bf.Minterm(1)
b.addLiteral('~x1')
b.addLiteral('~x3')
b.addLiteral('x4')

c = bf.Maxterm(0)
c.addMinterm(a)
c.addMinterm(b)
tmp = copy.deepcopy(c) 
print "Maxterm: "
print c

print "\nIf x1=true:"
c.setLiteralTrue('x1')
print c

c = copy.deepcopy(tmp)
print "\nIf x2=true:"
c.setLiteralTrue('x2')
print c

c = copy.deepcopy(tmp)
print "\nIf x3=true:"
c.setLiteralTrue('x3')
print c

c = copy.deepcopy(tmp)
print "\nIf x4=true:"
c.setLiteralTrue('x4')
print c

c = copy.deepcopy(tmp)
print "\nIf x5=true:"
c.setLiteralTrue('x5')
print c

c = tmp
c = copy.deepcopy(tmp)
print "\nIf x1=false:"
c.setLiteralFalse('x1')
print c

c = tmp
c = copy.deepcopy(tmp)
print "\nIf x2=false:"
c.setLiteralFalse('x2')
print c

c = tmp
c = copy.deepcopy(tmp)
print "\nIf x3=false:"
c.setLiteralFalse('x3')
print c

c = copy.deepcopy(tmp)
print "\nIf x4=false:"
c.setLiteralFalse('x4')
print c

c = copy.deepcopy(tmp)
print "\nIf x5=false:"
c.setLiteralFalse('x5')
print c

c = copy.deepcopy(tmp)
print "\nIf x1=false and x3=false and x4=true:"
c.setLiteralFalse('x1')
c.setLiteralFalse('x3')
c.setLiteralTrue('x4')
print c
