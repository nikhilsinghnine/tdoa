import numpy
import math
a=[1,2,3,4,5,6,7,8,9]
t=[]
for i in range(len(a)):
	temp=a[i]
	b=[item for item in a if item!=temp]
	print str(b)