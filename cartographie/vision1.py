"""
Created on Fri Jan 23 12:57:16 2026

@author: victordebanne
"""
from raytracing2 import line_test, creat_matrix
from visionpath import Space, matrixify
import matplotlib.pyplot as plt

S = Space(5)
M = matrixify(S, 50, 50)
A = [45, 5] #depart
B = [5, 45] #arrivée
plt.imshow(M)
plt.show()

O = creat_matrix(50, 50)

i = 0
j = 0

for k in range(50):
    p = [i,j]
    line_test(O, M, A, p)
    i += 1
for k in range(50):
    p = [i,j]
    line_test(O, M, A, p)
    j += 1
for k in range(50):
    p = [i,j]
    line_test(O, M, A, p)
    i -= 1
for k in range(50):
    p = [i,j]
    line_test(O, M, A, p)
    j -= 1
    
plt.imshow(O)
plt.show()