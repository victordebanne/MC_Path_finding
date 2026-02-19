#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  7 10:25:18 2026

@author: victordebanne
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Champs de forces pour exploration vers l'inconnu
"""

import matplotlib.pyplot as plt
import time 
import random as r

def create_matrix(i, j):
    return [[0 for k in range(j)] for k in range(i)]

def vect(a, b):
    return [b[0] - a[0], b[1] - a[1]]

def norm(v):
    return (v[0]**2 + v[1]**2)**0.5

def normalize(v):
    return [v[0] / norm(v), v[1] / norm(v)]

def rotate(v, sens = 1):
    return [-v[1] * sens, v[0] * sens]

def mult(v, k):
    return [v[0] * k, v[1] * k]

def add(u, v):
    return [u[0] + v[0], u[1] + v[1]]

def find_biggest(matrix):
    maxi = matrix[0][0]
    coord = [0,0]
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] >= maxi : 
                maxi = matrix[i][j]
                coord = [i,j]
                
    return coord
            
    return 


M = create_matrix(100, 100)
M[45][45] = 2
M[30][45] = 2
M[20][70] = 2

plt.imshow(M)
plt.show()

class Agent():
    def __init__(self):
        self.pos = [25, 25]
        self.speed = [0, 0]

    def emptyest_square(self, matrix, nb = 10):
        scores = create_matrix(int(len(matrix)/nb), int(len(matrix[0])/nb))
        #découpage de la matrice en grille 10 par 10
        for i in range(nb):
            for j in range(nb):
                #pour chaque grille 10x10
                for k in range(int(len(matrix)/nb)):
                    for l in range(int(len(matrix[0])/nb)):
                        if matrix[int(k + i*len(matrix)/nb)][int(l + j*len(matrix[0])/nb)] == 0 : 
                            scores[i][j] += 1
        maxi = find_biggest(scores)
        plt.imshow(scores)
        plt.show() 
        return maxi[0] * int(len(matrix)/nb), maxi[1] * int(len(matrix[0])/nb)
    
    def update(self):
        self.pos = add(self.pos, mult(self.speed, 3))
        self.pos = [int(self.pos[0]),int(self.pos[1])]
        
        
A = Agent()                                
        
for i in range(5000):                
   
    M[A.pos[0]][A.pos[1]] = 1
    A.speed = normalize(vect(A.pos,A.emptyest_square(M)))
    print(A.speed)
    print(A.pos)
    A.update()

                
        


