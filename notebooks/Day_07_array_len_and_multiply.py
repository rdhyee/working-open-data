# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

# What if you try to make an array with lists w/ non-matching lengths?

try:
    k = np.array(([1,2], [3,4,5]))
except Exception as e:
    print e
else:
    print k.ndim, k.shape
    assert k.ndim == 1
    assert k.shape == (2,)

# <codecell>

k

# <codecell>

# array multiplication is not matrix muliplication

a0 = arange(4).reshape(2,2)

print a0*a0
print np.dot(a0,a0)

# <codecell>

#how to prepend a series?

a10 = arange(10)

# <codecell>

#how to prepend a series?

a10 = arange(10)
a10

# <codecell>

# can't use extend on numpy.ndarray

try:
    a10.extend(-1)
except Exception as e:
    print e

# <codecell>

# append

list0 = [0,1,2]
list0.append(3)
list0

# <codecell>

# extend

list0.extend([-1])
list0

# <codecell>

# insert

list0.insert(0,-2)
list0

# <codecell>

# use np.insert

np.insert(a10,0,-1)

