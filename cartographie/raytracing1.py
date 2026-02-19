#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 20 17:16:50 2026

@author: victordebanne
"""

import matplotlib.pyplot as plt
import random as r

def vect(A, B):
    return [B[0] - A[0],B[1] - A[1]]

def norm(v):
    return (v[0]**2 + v[1]**2)**0.5

def mult(v, k):
    return [v[0] * k, v[1] * k]

def add(u, v):
    return [v[0] + u[0], v[1] + u[1]]

def creat_matrix(i, j):
    return [[0 for k in range(j)] for k in range(i)]

def random_noise(matrix):
    x = r.randint(0, 99)
    y = r.randint(0, 99)
    matrix[x][y] = 1

def line(out, matrix, A, B):
    matrix[A[0]][A[1]] = 2
    matrix[B[0]][B[1]] = 2
    AB = vect(A, B)
    k = 1/max(abs(AB[0]), abs(AB[1]))
    
    position = A
    for i in range(int(1/k)):
        
        if matrix[int(position[0])][int(position[1])] != 0:
            break
        else : 
            out[int(position[0])][int(position[1])] = 1
            position = add(position, mult(AB, k))
        

        
        
    

M = creat_matrix(100, 100)
O = creat_matrix(100, 100)
A = [r.randint(0, 99), r.randint(0, 99)]
B= [r.randint(0, 99), r.randint(0, 99)]

print(A, B)

O = line(O, M, A, B)

plt.imshow(M)
plt.show()

plt.imshow(O)
plt.show()